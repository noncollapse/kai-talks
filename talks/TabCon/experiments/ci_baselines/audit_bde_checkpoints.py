"""Read-only verification of the original BDE outlier's code and checkpoints."""
import hashlib
import json
import sys
from pathlib import Path
import run_task  # CPU/thread environment, no training.
import numpy as np
import tensorflow as tf

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'runtime_vendor' / 'bde'))
from neural_networks import negative_log_likelihood


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


report = {'source': [], 'checkpoints': []}
upstream = next(x for x in json.loads((ROOT / 'upstream.json').read_text()) if x['alias'] == 'bde')
for item in upstream['files']:
    if item['name'] not in {'experiment1.py', 'neural_networks.py', 'intervals.py', 'metrics.py', 'utils.py'}:
        continue  # Only these five pinned files were deployed for this baseline.
    content = (ROOT / 'vendor' / 'bde' / item['name']).read_bytes()
    digest = hashlib.sha1(f'blob {len(content)}\0'.encode() + content).hexdigest()
    assert digest == item['git_blob_sha'], item['name']
    report['source'].append(dict(file=item['name'], official_git_blob_verified=True))
for item in json.loads((ROOT / 'runtime_vendor' / 'patches.json').read_text()):
    if item['path'].startswith('vendor/bde/'):
        name = Path(item['path']).name
        assert sha(ROOT / 'runtime_vendor' / 'bde' / name) == item['runtime_sha256'], name
report['runtime_matches_recorded_patches'] = True
report['adapter_sha256'] = sha(ROOT / 'run_task.py')
report['patch_script_sha256'] = sha(ROOT / 'patch_vendor.py')

original = ROOT / 'runs/full/bde/high_noise__053'
replay = ROOT / 'runs/audit/bde_high_noise_053_seed_0'
for i in range(5):
    path = original / 'savednetworks' / f'ensemble_member_{i}.keras'
    before = sha(path)
    a = tf.keras.models.load_model(path, custom_objects={'negative_log_likelihood': negative_log_likelihood})
    b = tf.keras.models.load_model(replay / 'savednetworks' / path.name,
                                  custom_objects={'negative_log_likelihood': negative_log_likelihood})
    assert int(a.optimizer.iterations) == int(b.optimizer.iterations) == 1736
    assert len(a.weights) == len(b.weights)
    assert len(a.optimizer.variables()) == len(b.optimizer.variables())
    for va, vb in zip(a.weights + a.optimizer.variables(), b.weights + b.optimizer.variables()):
        np.testing.assert_array_equal(va.numpy(), vb.numpy())
    assert sha(path) == before
    report['checkpoints'].append(dict(member=i, sha256=before, optimizer_iteration=1736,
        bitwise_equal_weights_and_optimizer=True, original_file_unchanged=True))

path = ROOT / 'runs/audit/checkpoint_audit.json'
path.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(dict(official_sources_verified=len(report['source']),
                     runtime_patches_verified=True, original_checkpoints_verified=5)))
