"""Publish a full-method aggregate only when every original query/task is present."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent


def main():
    p=argparse.ArgumentParser();p.add_argument('--runs',type=Path,default=ROOT/'runs/full')
    p.add_argument('--methods',nargs='+',default=['grf','llf','bde']);args=p.parse_args()
    manifest=json.loads((ROOT/'data/manifest.json').read_text())
    by_task={m['task']:m for m in manifest}
    status={};summaries=[]
    for method in args.methods:
        rows=[]
        for task,meta in by_task.items():
            path=args.runs/method/task/'metrics.json'
            if not path.exists():continue
            row=json.loads(path.read_text())
            assert row['complete_task'] and row['production']
            assert row['input_sha256']==meta['files']['inputs.npz'] and row['n_query']==meta['n_query']
            # Recompute metrics from saved predictions to detect serialization/evaluation mistakes.
            pred=np.load(path.parent/'predictions.npz')
            truth=np.load(ROOT/'data'/task/'oracle.npy')
            assert np.all(np.isfinite(pred['lower'])) and np.all(pred['upper']>=pred['lower'])
            assert np.isclose(row['coverage_95'],np.mean((truth>=pred['lower'])&(truth<=pred['upper'])))
            assert np.isclose(row['length_95'],np.mean(pred['upper']-pred['lower']))
            rows.append(row)
        status[method]=dict(finished=len(rows),total=len(manifest),complete=len(rows)==len(manifest))
        if len(rows)!=len(manifest):continue
        for stress in sorted({m['stress'] for m in manifest}):
            selected=[r for r in rows if r['stress']==stress]
            assert len(selected)==128
            summaries.append(dict(method=rows[0]['method'],regime=stress,tasks=128,
                coverage_95=float(np.mean([r['coverage_95'] for r in selected])),
                length_95=float(np.mean([r['length_95'] for r in selected])),
                mean_rmse=float(np.mean([r['mean_rmse'] for r in selected])),
                mean_seconds=float(np.mean([r['total_seconds'] for r in selected]))))
    (args.runs/'completion.json').write_text(json.dumps(status,indent=2)+'\n')
    if summaries:
        with (args.runs/'completed_methods_summary.csv').open('w') as f:
            writer=csv.DictWriter(f,fieldnames=list(summaries[0]));writer.writeheader();writer.writerows(summaries)
    print(json.dumps(status,indent=2))


if __name__=='__main__':main()
