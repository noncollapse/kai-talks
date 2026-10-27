"""Keep upstream files untouched; create a separately hashed compatibility copy."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PATCHES = {
    ('bde', 'neural_networks.py'): [
        ('from keras.layers import Lambda, Wrapper, Input, Dense, merge',
         'from keras.layers import Lambda, Wrapper, Input, Dense'),
        ('np.int(', 'int('),
        ("f'./savednetworks/{name}'", "f'./savednetworks/{name}.keras'"),
        ('.predict(X_test)', '.predict(X_test, verbose=0)'),
    ],
    ('deeplr', 'intervals_regression.py'): [('import scipy\n', 'import scipy\nfrom scipy import stats\n')],
    ('deeplr', 'mve_network.py'): [('N_extra = int(N * fraction)',
                                 'N_extra = max(1, int(N * fraction))')],
}


def main():
    report = []
    for path in sorted((ROOT / 'vendor').glob('*/*')):
        if not path.is_file():
            continue
        destination = ROOT / 'runtime_vendor' / path.parent.name / path.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        original = path.read_text()
        content = original
        changes = []
        for old, new in PATCHES.get((path.parent.name, path.name), []):
            assert old in content, (path, old)
            changes.append(dict(old=old, new=new, count=content.count(old)))
            content = content.replace(old, new)
        destination.write_text(content)
        report.append(dict(path=str(path.relative_to(ROOT)),
            upstream_sha256=hashlib.sha256(original.encode()).hexdigest(),
            runtime_sha256=hashlib.sha256(content.encode()).hexdigest(), changes=changes))
    (ROOT / 'runtime_vendor' / 'patches.json').write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
