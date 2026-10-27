# Independent audit: BDE, BRAT-P and BRAT-D

Date: 2026-10-27. Scope: the three named methods only. Read-only review of original artifacts and official source, plus eight deterministic BRAT diagnostic fits on unchanged original input arrays. Diagnostic files were written only under `/tmp`; production data, predictions, checkpoints and configurations were not changed. No oracle-based tuning was performed. EBM was not investigated.

All relative paths below start at `talks/TabCon/experiments/ci_baselines/`. `BV` denotes the pinned official source directory on beast: `/home/kyle/Documents/lab/tabcon-ci-baselines-20261026/runtime_vendor/Boulevard-ec0a4ede4155519b70fbca65ac73f9ece64da276`.

## Verdicts

| Method | Official implementation / adapter | Overall | Reason for qualification |
|---|---|---|---|
| BDE | PASS for current source, documented patches, configuration, bootstrap and CI calculations | WARN | Reproducible finite variance-head instability in one run; 17 early diagnostic archives have an unversioned precision difference and incomplete historical source provenance. |
| BRAT-P | PASS for pinned author package, README settings, return ordering and signal CI calculation | WARN | Training-residual variance replaces the held-out variance estimation used in the README example and paper experiments. README initialization also differs from the paper's sequential warm-start. Original training histories were not retained. |
| BRAT-D | PASS for pinned author package, README settings, signal correction and CI calculation | WARN | Same training-residual variance choice; original training histories were not retained. No persistent explosive training was found in the checked replays. |

No wrong return tuple, CI/PI substitution, missing factor of ensemble size, double response scaling, or accidental omission of a required *CI* observation-noise term was found. An additional observation-noise term would produce prediction intervals and would change the requested interval type.

## Independently checked saved results

I opened every production configuration, prediction archive, relevant diagnostic archive, metric record and paired input archive for these methods. All three have one common non-seed/non-input-hash configuration, 1,280 complete production tasks and 155,520 queries. Every input hash matches the recorded frozen input hash; query counts match. All authoritative endpoints are finite and ordered.

Reconstructed means and endpoints match at `rtol=1e-12, atol=1e-12`; coverage, length and RMSE independently recompute from saved predictions. The BRAT check recomputes context response statistics **after converting the saved responses to float64**, as the adapter does (`run_modern_task.py:116`, `:129`). Computing these statistics in the saved input's float32 dtype would instead create an audit-side rounding discrepancy.

| Method | Recomputed mean coverage | Recomputed mean length |
|---|---:|---:|
| BDE | 0.77291259765625 | 14.767485732214302 |
| BRAT-P | 0.1536224365234375 | 0.2074908501043721 |
| BRAT-D | 0.2644775390625 | 0.2666031319457618 |

These are equal-weight task means; each regime contains 128 tasks, so they equal the declared task-then-regime aggregation. Evidence: `aggregate.py:26`, `:35`; `evidence/modern_completion_verification.json:4`, `:20`. The audit script and numerical summary are temporarily retained at `/tmp/audit_bde_brat_arrays.py` and `/tmp/audit_bde_brat_all_arrays.json` on the local machine.

## BDE

### Source and compatibility changes: PASS, with historical provenance limitation

The five deployed vendor files were compared byte-for-byte against the official GitHub files at commit `e4044b29ab80eac8036e7adbaf12ba42b42ba9c0`; all match. The deployed runtime copies exactly equal the vendor files after applying the recorded replacements, with no additional runtime change found. The current local and remote adapter hashes match `runs/full/launch.json:19` and `evidence/bde-audit.json:80`.

Changes in `patch_vendor.py:8` are explicit compatibility changes: remove the unused obsolete `merge` import; replace removed `np.int`; silence prediction progress; and change both checkpoint save/load paths to native `.keras`. The last is behaviorally important: it restores the optimizer state that the author's algorithm requires, rather than deliberately resetting it. It is not an unchanged-file reproduction.

