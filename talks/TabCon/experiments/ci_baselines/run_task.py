"""One isolated baseline/task process. Inputs and oracle are kept separate."""
import argparse
import hashlib
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

# Apply before importing numerical libraries. GPU is occupied by unrelated jobs.
for name in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
             'TF_NUM_INTRAOP_THREADS', 'TF_NUM_INTEROP_THREADS']:
    os.environ[name] = '1'
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '2')
os.environ.setdefault('TF_ENABLE_ONEDNN_OPTS', '0')

import numpy as np

ROOT = Path(__file__).resolve().parent
NAMES = dict(grf='GRF', llf='Local Linear Forest', bde='BDE', deeplr='DeepLR')


def dump(path, obj):
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(obj, indent=2, allow_nan=False) + '\n')
    tmp.replace(path)


def seed_for(*parts):
    return int.from_bytes(hashlib.sha256('\x1f'.join(map(str, parts)).encode()).digest()[:8],
                          'little') % (2**31-1)


def timeout_handler(signum, frame):
    raise TimeoutError('DeepLR per-query timeout: retained as a failure, not a finite CI')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--method', choices=NAMES, required=True)
    p.add_argument('--task', required=True)
    p.add_argument('--data', type=Path, default=ROOT/'data')
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--smoke', action='store_true')
    p.add_argument('--query-limit', type=int, default=0)
    p.add_argument('--threads', type=int, default=1)
    p.add_argument('--query-timeout', type=int, default=1800)
    args = p.parse_args()
    args.out = args.out.resolve()
    args.data = args.data.resolve()
    args.out.mkdir(parents=True, exist_ok=True)
    task_dir = args.data/args.task
    meta = json.loads((task_dir/'metadata.json').read_text())
    assert meta['validated_against_saved_wald']
    inputs_path = task_dir/'inputs.npz'
    assert hashlib.sha256(inputs_path.read_bytes()).hexdigest() == meta['files']['inputs.npz']
    with np.load(inputs_path) as inputs:
        X, y, Xq = inputs['X'], inputs['y'], inputs['Xq']
    if args.query_limit:
        Xq = Xq[:args.query_limit]
    seed = seed_for(args.method, args.task, 770001)
    config = dict(method=args.method, seed=seed, smoke=args.smoke, query_limit=args.query_limit,
                  input_sha256=meta['files']['inputs.npz'], nominal_coverage=.95,
                  adapter_version=3,
                  preprocessing='Original context-only Wald encoder; drop constant columns')
    if args.method == 'bde':
        config.update(members=2 if args.smoke else 5, hidden=[40,30,20],
                      epochs=2 if args.smoke else 80, save_epoch=1 if args.smoke else 56,
                      retrain_epochs=1 if args.smoke else 24, regularization='1/n', batch_size=32)
    elif args.method == 'deeplr':
        config.update(mean_hidden=[40,30,20], var_hidden=[5,2],
                      epochs=2 if args.smoke else 400,
                      perturb_epochs=2 if args.smoke else 400, n_steps=100,
                      delta=1, fraction=1/16, reg_mean=1e-4, reg_var=1e-4, batch_size=32)
        config['query_copies'] = max(1,int(len(y)/16))
    else:
        config.update(num_trees=100 if args.smoke else 2000, honesty=True,
                      ci_group_size=2, threads=args.threads)
    if (args.out/'config.json').exists():
        assert json.loads((args.out/'config.json').read_text()) == config, 'Refusing mixed protocol resume'
    else:
        dump(args.out/'config.json', config)
    if (args.out/'metrics.json').exists():
        print('Already complete', args.method, args.task, flush=True)
        return
    os.chdir(args.out)
    started = time.monotonic()
    dump(args.out/'status.json', dict(status='running', pid=os.getpid(), task=args.task,
                                     method=args.method, started_at=time.time()))
    if args.method in ('grf', 'llf'):
        for name, a in [('X', X), ('y', y[:,None]), ('Xq', Xq)]:
            np.savetxt(name+'.csv', a, delimiter=',', header=','.join(f'v{i}' for i in range(a.shape[1])), comments='')
        env = dict(os.environ, R_LIBS_USER=str(ROOT/'rlib'))
        subprocess.run(['/home/kyle/miniconda3/envs/RIAID/bin/Rscript', str(ROOT/'forest.R'),
                        args.method, str(args.out), str(seed), str(config['num_trees']),
                        str(args.threads)], env=env, check=True)
        predictions = np.genfromtxt('predictions.csv', delimiter=',', names=True)
        mean = predictions['mean']
        ci = np.column_stack([predictions['lower'], predictions['upper']])
        aux = json.loads(Path('forest_metadata.json').read_text())
    else:
        import tensorflow as tf
        tf.config.threading.set_intra_op_parallelism_threads(args.threads)
        tf.config.threading.set_inter_op_parallelism_threads(1)
        tf.keras.utils.set_random_seed(seed)
        sys.path.insert(0, str(ROOT/'runtime_vendor'/args.method))
        if args.method == 'bde':
            from neural_networks import gen_deep_ensemble, gen_extra_deep_ensemble
            from intervals import PICI_bootstrapped_deep_ensemble, deep_ensemble_prediction
            Path('savednetworks').mkdir(exist_ok=True)
            deep = gen_deep_ensemble(X, y, M=config['members'], hidden_units=config['hidden'],
                                    n_epochs=config['epochs'], save_epoch=config['save_epoch'],
                                    verbose=False, reg=True)
            # Author's method explicitly resumes the checkpoint optimizer state.
            # Native .keras fixes TF 2.15's SavedModel loader silently resetting it.
            from neural_networks import negative_log_likelihood
            expected_iterations = config['save_epoch'] * int(np.ceil(len(y)/32))
            for i in range(config['members']):
                restored = tf.keras.models.load_model(f'savednetworks/ensemble_member_{i}.keras',
                    custom_objects={'negative_log_likelihood':negative_log_likelihood})
                assert int(restored.optimizer.iterations)==expected_iterations
                assert len(restored.optimizer.variables())>1
                del restored
            extra = gen_extra_deep_ensemble(X, deep, retrain_epochs=config['retrain_epochs'])
            # N_samples affects only the discarded PI. The returned CI is analytic.
            _, ci = PICI_bootstrapped_deep_ensemble(deep, extra, Xq, alpha=.05, N_samples=2)
            mean = deep_ensemble_prediction(deep, Xq)
            # Independent check that the official return is the mean CI, not the PI.
            from scipy.stats import t
            # Upstream allocates Y/Z as float64 before doing arithmetic; preserve
            # that here too (float32 subtraction caused a false validation failure).
            member = np.array([m.f(Xq) for m in deep], dtype=np.float64)
            boot = np.array([m.f(Xq) for m in extra], dtype=np.float64)
            variance = np.mean((member-boot)**2, axis=0) + np.var(member, axis=0, ddof=1)/len(deep)
            half = t.ppf(.975, df=len(deep)-1)*np.sqrt(variance)
            np.testing.assert_allclose(ci, np.column_stack([mean-half,mean+half]), rtol=1e-6, atol=1e-8)
            np.savez_compressed('members.npz', means=member, bootstrap_means=boot, variance=variance)
            aux = dict(ci_formula_verified=True, checkpoint_optimizer_verified=True,
                       checkpoint_optimizer_iterations=expected_iterations,tensorflow=tf.__version__)
        else:
            from mve_network import MVENetwork, negative_log_likelihood
            from intervals_regression import CI_NNx
            Path('models').mkdir(exist_ok=True)
            if Path('models/base.keras').exists():
                network = MVENetwork.__new__(MVENetwork)
                network._normalization = True
                network._X_mean, network._X_std = np.mean(X,axis=0), np.std(X,axis=0)
                network._Y_mean, network._Y_std = np.mean(y), np.std(y)
                network.model = tf.keras.models.load_model('models/base.keras',
                    custom_objects={'negative_log_likelihood':negative_log_likelihood})
            else:
                network = MVENetwork(X=X, Y=y, n_hidden_mean=config['mean_hidden'],
                    n_hidden_var=config['var_hidden'], n_epochs=config['epochs'],
                    reg_mean=config['reg_mean'], reg_var=config['reg_var'], verbose=False)
                network.model.save('models/base.keras')
            mean = network.f(Xq)
            mu_hats, sigma_hats = network.f(X), network.sigma(X)
            assert np.all(np.isfinite(mean)) and np.all(np.isfinite(mu_hats))
            assert np.all(np.isfinite(sigma_hats)) and np.all(sigma_hats>0)
            ci = np.full((len(Xq),2),np.nan)
            query_times = []
            Path('queries').mkdir(exist_ok=True)
            signal.signal(signal.SIGALRM, timeout_handler)
            for j, x in enumerate(Xq):
                saved = Path('queries')/f'{j:04d}.json'
                if saved.exists():
                    result = json.loads(saved.read_text())
                else:
                    tf.keras.utils.set_random_seed(seed_for('deeplr-query',seed,j))
                    tick = time.monotonic()
                    signal.alarm(args.query_timeout)
                    try:
                        bounds = CI_NNx(MVE_network=network, x=x, X_train=X, Y_train=y,
                            mu_hats=mu_hats, sigma_hats=sigma_hats, n_steps=config['n_steps'],
                            alpha=.05, n_epochs=config['perturb_epochs'], delta=1, fraction=1/16)
                    finally:
                        signal.alarm(0)
                    bounds = [float(np.asarray(v).item()) for v in bounds]
                    assert np.all(np.isfinite(bounds)) and bounds[1]>=bounds[0]
                    result = dict(query=j, lower=bounds[0], upper=bounds[1], seconds=time.monotonic()-tick)
                    dump(saved,result)
                ci[j] = [result['lower'],result['upper']]
                query_times.append(result['seconds'])
                dump(Path('status.json'),dict(status='running', method=args.method, task=args.task,
                    queries_complete=j+1, queries_total=len(Xq), elapsed_seconds=time.monotonic()-started,
                    mean_query_seconds=float(np.mean(query_times))))
                print(json.dumps(dict(task=args.task,**result)),flush=True)
            aux = dict(tensorflow=tf.__version__, query_seconds=query_times)
    assert np.all(np.isfinite(ci)) and np.all(np.isfinite(mean))
    assert ci.shape==(len(Xq),2) and np.all(ci[:,1]>=ci[:,0])
    elapsed = time.monotonic()-started
    np.savez_compressed('predictions.npz', mean=mean, lower=ci[:,0], upper=ci[:,1])
    # Evaluation only: oracle is first loaded after fitting and intervals finish.
    oracle_path = task_dir/'oracle.npy'
    assert hashlib.sha256(oracle_path.read_bytes()).hexdigest()==meta['files']['oracle.npy']
    target = np.load(oracle_path)[:len(Xq)]
    covered = (target>=ci[:,0]) & (target<=ci[:,1])
    metrics = dict(task=args.task, stress=meta['stress'], episode=meta['episode'],
        method=NAMES[args.method], n_context=len(y), n_query=len(Xq),
        n_features=meta['n_features'], encoded_features=X.shape[1],
        coverage_95=float(np.mean(covered)), length_95=float(np.mean(ci[:,1]-ci[:,0])),
        mean_rmse=float(np.sqrt(np.mean((mean-target)**2))), total_seconds=elapsed,
        complete_task=len(Xq)==meta['n_query'], production=not args.smoke,
        input_sha256=meta['files']['inputs.npz'], aux=aux)
    dump(Path('metrics.json'),metrics)
    dump(Path('status.json'),dict(status='finished',seconds=elapsed))
    print(json.dumps(metrics),flush=True)


if __name__=='__main__':
    main()
