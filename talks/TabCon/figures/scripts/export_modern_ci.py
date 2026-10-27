"""Export completed second-batch methods after local, per-query verification."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT = ROOT/'experiments/ci_baselines'
NAMES = {'bratp': 'BRAT-P', 'bratd': 'BRAT-D', 'rfu': 'RF-U', 'iebm': 'Inferable EBM'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--methods', nargs='+', choices=NAMES, required=True)
    args = parser.parse_args()
    manifest = json.loads((EXPERIMENT/'data/manifest.json').read_text())
    assert len(manifest)==1280
    alignment = json.loads((EXPERIMENT/'data/alignment.json').read_text())
    assert alignment['status']=='passed' and alignment['tasks']==1280
    rows, provenance = [], {}
    for method in args.methods:
        root = EXPERIMENT/'runs/modern_full'/method
        launch = json.loads((root/'launch.json').read_text())
        remote = json.loads((root/'provenance.json').read_text())
        assert launch['manifest_sha256']==sha(EXPERIMENT/'data/manifest.json')
        assert sha(root/'launch.json')==remote['launch_sha256']
        digest, tasks = hashlib.sha256(), []
        for meta in manifest:
            folder = root/meta['task']
            cfg = json.loads((folder/'config.json').read_text())
            expected = dict(launch['configuration'], input_sha256=meta['files']['inputs.npz'],
                seed=int.from_bytes(hashlib.sha256(
                  '\x1f'.join([method,meta['task'],'770001']).encode()).digest()[:8],
                  'little') % (2**31-1))
            assert cfg==expected
            r = json.loads((folder/'metrics.json').read_text())
            assert r['production'] and r['complete_task'] and r['quality_passed']
            assert r['method']==NAMES[method] and r['input_sha256']==cfg['input_sha256']
            assert r['n_context']==meta['n_context'] and r['n_query']==meta['n_query']
            with np.load(folder/'predictions.npz') as data:
                low,high,mean = [data[k] for k in ('lower','upper','mean')]
                oracle_path = EXPERIMENT/'data'/meta['task']/'oracle.npy'
                assert sha(oracle_path)==meta['files']['oracle.npy']
                oracle = np.load(oracle_path)
                assert low.shape==high.shape==mean.shape==oracle.shape
                assert all(np.isfinite(a).all() for a in (low,high,mean,oracle))
                assert (low<=high).all()
                from statistics import NormalDist
                se=data['standard_error']
                np.testing.assert_allclose(low,mean-NormalDist().inv_cdf(.975)*se,rtol=1e-7,atol=1e-8)
                np.testing.assert_allclose(high,mean+NormalDist().inv_cdf(.975)*se,rtol=1e-7,atol=1e-8)
                values = [np.mean((low<=oracle)&(oracle<=high)),np.mean(high-low),
                          np.sqrt(np.mean((mean-oracle)**2))]
                np.testing.assert_allclose(values,
                  [r['coverage_95'],r['length_95'],r['mean_rmse']],rtol=1e-12,atol=1e-12)
            digest.update((meta['task']+':'+sha(folder/'predictions.npz')+'\n').encode())
            tasks.append(r)
        assert digest.hexdigest()==remote['prediction_manifest_sha256']
        for regime in sorted({r['stress'] for r in tasks}):
            selected = [r for r in tasks if r['stress']==regime]
            assert len(selected)==128
            rows.append(dict(method=NAMES[method],interval_kind=cfg['interval_kind'],
              regime=regime,tasks=128,
              coverage_95=float(np.mean([r['coverage_95'] for r in selected])),
              length_95=float(np.mean([r['length_95'] for r in selected]))))
        provenance[NAMES[method]] = dict(remote, locally_verified=True,
            source_versions=tasks[0]['aux'], configuration=launch['configuration'])
    out = ROOT/'figures/data'
    target = out/'stress_modern_ci_results.csv'
    with target.open('w') as f:
        writer = csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)
    report = dict(source=target.name,source_sha256=sha(target),methods=provenance,
        original_plot_source_sha256=alignment['current_plot_sha256'],
        manifest_sha256=sha(EXPERIMENT/'data/manifest.json'),
        target='Same saved latent oracle as original plot; no estimand change.',
        protocol='experiments/ci_baselines/PROTOCOL_MODERN.md',
        excluded_methods=[NAMES[m] for m in NAMES if m not in args.methods],
        cancelled_methods=['BART', 'GP', 'DeepLR'],
        cancellation_reason='User excluded Bayesian credible-interval baselines')
    (out/'stress_modern_ci_provenance.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:{s:v[s] for s in ['tasks','queries','mean_coverage','mean_length']}
                      for k,v in provenance.items()},indent=2))


if __name__=='__main__':
    main()
