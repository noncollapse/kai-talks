"""Run production-size interface/numerical pilots, never tune on their coverage."""
from concurrent.futures import ThreadPoolExecutor
import argparse
import json
import subprocess
from launch_modern_suite import PILOTS, ROOT, validate
from run_modern_task import NAMES

p=argparse.ArgumentParser()
p.add_argument('--methods',nargs='+',choices=NAMES,required=True)
args=p.parse_args()
tasks={t['task']:t for t in json.loads((ROOT/'data/manifest.json').read_text())}

def run(item):
    method,task=item;out=ROOT/'runs/modern_pilots'/method/task
    out.mkdir(parents=True,exist_ok=True)
    with (out/'run.log').open('a') as log:
        r=subprocess.run([str(ROOT/'venv_modern/bin/python'),str(ROOT/'run_modern_task.py'),
            '--method',method,'--task',task,'--out',str(out)],stdout=log,stderr=log)
    if r.returncode:
        print(json.dumps(dict(method=method,task=task,failed=True)),flush=True)
        return False
    row=validate(out,method,tasks[task])
    print(json.dumps(dict(method=method,task=task,seconds=row['total_seconds'],passed=True)),flush=True)
    return True

with ThreadPoolExecutor(max_workers=min(8,2*len(args.methods))) as pool:
    good=list(pool.map(run,[(m,t) for t in PILOTS for m in args.methods]))
assert all(good),'At least one pilot failed; inspect logs before launching that method'
