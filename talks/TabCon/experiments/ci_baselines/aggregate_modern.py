"""Verify raw intervals and export a method only after all original tasks pass."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import numpy as np
from launch_modern_suite import validate, sha
from run_modern_task import NAMES, ROOT
from run_task import dump


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--runs', type=Path, default=ROOT/'runs/modern_full')
    args = p.parse_args()
    manifest = json.loads((ROOT/'data/manifest.json').read_text())
    assert len(manifest)==1280
    statuses = {}
    cancellation_path = args.runs/'cancellations.json'
    cancelled = json.loads(cancellation_path.read_text())['methods'] if cancellation_path.exists() else []
    for method, name in NAMES.items():
        if method in cancelled:
            statuses[method] = dict(status='cancelled_by_user', plotted=False)
            continue
        if not (args.runs/method).exists():
            continue
        rows, provenance = [], hashlib.sha256()
        for meta in manifest:
            folder = args.runs/method/meta['task']
            if not (folder/'metrics.json').exists():
                continue
            row = validate(folder, method, meta)
            with np.load(folder/'predictions.npz') as prediction:
                lower, upper, mean = [prediction[k] for k in ['lower', 'upper', 'mean']]
                oracle_path = ROOT/'data'/meta['task']/'oracle.npy'
                assert sha(oracle_path)==meta['files']['oracle.npy']
                oracle = np.load(oracle_path)
                assert lower.shape==upper.shape==mean.shape==oracle.shape
                assert all(np.isfinite(a).all() for a in (lower, upper, mean, oracle))
                assert (lower<=upper).all()
                from scipy.stats import norm
                se=prediction['standard_error']
                np.testing.assert_allclose(lower,mean-norm.ppf(.975)*se,rtol=1e-7,atol=1e-8)
                np.testing.assert_allclose(upper,mean+norm.ppf(.975)*se,rtol=1e-7,atol=1e-8)
                cp = np.mean((lower<=oracle)&(oracle<=upper))
                width = np.mean(upper-lower)
                rmse = np.sqrt(np.mean((mean-oracle)**2))
                np.testing.assert_allclose([cp,width,rmse],
                  [row['coverage_95'],row['length_95'],row['mean_rmse']],rtol=1e-12,atol=1e-12)
            provenance.update((meta['task']+':'+sha(folder/'predictions.npz')+'\n').encode())
            rows.append(row)
        statuses[method] = dict(finished=len(rows), total=len(manifest),
                                complete=len(rows)==len(manifest))
        if len(rows)!=len(manifest):
            continue
        summary = []
        for stress in sorted({r['stress'] for r in rows}):
            selected = [r for r in rows if r['stress']==stress]
            assert len(selected)==128
            summary.append(dict(method=name, interval_kind=rows[0]['interval_kind'],
                 regime=stress, tasks=128,
                 coverage_95=float(np.mean([r['coverage_95'] for r in selected])),
                 length_95=float(np.mean([r['length_95'] for r in selected])),
                 mean_seconds=float(np.mean([r['total_seconds'] for r in selected]))))
        stream = io.StringIO()
        writer = csv.DictWriter(stream, fieldnames=list(summary[0]))
        writer.writeheader();writer.writerows(summary)
        tmp = args.runs/method/'summary.csv.tmp'
        tmp.write_text(stream.getvalue())
        tmp.replace(args.runs/method/'summary.csv')
        report = dict(method=name, interval_kind=rows[0]['interval_kind'], tasks=len(rows),
            queries=sum(r['n_query'] for r in rows),
            prediction_manifest_sha256=provenance.hexdigest(),
            mean_coverage=float(np.mean([r['coverage_95'] for r in rows])),
            mean_length=float(np.mean([r['length_95'] for r in rows])),
            mean_seconds=float(np.mean([r['total_seconds'] for r in rows])),
            manifest_sha256=sha(ROOT/'data/manifest.json'),
            launch_sha256=sha(args.runs/method/'launch.json'),
            target='Same saved latent oracle as original plot; no estimand change',
            aggregation='Equal-weight queries within tasks, tasks within stress regimes, then regimes')
        dump(args.runs/method/'provenance.json', report)
    dump(args.runs/'completion.json', statuses)
    print(json.dumps(statuses,indent=2))


if __name__=='__main__':
    main()
