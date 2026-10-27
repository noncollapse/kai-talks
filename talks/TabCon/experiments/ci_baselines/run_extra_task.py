"""RF-IJ, DRF inference, BART and exact GP on the original frozen episodes.

This adapter deliberately leaves the first baseline batch's code unchanged.
Only the evaluator loads the stored oracle, after fitting and saving predictions.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import run_task  # Original one-thread CPU environment.
import numpy as np
from scipy.stats import norm

ROOT = Path(__file__).resolve().parent
NAMES = {'rfij': 'RF-IJ', 'drf': 'DRF', 'bart': 'BART', 'gp': 'GP'}
R_BIN = '/home/kyle/miniconda3/envs/RIAID/bin/Rscript'
dump = run_task.dump


def configuration(method, smoke=False):
    c = dict(method=method, adapter_version=2, nominal_coverage=.95,
             interval_kind='credible' if method in ('bart', 'gp') else 'confidence',
             preprocessing='Frozen original context-only Wald encoding; constant columns removed',
             smoke=smoke, threads=1)
    if method == 'rfij':
        c.update(package='ranger', num_trees=100 if smoke else 2000,
                 replace=True, sample_fraction=1., min_node_size=5,
                 standard_error='infjack', keep_inbag=True)
    elif method == 'drf':
        c.update(package='drf', num_trees=100 if smoke else 6000,
                 ci_groups=10 if smoke else 100, min_node_size=5,
                 splitting_rule='FourierMMD', num_features=10,
                 sample_fraction=.5, honesty=True, response_scaling=True,
                 uncertainty='Official CI-group weights; exact weighted mean; sample variance')
    elif method == 'bart':
        c.update(package='dbarts', num_trees=20 if smoke else 200,
                 chains=2 if smoke else 4, burn=20 if smoke else 1000,
                 samples_per_chain=30 if smoke else 2000, thinning=1,
                 continuation_rounds=0 if smoke else 4,
                 max_rank_rhat=1.05, min_bulk_ess=400, min_tail_ess=400,
                 continuation='Double burn and retained draws; continue same chains; retain latest round only',
                 k=2., tree_base=.95, tree_power=2., sigdf=3., sigquant=.9,
                 sigest='Context response sd; conservative noise-prior scale valid also when p >= n',
                 interval='Pointwise .025/.975 quantiles of f draws; no observation noise')
    else:
        c.update(package='gpflow', kernel='Matern52 isotropic', likelihood='Gaussian',
                 x_standardize='Context mean and population sd',
                 y_standardize='Context mean and population sd',
                 optimizer='L-BFGS-B marginal likelihood', maxiter=5 if smoke else 300,
                 initial_lengthscale_multipliers=[1.] if smoke else [0.5, 2.],
                 initial_noise_variance=.1,
                 interval='predict_f mean +/- normal quantile * latent sd; empirical Bayes')
    return c


def fit_gp(X, y, Xq, config, out):
    import tensorflow as tf
    tf.config.threading.set_intra_op_parallelism_threads(1)
    tf.config.threading.set_inter_op_parallelism_threads(1)
    import gpflow
    tf.keras.utils.set_random_seed(config['seed'])
    gpflow.config.set_default_float(np.float64)
    X, y, Xq = (np.asarray(a, dtype=np.float64) for a in (X, y, Xq))
    xm, xs, ym, ys = X.mean(axis=0), X.std(axis=0), float(y.mean()), float(y.std())
    assert np.all(xs > 0) and ys > 0
    x, target, q = (X-xm)/xs, ((y-ym)/ys)[:, None], (Xq-xm)/xs
    trials = []
    best = None
    for multiplier in config['initial_lengthscale_multipliers']:
        kernel = gpflow.kernels.Matern52(lengthscales=multiplier*np.sqrt(x.shape[1]))
        model = gpflow.models.GPR((x, target), kernel=kernel,
                                 noise_variance=config['initial_noise_variance'])
        optimizer = gpflow.optimizers.Scipy()
        result = optimizer.minimize(model.training_loss, model.trainable_variables,
            method='L-BFGS-B', options=dict(maxiter=config['maxiter'], ftol=1e-9, gtol=1e-5))
        loss = float(model.training_loss())
        assert np.isfinite(loss)
        trials.append(dict(initial_lengthscale_multiplier=multiplier,
                           objective=loss, success=bool(result.success),
                           message=str(result.message), iterations=int(result.nit)))
        if best is None or loss < best[0]:
            best = (loss, model, len(trials)-1)
    _, model, selected = best
    mean_f, var_f = (a.numpy().ravel() for a in model.predict_f(q))
    mean_y, var_y = (a.numpy().ravel() for a in model.predict_y(q))
    noise = float(model.likelihood.variance.numpy())
    np.testing.assert_allclose(mean_y, mean_f, rtol=1e-8, atol=1e-8)
    np.testing.assert_allclose(var_y-var_f, noise, rtol=1e-6, atol=1e-8)
    # Independent exact latent-posterior check. No white-noise term in K(q,q).
    K = model.kernel(x).numpy() + np.eye(len(x))*noise
    cross = model.kernel(x, q).numpy()
    chol = np.linalg.cholesky(K)
    from scipy.linalg import solve_triangular
    projected_y = solve_triangular(chol, target, lower=True)
    projected_q = solve_triangular(chol, cross, lower=True)
    reference_mean = (projected_q.T @ projected_y).ravel()
    reference_var = model.kernel(q, full_cov=False).numpy() - (projected_q**2).sum(axis=0)
    np.testing.assert_allclose(mean_f, reference_mean, rtol=1e-5, atol=1e-7)
    np.testing.assert_allclose(var_f, reference_var, rtol=1e-5, atol=1e-7)
    assert np.all(var_f >= -1e-9)
    variance = np.maximum(var_f, 0)*ys**2
    mean = mean_f*ys+ym
    half = norm.ppf(.975)*np.sqrt(variance)
    np.savez_compressed(out/'gp_posterior.npz', mean=mean, variance=variance,
        predictive_variance=var_y*ys**2, noise_variance=noise*ys**2,
        lengthscales=model.kernel.lengthscales.numpy(), kernel_variance=float(model.kernel.variance.numpy()),
        X_mean=xm, X_sd=xs, y_mean=ym, y_sd=ys)
    return mean, np.column_stack([mean-half, mean+half]), dict(
        gpflow_version=gpflow.__version__, tensorflow_version=tf.__version__,
        trials=trials, selected_trial=selected, converged=trials[selected]['success'],
        latent_posterior_verified=True, observation_noise_excluded=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--method', choices=NAMES, required=True)
    p.add_argument('--task', required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--smoke', action='store_true')
    args = p.parse_args()
    out = args.out.resolve();out.mkdir(parents=True, exist_ok=True)
    task = ROOT/'data'/args.task
    meta = json.loads((task/'metadata.json').read_text())
    assert meta['validated_against_saved_wald']
    input_sha = hashlib.sha256((task/'inputs.npz').read_bytes()).hexdigest()
    assert input_sha == meta['files']['inputs.npz']
    with np.load(task/'inputs.npz') as data:
        X, y, Xq = data['X'], data['y'], data['Xq']
    config = configuration(args.method, args.smoke)
    config.update(seed=run_task.seed_for(args.method, args.task, 770001), input_sha256=input_sha)
    if (out/'config.json').exists():
        assert json.loads((out/'config.json').read_text()) == config, 'Mixed protocol resume'
    else:
        dump(out/'config.json', config)
    if (out/'metrics.json').exists():
        print('Already complete', args.method, args.task, flush=True);return
    started = time.monotonic()
    dump(out/'status.json', dict(status='running', task=args.task, method=args.method,
                                 pid=os.getpid(), started_at=time.time()))
    if args.method == 'gp':
        mean, ci, aux = fit_gp(X, y, Xq, config, out)
    else:
        for name, array in [('X', X), ('y', y[:, None]), ('Xq', Xq)]:
            np.savetxt(out/(name+'.csv'), array, delimiter=',',
                       header=','.join(f'v{i}' for i in range(array.shape[1])), comments='')
        env = dict(os.environ, R_LIBS_USER=str(ROOT/'rlib'))
        subprocess.run([R_BIN, str(ROOT/'extra_methods.R'), str(out)], check=True, env=env)
        pred = np.genfromtxt(out/'predictions.csv', delimiter=',', names=True)
        mean = pred['mean'];ci = np.column_stack([pred['lower'], pred['upper']])
        aux = json.loads((out/'method_metadata.json').read_text())
        if args.method == 'bart':
            actual_samples = aux['samples_per_chain']
            draws = np.fromfile(out/'posterior_draws.bin', dtype='<f8').reshape(
                (config['chains']*actual_samples, len(Xq)), order='F')
            np.testing.assert_allclose(mean, draws.mean(axis=0), rtol=1e-7, atol=1e-8)
            np.testing.assert_allclose(ci, np.quantile(draws, [.025, .975], axis=0).T, rtol=1e-7, atol=1e-8)
            np.savez_compressed(out/'posterior_draws.npz', draws=draws,
                                chains=config['chains'], samples_per_chain=actual_samples)
            (out/'posterior_draws.bin').unlink()
            aux['posterior_quantiles_verified'] = True
        elif args.method == 'drf':
            group_means = np.loadtxt(out/'group_means.csv', delimiter=',')
            variance = np.var(group_means, axis=0, ddof=1)
            np.testing.assert_allclose(pred['variance'], variance, rtol=1e-7, atol=1e-10)
            np.testing.assert_allclose(mean, group_means.mean(axis=0), rtol=1e-6, atol=1e-8)
            half = norm.ppf(.975)*np.sqrt(variance)
            np.testing.assert_allclose(ci, np.column_stack([mean-half, mean+half]), rtol=1e-7, atol=1e-8)
            np.savez_compressed(out/'group_means.npz', means=group_means, variance=variance)
            (out/'group_means.csv').unlink()
            aux['mean_ci_verified'] = True
        else:
            half = norm.ppf(.975)*np.sqrt(pred['variance'])
            np.testing.assert_allclose(ci, np.column_stack([mean-half, mean+half]), rtol=1e-7, atol=1e-8)
            aux['wald_ci_verified'] = True
    assert mean.shape == (len(Xq),) and ci.shape == (len(Xq), 2)
    assert np.isfinite(mean).all() and np.isfinite(ci).all() and np.all(ci[:, 1] >= ci[:, 0])
    np.savez_compressed(out/'predictions.npz', mean=mean, lower=ci[:, 0], upper=ci[:, 1])
    elapsed = time.monotonic()-started
    dump(out/'fit_diagnostics.json', aux)
    if args.method in ('bart', 'gp') and not args.smoke and not aux['converged']:
        dump(out/'status.json', dict(status='failed_quality_gate', seconds=elapsed, diagnostics=aux))
        raise RuntimeError('Convergence gate failed; saved predictions excluded from aggregation')
    # No oracle access until all model calculations and saved predictions finish.
    assert hashlib.sha256((task/'oracle.npy').read_bytes()).hexdigest() == meta['files']['oracle.npy']
    oracle = np.load(task/'oracle.npy')
    metrics = dict(task=args.task, stress=meta['stress'], episode=meta['episode'],
        method=NAMES[args.method], interval_kind=config['interval_kind'], n_context=len(y),
        n_query=len(Xq), n_features=meta['n_features'], encoded_features=X.shape[1],
        coverage_95=float(np.mean((oracle>=ci[:, 0]) & (oracle<=ci[:, 1]))),
        length_95=float(np.mean(ci[:, 1]-ci[:, 0])), mean_rmse=float(np.sqrt(np.mean((mean-oracle)**2))),
        total_seconds=elapsed, complete_task=True, production=not args.smoke, quality_passed=True,
        input_sha256=input_sha, aux=aux)
    dump(out/'metrics.json', metrics)
    dump(out/'status.json', dict(status='finished', seconds=elapsed))
    print(json.dumps(metrics), flush=True)


if __name__ == '__main__':
    main()
