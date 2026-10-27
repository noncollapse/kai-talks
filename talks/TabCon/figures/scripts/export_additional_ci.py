"""Export only complete, paired CI experiments into the slide's plotting data."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT = ROOT / 'experiments/ci_baselines'
RUNS = EXPERIMENT / 'runs/full'
OUT = ROOT / 'figures/data'
METHODS = {'grf': 'GRF', 'llf': 'Local Linear Forest', 'bde': 'BDE'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    global EXPERIMENT, RUNS, OUT
    parser = argparse.ArgumentParser()
    parser.add_argument('--experiment-dir', type=Path, default=EXPERIMENT)
    parser.add_argument('--output-dir', type=Path, default=OUT)
    args = parser.parse_args()
    EXPERIMENT = args.experiment_dir.resolve()
    RUNS = EXPERIMENT/'runs/full'
    OUT = args.output_dir.resolve()
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((EXPERIMENT / 'data/manifest.json').read_text())
    assert len(manifest) == 1280
    paired = json.loads((EXPERIMENT / 'data/alignment.json').read_text())
    assert paired['status'] == 'passed' and paired['tasks'] == 1280
    rows, provenance = [], {}
    for key, name in METHODS.items():
        tasks = []
        digest = hashlib.sha256()
        for task in manifest:
            folder = RUNS / key / task['task']
            result = json.loads((folder / 'metrics.json').read_text())
            assert result['method'] == name and result['production'] and result['complete_task']
            assert result['input_sha256'] == task['files']['inputs.npz']
            assert result['n_query'] == task['n_query']
            with np.load(folder / 'predictions.npz') as predictions:
                lower, upper, mean = [predictions[k] for k in ['lower', 'upper', 'mean']]
                target = np.load(EXPERIMENT / 'data' / task['task'] / 'oracle.npy')
                assert lower.shape == upper.shape == mean.shape == target.shape
                assert all(np.isfinite(x).all() for x in [lower, upper, mean, target])
                assert (upper >= lower).all()
                cp = float(np.mean((target >= lower) & (target <= upper)))
                length = float(np.mean(upper - lower))
                np.testing.assert_allclose([cp, length], [result['coverage_95'], result['length_95']],
                                           rtol=1e-12, atol=1e-12)
            digest.update((task['task'] + ':' + sha(folder/'predictions.npz') + '\n').encode())
            tasks.append(result)
        for stress in sorted({t['stress'] for t in tasks}):
            selected = [r for r in tasks if r['stress'] == stress]
            assert len(selected) == 128
            rows.append(dict(method=name, regime=stress, tasks=128,
                             coverage_95=float(np.mean([r['coverage_95'] for r in selected])),
                             length_95=float(np.mean([r['length_95'] for r in selected]))))
        extreme = max(tasks, key=lambda r: r['length_95'])
        provenance[name] = dict(tasks=len(tasks), queries=sum(r['n_query'] for r in tasks),
            prediction_manifest_sha256=digest.hexdigest(),
            mean_coverage=float(np.mean([r['coverage_95'] for r in tasks])),
            mean_length=float(np.mean([r['length_95'] for r in tasks])),
            largest_task=dict(task=extreme['task'], mean_length=extreme['length_95'],
                fraction_of_total_length=extreme['length_95']/sum(r['length_95'] for r in tasks)))
    target_csv = OUT / 'stress_additional_ci_results.csv'
    with target_csv.open('w') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    report = dict(source=target_csv.name, source_sha256=sha(target_csv),
        original_plot_source_sha256=paired['current_plot_sha256'],
        alignment_sha256=sha(EXPERIMENT/'data/alignment.json'),
        target='Same saved latent oracle as the original plot; no estimand change.',
        aggregation='Queries within each task, then equal-weight tasks and stress settings; no trimming.',
        methods=provenance, excluded_method='DeepLR cancelled by user',
        bde_note='One high-noise task has extreme bootstrap-network predictions; its original finite CI is retained.',
        protocol='experiments/ci_baselines/PROTOCOL.md')
    (OUT/'stress_additional_ci_provenance.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
