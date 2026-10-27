"""Run four additional baselines on frozen tasks; gate each method on its pilots."""
import argparse
import concurrent.futures
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

from run_extra_task import configuration, NAMES, ROOT
from run_task import dump, seed_for

PILOTS = ['near_constant__029', 'near_constant__106', 'categorical_missing__099',
          'high_noise__053', 'asymmetric_extreme_outlier__116']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected_config(method, meta):
    result = configuration(method)
    result.update(seed=seed_for(method, meta['task'], 770001),
                  input_sha256=meta['files']['inputs.npz'])
    return result


def validate(folder, method, meta):
    assert json.loads((folder/'config.json').read_text()) == expected_config(method, meta)
    r = json.loads((folder/'metrics.json').read_text())
    assert r['production'] and r['complete_task'] and r['quality_passed']
    assert r['method'] == NAMES[method]
    assert r['input_sha256'] == meta['files']['inputs.npz']
    assert r['n_query'] == meta['n_query'] and r['n_context'] == meta['n_context']
    assert (folder/'predictions.npz').exists()
    if method in ('bart', 'gp'):
        assert r['aux']['converged']
    return r


def run_queue(method, workers, tasks, out, pilots, sources):
    # Per-method lock allows independently cleared methods to proceed.
    method_out = out/method
    method_out.mkdir(parents=True, exist_ok=True)
    lock = (method_out/'.controller.lock').open('a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    by_name = {t['task']: t for t in tasks}
    checks = []
    for task in PILOTS:
        folder = pilots/method/task
        row = validate(folder, method, by_name[task])
        checks.append(dict(task=task, seconds=row['total_seconds'],
                           metrics_sha256=sha(folder/'metrics.json')))
    snapshot = dict(method=method, workers=workers, tasks=len(tasks),
        queries=sum(t['n_query'] for t in tasks), pid=os.getpid(), started_at=time.time(),
        configuration=configuration(method), sources=sources, pilot_checks=checks,
        manifest_sha256=sha(ROOT/'data/manifest.json'), device='CPU')
    previous = method_out/'launch.json'
    if previous.exists():
        old = json.loads(previous.read_text())
        for key in ('configuration', 'sources', 'manifest_sha256'):
            assert snapshot[key] == old[key], f'Mixed protocol resume: {key}'
    else:
        dump(previous, snapshot)

    def run(meta):
        for source, digest in sources.items():
            assert sha(ROOT/source) == digest, 'Source changed during active queue'
        folder = method_out/meta['task']
        folder.mkdir(parents=True, exist_ok=True)
        if (folder/'metrics.json').exists():
            validate(folder, method, meta)
            return dict(task=meta['task'], status='finished', resumed=True)
        with (folder/'run.log').open('a') as log:
            result = subprocess.run([str(ROOT/'venv/bin/python'), str(ROOT/'run_extra_task.py'),
                '--method', method, '--task', meta['task'], '--out', str(folder)],
                stdout=log, stderr=log)
        if result.returncode == 0:
            validate(folder, method, meta)
        row = dict(task=meta['task'], status='finished' if result.returncode==0 else 'failed',
                   returncode=result.returncode)
        dump(folder/'exit.json', row)
        print(json.dumps(dict(method=method, **row)), flush=True)
        return row

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(run, t) for t in tasks]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
            dump(out/f'{method}.progress.json', dict(method=method, total=len(tasks),
                 finished=sum(r['status']=='finished' for r in results),
                 failed=sum(r['status']=='failed' for r in results),
                 failure_tasks=[r['task'] for r in results if r['status']=='failed'],
                 workers=workers, updated_at=time.time()))
    dump(method_out/'queue_complete.json', dict(results=results, finished_at=time.time()))
    fcntl.flock(lock, fcntl.LOCK_UN)
    lock.close()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--methods', nargs='+', choices=NAMES, required=True)
    p.add_argument('--workers', nargs='+', type=int, required=True)
    p.add_argument('--out', type=Path, default=ROOT/'runs/extra_full')
    p.add_argument('--pilots', type=Path, default=ROOT/'runs/extra_pilots_v2')
    args = p.parse_args()
    assert len(args.methods)==len(args.workers) and all(w>0 for w in args.workers)
    tasks = json.loads((ROOT/'data/manifest.json').read_text())
    assert len(tasks)==1280
    alignment = json.loads((ROOT/'data/alignment.json').read_text())
    assert alignment['status']=='passed' and alignment['tasks']==1280
    args.out.mkdir(parents=True, exist_ok=True)
    sources = {name: sha(ROOT/name) for name in
               ['run_extra_task.py', 'extra_methods.R', 'run_task.py', 'launch_extra_suite.py']}
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(args.methods)) as pool:
        futures = [pool.submit(run_queue, m, w, tasks, args.out, args.pilots, sources)
                   for m, w in zip(args.methods, args.workers)]
        for future in futures:
            future.result()
    subprocess.run([str(ROOT/'venv/bin/python'), str(ROOT/'aggregate_extra.py'),
                    '--runs', str(args.out)], check=True)


if __name__=='__main__':
    main()
