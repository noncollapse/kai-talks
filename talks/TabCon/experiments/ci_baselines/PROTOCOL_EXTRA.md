# RF-IJ, DRF, BART and GP on the frozen stress benchmark

**Current scope: RF-IJ and DRF.** On 27 October 2026 the user removed Bayesian
credible-interval baselines, cancelling BART and GP. Their saved pilot/partial
results and protocol descriptions below are retained only for provenance; they
must not be resumed or plotted without a new instruction. The GP queue was stopped.
This does not restart the cancelled DeepLR experiments or replace the original BDE
result with its stabilized diagnostic run. No GitHub publication is authorized.

## Data and target

All methods read the same saved `inputs.npz` arrays for all 1,280 tasks and all
155,520 queries described in [PROTOCOL.md](PROTOCOL.md). No training rows, features
or queries are resampled or removed. Per-task input hashes are checked. The
context-only encoding and removal of context-constant columns are unchanged.

The original generator allows 8–2,048 context observations, sampling with equal
probability from a uniform or log-uniform size distribution. The realized range
in these 1,280 tasks is 9–2,039, with median 426.5; 180 tasks have fewer than 30 rows
and 370 have fewer than 100. These are counts of context rows per evaluation task,
not pretraining observations. See `evidence/dataset-sizes.json`. Different methods
always see the same sample size within a task.

As before, the target is the stored `f_query_oracle_raw`. It is a transformed
hidden SCM node, not in general guaranteed to equal `E[Y | observed X]`. The
comparison preserves this benchmark and does not establish a frequentist coverage
guarantee for a conditional mean. The oracle file is opened only after interval
predictions and convergence diagnostics have been saved.

## Implementations and intervals

| Method | Official implementation | Prespecified configuration and interval |
| --- | --- | --- |
| RF-IJ | `ranger` 0.18.0 | 2,000 trees, bootstrap sampling, minimum node size 5, retained in-bag counts; `predict(type="se", se.method="infjack")`; estimate ± 1.96 × IJ SE |
| DRF | `drf` 1.3.1 | 6,000 honest trees, 100 CI groups of 60 trees, minimum node size 5, sampling fraction 0.5, FourierMMD with 10 random features; native `predict(estimate.uncertainty=TRUE)` |
| BART | `dbarts` 0.9-34 | 200 trees, four chains, k=2, tree prior base=.95/power=2, noise prior df=3/quantile=.9; .025/.975 quantiles of latent-function posterior draws |
| GP | `GPflow` 2.9.1 | Exact Gaussian process, isotropic Matérn-5/2 kernel, Gaussian likelihood, zero mean after context-only response centering; latent posterior mean ± 1.96 × latent SD |

RF-IJ and DRF are confidence-interval procedures. **BART and GP are Bayesian
credible intervals**, now excluded at the user's request.
All are evaluated at nominal 95% using the same saved target. None uses response
quantiles or an observation-noise-inclusive prediction interval as a substitute.

DRF's official uncertainty output supplies a matrix of weights for each CI group.
For the conditional-mean functional, each group's estimate is exactly its weights
times the training response vector. The estimated variance is the sample variance
of these group means, not that variance divided by the number of groups. This is
the native inference API's resampling distribution. The overall mean must equal
the average group mean. We use exact weighted means instead of adding Monte Carlo
sampling noise to the functional calculation.

BART sets the noise-prior scale `sigest=sd(y_context)` consistently for every task.
The default OLS estimate is undefined on some of these p≥n tasks. This is an
explicit, context-only choice of prior scale, not a parameter tuned to oracle
coverage. There is no added observation noise in saved `yhat.test` draws.

GP standardizes each input and the response using context mean and population
standard deviation, then unscales its posterior. Kernel variance, one length scale
and noise variance are fitted by L-BFGS-B marginal likelihood (up to 300 iterations,
ftol 1e-9, gtol 1e-5). Two deterministic initial length scales are .5√p and 2√p,
with initial noise variance .1; the lower training objective is retained. The
isotropic baseline avoids fitting hundreds of ARD length scales on tiny tasks.
An initial ARD pilot was retained as a diagnostic, not pooled with this protocol.
Independent NumPy Cholesky calculations verify the exact latent posterior. The
difference between `predict_y` and `predict_f` variances must equal the fitted noise
variance, confirming it is excluded from the reported interval.

## Numerical checks and MCMC

Production pilots use the complete original tasks `near_constant__029` (n=9),
`near_constant__106` (n=2,039), `categorical_missing__099` (409 encoded features),
`high_noise__053`, and `asymmetric_extreme_outlier__116`. Smoke outputs and earlier
failed pilots are retained separately and never included in the figure.

BART starts with 1,000 burn-in and 2,000 retained draws per chain. The official
`posterior` package 1.7.0 computes rank-normalized split R-hat, bulk ESS and tail ESS
for every query's latent-function draws. The prespecified gate is maximum R-hat
≤1.05 and minimum bulk/tail ESS ≥400. If it fails, the **same chains** continue,
doubling new burn-in and retained draws, up to four continuation rounds (32,000
retained draws per chain in the last round). Only the latest round enters the
interval calculation; earlier rounds serve as additional warm-up. The stopping
rule never uses the oracle, coverage or interval width. All round diagnostics are
saved. A task that still fails is an explicit failure and blocks the full-method
aggregate; it is not dropped or silently called converged.

GP requires convergence of its selected marginal-likelihood solution. BART
quantiles, RF-IJ Wald endpoints and DRF group-variance endpoints are independently
recomputed in Python from saved underlying outputs. Every interval must be finite
and ordered. Configurations, input hashes, versions and source hashes are saved.

## Execution and aggregation

`launch_extra_suite.py` checks the five production pilots separately for each
method before starting its 1,280-task queue. Per-method locks prevent duplicate
controllers; resumes require identical configurations and source hashes. CPU-only
workers each use one numerical-compute thread. The occupied GPU and unrelated
experiments are left untouched. Package additions use isolated `venv/` and `rlib/`.

`aggregate_extra.py` verifies every saved interval against the original oracle and
only exports a method after all 1,280 tasks pass. Queries are averaged within each
task, tasks equally within each stress regime, and regimes equally overall. All
failure counts remain visible. Raw posterior draws and diagnostics stay on Beast;
plot-ready summaries are separate from the existing GRF/LLF/BDE result files.

## Sources

- [ranger uncertainty API](https://imbs-hl.github.io/ranger/reference/predict.ranger.html)
- [DRF native inference documentation](https://github.com/cran/drf/blob/master/man/predict.drf.Rd)
- [DRF paper](https://www.jmlr.org/papers/v24/23-0185.html)
- [dbarts authors' implementation](https://github.com/vdorie/dbarts)
- [dbarts sampler continuation](https://github.com/vdorie/dbarts/blob/main/man/dbartsSampler-class.Rd)
- [posterior diagnostics](https://mc-stan.org/posterior/reference/diagnostics.html)
- [GPflow exact Gaussian process regression](https://gpflow.github.io/GPflow/2.9.1/notebooks/basics/regression.html)
