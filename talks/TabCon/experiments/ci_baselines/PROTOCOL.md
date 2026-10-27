# Additional CI baselines for the existing TabCon stress plot

This is a local experiment addition. No GitHub publication is authorized.

**First-batch scope:** GRF, Local Linear Forest and BDE only. The later authorized
RF-IJ, DRF, BART and GP additions are specified separately in
[PROTOCOL_EXTRA.md](PROTOCOL_EXTRA.md). The user cancelled
DeepLR after its cost estimate. Its eight active workers were stopped, pending
jobs cancelled, and partial results excluded from aggregation. Its implementation
and pilot records below are retained for provenance, not as a completed baseline.

## Data pairing

The benchmark is the **same 1,280 episodes** underlying the current opening plot:
10 stress regimes, episodes 0–127 in each, `make_stress_generator(base_seed=770001)`.
`regular_control` is excluded, exactly as in the plot. The resulting 155,520 query
points are all retained. Training sizes vary between original episodes; they are
never changed between methods. No new random datasets, split, or query subset is
used in production.

The source evaluation directory contains seeds, configurations and per-episode
metrics, but no historical raw input arrays were located there. The original
generator source has SHA256
`ad310101c33529299885f9beb73152fd7c24a4e0a9e68f8220d0096c6f6b17e7`.
Episodes have been deterministically recovered from that source. Every episode
matches saved dimensions/seeds and Linear prediction RMSE; an independent replay
of the original RFF baseline matches coverage, CI width and RMSE within relative
tolerance `1e-6`, absolute tolerance `1e-8`. Historical aggregates for both methods
also match the CSV used by the current plot. Six ill-conditioned Linear HC3 tasks
have coverage differences under the current numerical backend; those differences
are preserved in `data/alignment.json`, not silently changed in the old plot.
This is a numerical replay audit, not a comparison with a historical raw-array hash.

Recovered inputs, raw DataFrames, oracle arrays, metadata and SHA256 hashes are
saved once under `data/`. All four adapters read those fixed files. The original
Wald context-only encoder handles missing and categorical features. Columns
constant in context are removed; no dimension reduction is applied. Native
network standardization is fitted only to context. Query outcomes and oracle
values are inaccessible to training; `oracle.npy` is first loaded for evaluation
after predictions have been saved.

The evaluation target remains the original `f_query_oracle_raw`. In this existing
SCM benchmark, that is a transformed hidden-node target and is not in general
guaranteed to equal `E[Y | observed X]`. This addition preserves the old benchmark
rather than correcting its estimand. Coverage here is coverage of the saved
oracle, not an independent validation of conditional-mean CI guarantees.

## Official methods and fixed configurations

| Method | Implementation | Configuration |
| --- | --- | --- |
| GRF | Authors' R `grf` 2.6.1, `regression_forest` and `predict(estimate.variance=TRUE)` | 2,000 trees; honesty on; CI group size 2; remaining package defaults; normal CI using estimated mean variance |
| Local Linear Forest | Same official package, `ll_regression_forest` | Same forest settings; local ridge penalty selected by official context-only cross-validation; all encoded features eligible for correction |
| BDE | [Authors' repository](https://github.com/LaurensSluyterman/Bootstrapped_Deep_Ensembles), commit `e4044b29ab80eac8036e7adbaf12ba42b42ba9c0` | Paper Section 4.2: 5 members; hidden layers 40/30/20; 80 epochs; checkpoint at 56; 24 bootstrap retraining epochs; batch 32; L2 = 1/n |
| DeepLR | [Authors' repository](https://github.com/LaurensSluyterman/Likelihood_ratio_intervals), commit `3aa81d23305e6f37ca5d96c2b108fd27f4881514` | Official regression example: mean 40/30/20, variance 5/2; 400 base epochs and 400 epochs per positive/negative perturbation; delta 1; fraction 1/16; 100 search steps per unit; L2 1e-4 |

Confidence level is 95%, matching the current plot. GRF/LLF estimate uncertainty
in the mean, not response quantiles. BDE uses the official analytic CI return;
the accompanying simulated PI is discarded. DeepLR uses the official `CI_NNx`
likelihood-ratio procedure for every query; no ensemble or Wald approximation
is substituted. Hyperparameters are fixed from the above sources, not chosen
using benchmark coverage.

## Compatibility changes

`vendor/` files match upstream Git blob hashes recorded in `upstream.json`.
`patch_vendor.py` writes separate runtime copies and records every replacement.

- BDE: replace removed `np.int` with `int`; remove an unused obsolete Keras import;
  silence prediction progress bars.
- BDE: use native `.keras` checkpoint serialization. TF 2.15's SavedModel loader
  reset the author's Adam state (saved iteration 1,456, loaded iteration 0).
  Native serialization preserves all slots and iterations. `check_optimizer.py`
  verifies equality of the next training update after reload. Each BDE task also
  asserts its checkpoint optimizer iteration count before bootstrap retraining.
- DeepLR: add the missing `scipy.stats` import used by the author's interval code.
- DeepLR: ensure at least one repeated query row. The original `int(n/16)` is zero
  for the benchmark's n=9 episode. `max(1, int(n/16))` preserves the author's
  total added-query weight of one; no training observations are added or removed.
  This is an explicit small-sample adaptation, not an unmodified upstream run.
- Separate task working directories prevent the author's fixed checkpoint
  filenames from colliding. A per-query timeout records a failure rather than
  substituting a finite interval.

TensorFlow CPU 2.15.1 / Keras 2.15, TFP 0.23.0, NumPy 1.26.4, SciPy 1.11.4 run in
a new isolated venv. The original TabPFN environment is used only to reconstruct
and audit datasets. Existing research environments/checkpoints are unchanged.

## Execution and aggregation

Smoke checks and production-configuration pilots precede the full queue, including
the original task with 9 context rows and the task with 409 encoded features.
Pilots are diagnostic only; truncated-query pilots are never plotted.

The current CPU queue uses 2 GRF workers, 2 LLF workers and 6 BDE workers,
with one numerical-compute thread each and low scheduling priority. The occupied
GPU is left to the pre-existing experiment. Active methods resume per completed task.
The cancelled DeepLR implementation can resume per query if requested later. Every task retains
its configuration, predictions, metrics, timing, input hash and log. Failed tasks
remain explicit. They are not silently excluded from the comparison.

Metrics use inclusive bounds, first averaging queries within a task, then giving
equal weight to 128 tasks per stress regime, then equal weight to the 10 regimes.
Interval lengths remain in the original response scale. `aggregate.py` recomputes
metrics from saved predictions and only emits a method's plot-ready aggregate
when all 1,280 complete tasks are present. No existing plot point is replaced by
an incomplete result or an estimate of future experiments.

Remote work directory: `/home/kyle/Documents/lab/tabcon-ci-baselines-20261026`.
Local source: this directory. Raw data and run artifacts are ignored by Git.