An independent remote read of all five original `high_noise__053` checkpoints confirmed 1,736 optimizer iterations, 17 optimizer variables, and bitwise equality of weights and optimizer variables with the existing exact diagnostic replay. Original checkpoint bytes were unchanged. The iteration count is `56 * ceil(976/32)`. Evidence: `run_task.py:117`; `vendor/bde/neural_networks.py:223`; the recorded hashes in `evidence/bde-audit.json:42` match the independent reads. This audit did not reload every checkpoint from every task.

### Parameters, training and bootstrap: PASS

The actual configuration is five ensemble members; hidden widths 40/30/20; ReLU hidden layers; two linear outputs; 80 epochs; checkpoint after 56; 24 bootstrap epochs; Adam; batch size 32; hidden-layer kernel L2 coefficient `1/n`; output standard deviation `exp(log_sigma)+1e-3`. These match the author paper's Section 4.2 and the implementation, not merely the function's shorter defaults. See `run_task.py:70`, `:114`; `vendor/bde/neural_networks.py:358`, `:389`, `:439`, `:475`; [author paper, Section 4.2](https://arxiv.org/pdf/2202.10903).

`gen_deep_ensemble` reshuffles the same context without replacement, with paired X/y ordering and independent initialization. The parametric bootstrap keeps X fixed and samples new targets from each fully trained member's Gaussian mean and standard deviation. It resumes that member's 56-epoch checkpoint, including Adam, for the final 24 epochs. There is no observation-row bootstrap, ensemble averaging before target simulation, or restart from random weights. Re-estimating the bootstrap target normalization follows the upstream `ExtraTrainedNetwork` implementation exactly. See `vendor/bde/neural_networks.py:499`, `:512`, `:213`.

Context encoding and dropping constant input columns are benchmark adapters (`run_task.py:68`; `PROTOCOL.md:34`), while the neural network's own context normalization remains active. No oracle is loaded until after prediction generation (`run_task.py:195`).

### CI calculation and scaling: PASS

The author returns `(PI, CI)` and the adapter retains the second object (`run_task.py:129`; `vendor/bde/intervals.py:84`, `:125`). For each query it is

`mean(member) ± t_(.975,4) * sqrt(mean((member - bootstrap_member)^2) + sample_var(member)/5)`.

The bootstrap difference term is **not** divided by five again. Observation noise enters the bootstrap target draws; it is not added directly to the final signal variance. `N_samples=2` affects only the discarded PI simulation after the CI has already been computed (`vendor/bde/intervals.py:100`, `:109`). The f/sigma methods already invert response normalization, so the adapter correctly applies no additional response transform.

### Finite training instability: WARN

For `high_noise__053`, the existing replay's saved means, bootstrap means and variance independently match the production archive bitwise. The main predictor remains ordinary in scale, but base member 1 produces a maximum context sigma of **16,264,385**, and its simulated bootstrap targets have standard deviation **188,335.34**. That bootstrap member reaches a context mean magnitude of **551,011.19**. This occurs before CI assembly. Evidence: `runs/audit/bde_high_noise_053_seed_0/diagnostics.json:35893`, `:36102`, `:36119`; production length **16,948.60** at `runs/full/bde/high_noise__053/metrics.json:11`.

The loss and outputs can remain finite while the variance head becomes pathological; endpoint-finiteness checks do not establish a stable fit. This is a reproducible result of the deployed author training procedure, not evidence of incorrect CI algebra or a response-scale conversion bug. The known sensitivity runs are diagnostic only (`diagnose_bde.py:67`, `:150`); no clipped or different-seed result replaced production. Other runs' full internal training trajectories cannot be certified because they were not all retained. The benchmark and its inputs need no reinterpretation to identify this numerical issue.

### Diagnostic precision / provenance: WARN

Exactly **17** `members.npz` files store `means`, `bootstrap_means` and `variance` as float32; the other **1,263** store float64. All declare `adapter_version=3`, while the current adapter explicitly requests float64 (`run_task.py:135`; representative older config `runs/full/bde/asymmetric_extreme_outlier__000/config.json:8`). The older files are:

`asymmetric_extreme_outlier__000`, `asymmetric_extreme_outlier__001`, `bounded__000`, `bounded__002`, `categorical_missing__000`, `discontinuous__000`, `discontinuous__001`, `discontinuous__002`, `heavy_tail_noise__000`, `heteroscedastic__000`, `high_noise__000`, `near_constant__000`, `near_constant__001`, `near_constant__002`, `near_zero__000`, `quantized__000`, `quantized__002`.

Casting the saved members to float64 before subtraction/averaging reproduces **every authoritative endpoint** within `1e-12`. The float32 diagnostic variance itself differs from that reconstruction by at most **2.984e-5 relative**. Thus the stored diagnostic variance is not always an exact representation of the variance used by the author's CI return; no affected authoritative result was found.

The first-batch launcher records only the current launch source hashes, overwrites the launch snapshot on restart, and resumes already-finished tasks (`launch_suite.py:25`, `:63`, `:68`). It does not preserve per-task source bytes/hashes. Consequently current source identity is verified, but an exact historical source identity claim for all 1,280 BDE tasks is not independently established. Preserve the originals; version this diagnostic-format change and retain per-task source provenance in future runs.

## BRAT-P and BRAT-D

### Installed author source and parameters: PASS

All ten installed Boulevard Python files exactly match the pinned extracted source. The relevant source files and README also match newly fetched official GitHub bytes at commit `ec0a4ede4155519b70fbca65ac73f9ece64da276`. Installed package version is `0.1.0a1`, with scikit-learn `1.8.0`. No package patch was found. Adapter source hashes match the launch record (`runs/modern_full/bratp/launch.json:34`).

The production BRAT-P settings exactly match the [pinned README example](https://github.com/boosting-inference/Boulevard/blob/ec0a4ede4155519b70fbca65ac73f9ece64da276/README.md#parallelbooster): 70 rounds × 6 trees, subsample .8, depth 8, 64 leaves, minimum leaf 4, 64 bins, `drop_first_round=True`, one job. BRAT-D exactly matches its README example: 700 trees, learning rate .8, dropout .1, subsample .8, depth 6, 64 leaves, minimum leaf 2, 64 bins. Only the deterministic task-specific seed replaces the example seed. Evidence: `run_modern_task.py:37`; `BV/README.md:184`, `:226`.

These are maintained author-package examples, **not an exact reproduction of the paper experiments**. BRAT-P's README setting skips the sequential first-round warm-start shown in paper Algorithm 2 (`BV/src/boulevard/estimators/sklearn/parallel.py:778`). The package computes a histogram-cell kernel and direct linear solves (`parallel.py:886`; `dropout.py:701`), whereas the paper experiments use Nyström approximation. The paper experiments also have distinct per-experiment or tuned settings. See [author paper, Algorithms 1–2 and Sections 4/6](https://papers.neurips.cc/paper_files/paper/2025/file/2f383b17f62bb308b50f20b4e679c9de-Paper-Conference.pdf).

### Signal CI, variance and transforms: PASS for implementation; WARN for variance-estimation choice

The adapter reads `(lower, upper, mean)` in the correct order, explicitly selects `mode='confidence'`, and verifies the returned mean against `predict` (`run_modern_task.py:57`). BRAT-P uses `SE=sigma_hat*weight_norm`. BRAT-D uses `SE=2.15*sigma_hat*weight_norm`, where `2.15=(1+.8*(1-.1))/.8`. Its `predict` already applies its own signal correction; the adapter does not apply the correction to the mean again. Source: `BV/.../dropout.py:259`, `:387`; `BV/.../parallel.py:459`; adapter `run_modern_task.py:64`.

Both confidence formulas exclude the additive observation variance present in the package's prediction-interval branch. The saved weight norms are raw influence norms; multiplying by 2.15 once for BRAT-D's SE is required. The final inversion multiplies means/endpoints/SE by context `y_sd` once and adds `y_mean` only to location quantities (`run_modern_task.py:129`). All saved endpoints independently pass this calculation.

`prepare_inference()` without arguments uses centered **training** residual variance with `ddof=1`, exactly as the source implements (`dropout.py:307`, `:326`; `parallel.py:379`, `:398`). The adapter verifies this (`run_modern_task.py:61`). This is an officially supported fallback but differs from the README example and paper Section 6, which use a held-out set for noise estimation. It can substantially underestimate residual noise after fitting; therefore the observed undercoverage cannot be advertised as a controlled reproduction of that held-out procedure. The choice is already declared in `PROTOCOL_MODERN.md:30`. No held-out set, oracle residual, PI calibration or width inflation was secretly applied.

### Training and numerical checks: PASS for checked fits; WARN for incomplete historical diagnostics

All 1,280 saved standardized residual variances are finite, positive and below one for each method:

| Diagnostic | BRAT-P | BRAT-D |
|---|---:|---:|
| Minimum residual variance | 1.3441e-8 | 1.6534e-7 |
| Median residual variance | 0.0151685 | 0.0698101 |
| Maximum residual variance | 0.918791 | 0.936039 |
| Maximum absolute standardized query mean | 9.39808 | 10.47208 |

The maximum variance is at `categorical_missing__030` for both methods; see its respective `fit_diagnostics.json:6`. There is no explosive final residual-variance signature. Small residual variance is evidence about the fitted training residuals, not proof of correctly estimated noise.

Eight new deterministic diagnostic fits used unchanged original arrays, seeds and full production parameters: four tasks per method. Saved standardized query means, weight norms and residual variances match **bitwise**; back-transformed endpoints match at `1e-12`. The cached per-tree training predictions were used to reconstruct every BRAT-D iteration and every completed BRAT-P round without changing training. All cached tree values and all reconstructed training predictions are finite.

| Task | n / p | BRAT-P final training MSE | BRAT-D final training MSE |
|---|---:|---:|---:|
| near_constant__029 | 9 / 130 | 0.012882 | 0.094804 |
| categorical_missing__099 | 95 / 409 | 0.007722 | 0.059569 |
| high_noise__053 | 976 / 48 | 0.035161 | 0.266073 |
| near_zero__103 | 1,035 / 16 | 0.105706 | 0.084425 |

BRAT-P has an early overshoot under `drop_first_round=True`: maximum early training MSE 16.0–34.8 across these four fits, followed by bounded final training. BRAT-D stays bounded throughout these replays. Some training curves are nonmonotonic, so this is not a claim of convergence to a particular optimization tolerance. No persistent explosive failure or adapter corruption was found. Temporary replay evidence is at `/tmp/audit_bde_brat_replays_20261027.json` on both machines.

The original fitters used `verbose=0`; the package discards `train_score_` in this mode (`dropout.py:231`, `:237`; `parallel.py:302`, `:308`). The adapter saves residual variance/inference diagnostics but no training curve or model checkpoint, then writes `quality_passed=True` after finite-output checks (`run_modern_task.py:77`, `:148`). This field certifies the implemented gates, not numerical convergence of every historical fit. Future runs should save training diagnostics and name the flag accordingly.

## Concrete follow-up

1. Keep authoritative saved results unchanged. No correction to the three interval formulas or return ordering is supported by this audit.
2. Label BDE's extreme-width outcome as a reproducible finite training instability; do not present finite endpoints as a stable-fit certificate. Any stabilized method should be a separately declared experiment, not a replacement selected by coverage.
3. Describe BRAT results as the pinned author package with fixed README parameters and training-residual noise estimation. Do not call them a strict recreation of the paper's held-out noise-estimation experiments. A held-out or cross-fitted alternative would require a separate, predeclared training-only protocol; it is not a post-hoc width correction.
4. Record source/diagnostic-format hashes per task and retain immutable launch snapshots. Specifically disclose the 17 BDE float32 diagnostic archives; retain their original bytes.
5. Preserve training-trajectory diagnostics in future runs and distinguish a finite-output gate from a convergence claim. The checked BRAT runs do not justify a finding of numerical divergence across the method.
