"""Bounded, resumable CPU queues. Failures remain explicit, never dropped from denominators."""
import argparse
import concurrent.futures
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT=Path(__file__).resolve().parent


def run_queue(method,workers,tasks,out):
    def run(meta):
        task=meta['task']
        folder=out/method/task
        folder.mkdir(parents=True,exist_ok=True)
        log=folder/'run.log'
        if (folder/'metrics.json').exists():
            r=json.loads((folder/'metrics.json').read_text())
            assert r['production'] and r['complete_task']
            assert r['input_sha256']==meta['files']['inputs.npz']
            return dict(task=task,status='finished',resumed=True)
        with log.open('a') as f:
            process=subprocess.run([str(ROOT/'venv/bin/python'),str(ROOT/'run_task.py'),
                '--method',method,'--task',task,'--out',str(folder)],stdout=f,stderr=f)
        state='finished' if process.returncode==0 else 'failed'
        result=dict(task=task,status=state,returncode=process.returncode)
        (folder/'exit.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(dict(method=method,**result)),flush=True)
        return result
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures=[pool.submit(run,t) for t in tasks]
        for f in concurrent.futures.as_completed(futures):
            results.append(f.result())
            progress=dict(method=method,workers=workers,total=len(tasks),
                finished=sum(r['status']=='finished' for r in results),
                failed=sum(r['status']=='failed' for r in results),updated_at=time.time(),
                failure_tasks=[r['task'] for r in results if r['status']=='failed'])
            (out/f'{method}.progress.json').write_text(json.dumps(progress,indent=2)+'\n')
    return results


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',type=Path,default=ROOT/'runs/full')
    p.add_argument('--methods',nargs='+',default=['grf','llf','bde'])
    p.add_argument('--workers',nargs='+',type=int,default=[2,2,6])
    args=p.parse_args()
    assert len(args.methods)==len(args.workers)
    report=json.loads((ROOT/'data/alignment.json').read_text())
    assert report['status']=='passed' and report['tasks']==1280
    tasks=json.loads((ROOT/'data/manifest.json').read_text())
    assert len(tasks)==1280
    args.out=args.out.resolve();args.out.mkdir(parents=True,exist_ok=True)
    lock=(args.out/'.controller.lock').open('w')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    gate=json.loads((ROOT/'pilot_gate.json').read_text())
    assert gate['status']=='passed'
    snapshot=dict(started_at=time.time(),pid=os.getpid(),methods=args.methods,workers=args.workers,
        tasks=len(tasks),queries=sum(m['n_query'] for m in tasks),device='CPU',
        alignment_sha256=hashlib.sha256((ROOT/'data/alignment.json').read_bytes()).hexdigest(),
        sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                 [ROOT/'run_task.py',ROOT/'forest.R',ROOT/'patch_vendor.py',ROOT/'upstream.json']})
    (args.out/'launch.json').write_text(json.dumps(snapshot,indent=2)+'\n')
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(args.methods)) as pool:
        futures=[pool.submit(run_queue,m,w,tasks,args.out) for m,w in zip(args.methods,args.workers)]
        for f in futures: f.result()
    print('All queues finished. Inspect failure counts before aggregating.',flush=True)
    subprocess.run([str(ROOT/'venv/bin/python'),str(ROOT/'aggregate.py'),
                    '--runs',str(args.out),'--methods',*args.methods],check=True)


if __name__=='__main__':main()
