"""Second independent replay, using the better-conditioned original RFF baseline."""
import argparse
import hashlib
import json
import pickle
import sys
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import pandas as pd


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--original-repo',type=Path,required=True)
    p.add_argument('--data',type=Path,required=True)
    p.add_argument('--plot-csv',type=Path,required=True)
    args=p.parse_args()
    sys.path.insert(0,str(args.original_repo))
    sys.path.insert(0,str(args.original_repo/'src'))
    from experiments.wald_baselines.common import evaluate_batch,stable_seed
    ref_path=args.original_repo/'results/wald_baselines/linear_rff_hc3_seed0_20260920_104500/02_stress/raw_metrics.csv'
    reference=pd.read_csv(ref_path)
    plot=pd.read_csv(args.plot_csv)
    manifest=json.loads((args.data/'manifest.json').read_text())
    assert len(manifest)==1280
    # Establish the link between the exact historical task table and current plot.
    for name,method in [('Linear','Linear-Wald-HC3'),('RFF','RFF-Wald-HC3')]:
        means=reference[reference.system==method].groupby('suite')[['coverage_95','length_95']].mean()
        for row in plot[plot.method==name].itertuples():
            for metric in ['coverage_95','length_95']:
                assert np.isclose(means.loc[row.regime,metric],getattr(row,metric),rtol=1e-12,atol=1e-12)
    reference=reference[reference.system=='RFF-Wald-HC3'].set_index(['suite','episode'])
    reports=[]
    for meta in manifest:
        folder=args.data/meta['task']
        with (folder/'raw.pkl').open('rb') as f: raw=pickle.load(f)
        target=np.load(folder/'oracle.npy')
        batch=SimpleNamespace(X_context_raw=raw['X'],y_context_noisy_raw=raw['y'],
                              X_query_raw=raw['Xq'],f_query_oracle_raw=target)
        results,_=evaluate_batch(batch,seed=stable_seed('stress',meta['stress'],meta['episode_seed']),
                                methods=['RFF-Wald-HC3'],coverages=[.95],rff_features=64,min_residual_df=8)
        got=results['RFF-Wald-HC3']; expected=reference.loc[(meta['stress'],meta['episode'])]
        checks={k:dict(actual=float(got[k]),saved=float(expected[k]))
                for k in ['coverage_95','length_95','mean_rmse']}
        passed=all(np.isclose(v['actual'],v['saved'],rtol=1e-6,atol=1e-8) for v in checks.values())
        report=dict(task=meta['task'],passed=bool(passed),checks=checks)
        reports.append(report)
        if not passed:
            (args.data/'alignment.rff.failure.json').write_text(json.dumps(report,indent=2))
            raise RuntimeError(report)
        if len(reports)%100==0: print('RFF verified',len(reports),flush=True)
    (args.data/'alignment.rff.json').write_text(json.dumps(reports,indent=2))
    summary=json.loads((args.data/'alignment.linear.json').read_text())
    summary.update(status='passed',rf_fingerprint_tasks=len(reports),
                   current_plot_sha256=hashlib.sha256(args.plot_csv.read_bytes()).hexdigest(),
                   validation='All 1280 tasks: exact dimensions/seeds and saved Linear prediction RMSE; '
                   'independent RFF coverage, CI width and RMSE agree within rtol=1e-6, atol=1e-8. '
                   'Historical Linear and RFF aggregate results also match the current plot.',
                   linear_width_max_absolute_difference=max(abs(m['checks']['length_95']['actual']-
                     m['checks']['length_95']['saved']) for m in manifest),
                   linear_coverage_mismatch_tasks=[m['task'] for m in manifest if
                     m['checks']['coverage_95']['actual']!=m['checks']['coverage_95']['saved']])
    (args.data/'alignment.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary),flush=True)


if __name__=='__main__': main()
