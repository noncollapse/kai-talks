"""Pinned author implementations on the original saved tasks. Oracle is evaluation only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import run_task  # Set numerical threads to one before importing NumPy.
import numpy as np
from scipy.stats import norm

ROOT = Path(__file__).resolve().parent
NAMES = {'bratp': 'BRAT-P', 'bratd': 'BRAT-D', 'rfu': 'RF-U', 'iebm': 'Inferable EBM'}
BOULEVARD = 'ec0a4ede4155519b70fbca65ac73f9ece64da276'
RLT = 'd83a648a15591bbd4f057322dfdea7a75f056992'
R_BIN = '/home/kyle/miniconda3/envs/RIAID/bin/Rscript'
dump = run_task.dump


def configuration(method, smoke=False):
    c = dict(method=method, adapter_version=1, nominal_coverage=.95,
             interval_kind='confidence', smoke=smoke, threads=1,
             preprocessing='Frozen original context-only Wald encoding; context y standardized then inverted',
             source_commit=RLT if method=='rfu' else BOULEVARD)
    if method == 'rfu':
        c.update(package='RLT', trees_schedule=[200] if smoke else [10000,40000,160000],
                 retry='Only nonfinite/negative sampling variance; no coverage-based selection or clamping',
                 var_mode='matched', resample_replace=False, resample_prob=.5,
                 reinforcement=False, nmin=5, mtry='max(1,floor(p/2))',
                 importance='distribute (official variance-mode requirement)')
    else:
        c.update(package='boulevard-boosting', interval_mode='confidence',
                 variance_source='Official prepare_inference() training-residual variance; all context rows retained',
                 calibration='None: no oracle, query responses, or PI calibration',
                 hyperparameter_source='Author README examples, fixed before evaluation')
        if method == 'bratp':
            c['parameters'] = dict(n_rounds=4 if smoke else 70, trees_per_round=6,
                subsample_rate=.8,max_depth=8,max_leaf_nodes=64,min_samples_leaf=4,
                max_bins=64,drop_first_round=True,n_jobs=1)
        elif method == 'bratd':
            c['parameters'] = dict(max_iter=20 if smoke else 700,learning_rate=.8,
                dropout_rate=.1,subsample_rate=.8,max_depth=6,max_leaf_nodes=64,
                min_samples_leaf=2,max_bins=64)
        else:
            c['parameters'] = dict(max_rounds=12 if smoke else 160,max_bins=32,
                learning_rate=.6,subsample_rate=1.,warmup_rounds=2 if smoke else 10,
                max_depth=4,min_samples_leaf=8,leave_one_out=False)
    return c


def fit_boulevard(X, y, Xq, config, out):
    import importlib.metadata
    import sklearn
    from boulevard import DropoutBooster, ParallelBooster, ExplainableBooster
    cls = dict(bratp=ParallelBooster,bratd=DropoutBooster,iebm=ExplainableBooster)[config['method']]
    model = cls(**config['parameters'], random_state=config['seed']).fit(X, y)
    model.prepare_inference()
    lo, hi, mean = model.predict_intervals(Xq, level=.95, mode='confidence')
    np.testing.assert_allclose(mean, model.predict(Xq),rtol=1e-10,atol=1e-10)
    residuals = y-model.predict(X)
    sigma2 = float(np.var(residuals,ddof=1))
    np.testing.assert_allclose(model.sigma_hat2_,sigma2,rtol=1e-10,atol=1e-12)
    norms = model.weight_norms(Xq)
    scale, sigma, fallback = 1., float(np.sqrt(sigma2)), False
    if config['method']=='bratd':
        p = config['parameters'];scale = (1+p['learning_rate']*(1-p['dropout_rate']))/p['learning_rate']
    elif config['method']=='iebm':
        scale = float(model.boulevard_scale_)
        if sigma2<=0:
            fallback = True
            sigma = float(model.sigma_) if getattr(model,'sigma_',0)>0 else 1e-8
    se = scale*sigma*norms
    half = norm.ppf(.975)*se
    np.testing.assert_allclose(lo,mean-half,rtol=1e-7,atol=1e-8)
    np.testing.assert_allclose(hi,mean+half,rtol=1e-7,atol=1e-8)
    np.savez_compressed(out/'inference_diagnostics.npz',mean_standardized=mean,
        se_standardized=se,weight_norms=norms,sigma2=sigma2,sigma_used=sigma,scale=scale)
    return mean, np.column_stack([lo,hi]), se, dict(
        package_version=importlib.metadata.version('boulevard-boosting'),sklearn_version=sklearn.__version__,
        official_commit=BOULEVARD, interval_mode='confidence',
        sigma2_standardized=sigma2,scale=scale,sigma_fallback_used=fallback,
        independent_interval_check=True,observation_noise_excluded=True)


def fit_rfu(X,y,Xq,config,out):
    for name,array in [('X',X),('y',y[:,None]),('Xq',Xq)]:
        np.savetxt(out/(name+'.csv'),array,delimiter=',',
                   header=','.join(f'v{i}' for i in range(array.shape[1])),comments='')
    env=dict(os.environ,R_LIBS_USER=f'{ROOT}/rlib_modern:{ROOT}/rlib')
    subprocess.run([R_BIN,str(ROOT/'modern_rfu.R'),str(out)],check=True,env=env)
    p = np.genfromtxt(out/'predictions.csv',delimiter=',',names=True)
    mean,variance = p['mean'],p['variance']
    assert np.isfinite(variance).all() and (variance>=0).all()
    se=np.sqrt(variance);half=norm.ppf(.975)*se
    ci=np.column_stack([p['lower'],p['upper']])
    np.testing.assert_allclose(ci,np.column_stack([mean-half,mean+half]),rtol=1e-7,atol=1e-8)
    aux=json.loads((out/'method_metadata.json').read_text())
    aux.update(independent_interval_check=True,observation_noise_excluded=True,official_commit=RLT)
    np.savez_compressed(out/'inference_diagnostics.npz',mean_standardized=mean,se_standardized=se,
                        variance_standardized=variance)
    return mean,ci,se,aux


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--method',choices=NAMES,required=True)
    p.add_argument('--task',required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--smoke',action='store_true')
    args=p.parse_args();out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    task=ROOT/'data'/args.task;meta=json.loads((task/'metadata.json').read_text())
    assert meta['validated_against_saved_wald']
    input_sha=hashlib.sha256((task/'inputs.npz').read_bytes()).hexdigest()
    assert input_sha==meta['files']['inputs.npz']
    with np.load(task/'inputs.npz') as data:
        X,y,Xq=[np.asarray(data[k],dtype=float) for k in ('X','y','Xq')]
    assert len(y)==meta['n_context'] and len(Xq)==meta['n_query']
    assert all(np.isfinite(a).all() for a in (X,y,Xq))
    config=configuration(args.method,args.smoke)
    config.update(seed=run_task.seed_for(args.method,args.task,770001),input_sha256=input_sha)
    if (out/'config.json').exists():
        assert json.loads((out/'config.json').read_text())==config,'Mixed protocol resume'
    else:dump(out/'config.json',config)
    if (out/'metrics.json').exists():
        print('Already complete',args.method,args.task,flush=True);return
    start=time.monotonic()
    dump(out/'status.json',dict(status='running',task=args.task,method=args.method,pid=os.getpid(),started_at=time.time()))
    ym,ys=float(y.mean()),float(y.std())
    assert ys>0
    fit=fit_rfu if args.method=='rfu' else fit_boulevard
    mean,ci,se,aux=fit(X,(y-ym)/ys,Xq,config,out)
    mean=mean*ys+ym;ci=ci*ys+ym;se=se*ys
    assert mean.shape==(len(Xq),) and ci.shape==(len(Xq),2) and se.shape==mean.shape
    assert all(np.isfinite(a).all() for a in (mean,ci,se)) and (ci[:,1]>=ci[:,0]).all()
    np.testing.assert_allclose(ci,np.column_stack([mean-norm.ppf(.975)*se,mean+norm.ppf(.975)*se]),rtol=1e-7,atol=1e-8)
    np.savez_compressed(out/'predictions.npz',mean=mean,lower=ci[:,0],upper=ci[:,1],standard_error=se,y_mean=ym,y_sd=ys)
    elapsed=time.monotonic()-start
    aux.update(context_y_mean=ym,context_y_sd=ys)
    dump(out/'fit_diagnostics.json',aux)
    # All fitting and intervals are finished before the oracle is loaded.
    assert hashlib.sha256((task/'oracle.npy').read_bytes()).hexdigest()==meta['files']['oracle.npy']
    oracle=np.load(task/'oracle.npy')
    metrics=dict(task=args.task,stress=meta['stress'],episode=meta['episode'],method=NAMES[args.method],
        interval_kind='confidence',n_context=len(y),n_query=len(Xq),n_features=meta['n_features'],encoded_features=X.shape[1],
        coverage_95=float(np.mean((oracle>=ci[:,0])&(oracle<=ci[:,1]))),length_95=float(np.mean(ci[:,1]-ci[:,0])),
        mean_rmse=float(np.sqrt(np.mean((mean-oracle)**2))),total_seconds=elapsed,
        complete_task=True,production=not args.smoke,quality_passed=True,input_sha256=input_sha,aux=aux)
    dump(out/'metrics.json',metrics);dump(out/'status.json',dict(status='finished',seconds=elapsed))
    print(json.dumps(metrics),flush=True)


if __name__=='__main__':main()
