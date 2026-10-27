# Independent forest implementation audit — 2026-10-27

Scope: GRF, Local Linear Forest (LLF), RF-IJ, DRF and RF-U. This review directly inspected adapter source, saved outputs and the installed R implementations on Beast. It did not retrain models, change experiments, alter the frozen target, or use oracle outcomes to select settings. The only new file is this report.

Local paths below are relative to `talks/TabCon/experiments/ci_baselines/`. Remote paths are relative to `/home/kyle/Documents/lab/tabcon-ci-baselines-20261026/`.

## Verdicts

| Method | Verdict | Finding |
|---|---|---|
| GRF | PASS | Correct official `grf` regression-forest mean variance and normal CI; stock forest hyperparameters, not a tuned replication. |
| LLF | PASS | Correct official local-linear prediction and variance; ridge penalty selected by OOB error. Splits remain default CART; forest hyperparameters are not tuned. |
| RF-IJ | PASS | Correct official `ranger` infinitesimal-jackknife SE. The installed implementation includes its native bias correction and empirical-Bayes variance calibration. |
| DRF | PASS | Correct official uncertainty weights and conditional-mean functional. Sample variance across group means is correct; it must not be divided by the number of groups. |
| RF-U | WARN for the documented native-package benchmark; original raw-variance gate claim FAIL | Official RLT matched variance is used, but the package floors negative raw variances to zero before the adapter checks them. Documentation was corrected during this audit. Saved outputs include 4,040 zero-variance queries. |

PASS means implementation fidelity for the documented fixed configuration, not proof of finite-sample coverage or reproduction of a paper's optimized experiment. None of these five adapters substitutes a future-observation prediction interval for a mean-confidence interval.

## Priority finding: RF-U's package floor bypasses the promised retry

**[P1] The validation logic cannot detect native negative matched-variance estimates.** `modern_rfu.R:15–19` calls the official prediction function and tests the returned `pred$Variance >= 0`. In the pinned author source, `src/r-interface/RegUniForest.cpp:175–179` returns the mean over trees and dispatches `var_mode == 1` to `compute_matched_variance`. That function is defined in `src/include/core/Variance_IJ_Jack.h:136–156`; it computes `Var = Vh - Vs`, finds entries below zero, and replaces them with zero at lines 150–154. The header also contains IJ/jackknife implementations, but this particular branch is specifically **matched regression variance**.

The R wrapper's `clean.variance()` changes remaining negative values to NA, but receives values already floored in this C++ branch. Checking only the returned variance therefore cannot implement a retry on negative raw variance. At audit start, `PROTOCOL_MODERN.md:32` said there was no clipping and `MODERN_RUN_STATUS.md:20` said no negative-variance clipping was needed. Those were the original defective claims. `variance_attempts.json` reporting `invalid_queries: 0` is only evidence that the **post-floor** values were finite and nonnegative.

**Documentation correction verified during this audit:** the main agent updated `PROTOCOL_MODERN.md:32` and `MODERN_RUN_STATUS.md` to disclose the native floor, the 4,040 zero variances across 764 tasks, the inability to distinguish raw negatives from genuine zeros, and the fact that the retry observes returned values only. I re-read the corrected protocol. Runner, native library, configurations and results remain unchanged. Thus the reporting defect has been corrected; the historical raw-variance validation limitation remains.

Direct artifact checks found **4,040 / 155,520 zero standardized sampling variances (2.598%) across 764 / 1,280 RF-U tasks**. The same 4,040 queries have exactly zero original-unit interval width. Example: `runs/modern_full/rfu/asymmetric_extreme_outlier__000/inference_diagnostics.npz` has 12 zero variances among 128 queries. Zero values alone cannot distinguish a genuinely zero raw estimate from a negative value that the package floored; the existing saved diagnostics do not contain the individual tree predictions or pre-floor variance. Consequently this audit does **not** claim that every one of the 4,040 zeros was clipped or estimate what an alternative run's coverage would be.

This is an upstream behavior and an adapter/protocol discrepancy, not evidence that the author code was edited. Verified provenance:

- Pinned source commit: `d83a648a15591bbd4f057322dfdea7a75f056992`; installed package RLT 6.1.1.
- Archive SHA-256: `545a425422c418a39022429021c283f60c797d6809463b275d2cd3115c34f947`.
- All **148 archived files** match the extracted source byte-for-byte, with zero missing or changed files.
- Built `runtime_vendor/RLT-d83a648a15591bbd4f057322dfdea7a75f056992/src/RLT.so` and actually installed `rlib_modern/RLT/libs/RLT.so` have the identical SHA-256 `f1cebab1f02ac16ed3c9d9dfd82b8486b57854db837cb3296cb73f92ea5f4673`.
- Installed `RLT`, `predict.RLT`, `clean.variance` and `check_resamplepreset` have identical formals and deparsed bodies to those in the archive.

Official source links: [matched variance implementation](https://github.com/teazrq/RLT/blob/d83a648a15591bbd4f057322dfdea7a75f056992/src/include/core/Variance_IJ_Jack.h#L136-L156), [regression dispatch](https://github.com/teazrq/RLT/blob/d83a648a15591bbd4f057322dfdea7a75f056992/src/r-interface/RegUniForest.cpp#L175-L179), [author package](https://github.com/teazrq/RLT). The specific pinned pages were unavailable in the web tool's cache; the evidence above comes from the directly inspected archived source and installed library, not a cached web summary.

Minimal immediate fix, now applied to the protocol/status: describe RF-U explicitly as the native RLT matched-variance benchmark with the package's zero floor, disclose the zero count, and retract the claim that the saved run passed a raw-negative-variance gate. Preserve its saved metrics and mark the validation limitation. If the intended protocol really requires retries on raw negative estimates, a future separately authorized corrected run can request `keep.all=TRUE`, compute the native raw `Vh-Vs` from `PredictionAll`, compare the native returned variance to `pmax(raw,0)`, and apply the prespecified retry to the raw values. This does not require patching the author library. Existing post-floor diagnostic files cannot retroactively verify that gate. No such run was made in this audit.

## Implementation details and deviations from defaults

### GRF — PASS

`forest.R:13–15` calls `grf::regression_forest`; `forest.R:22–30` obtains `estimate.variance=TRUE`, checks finiteness/nonnegativity, and uses `mean ± qnorm(.975)*sqrt(variance.estimates)`. Installed grf is 2.6.1 on all 1,280 tasks. This is sampling variance for the fitted conditional mean, not the conditional variance of Y. The adapter does not add observation noise or divide again by the number of trees.

The actual installed function's defaults are 2,000 trees, sample fraction .5, `mtry=min(ceiling(sqrt(p)+20),p)`, minimum node size 5, honesty enabled, honesty fraction .5, pruning of empty honest leaves enabled, alpha .05, imbalance penalty 0, CI group size 2, and `tune.parameters="none"`. The adapter changes the random seed and uses one thread; the statistical settings are the package defaults. Half-sampling without replacement and the honest split are supported configurations for variance estimation. [Official regression API](https://grf-labs.github.io/grf/reference/regression_forest.html).

The official variance engine uses within/between-group quantities and native objective-Bayes debiasing, not merely the variance of tree predictions. Its output is used unchanged here. [Versioned author variance source](https://raw.githubusercontent.com/grf-labs/grf/v2.6.1/core/src/prediction/RegressionPredictionStrategy.cpp). There are 765 exactly zero saved variances; they are retained. They are not adapter-added floors.

Qualification: 2,000 is the stock tree count, not a demonstrated Monte Carlo convergence threshold. The author guide recommends checking excess error and potentially more trees for CIs; the adapter saves neither excess-error diagnostics nor a forest-size stability study. This is a limitation of the fixed baseline, not evidence that the API was misused. [Author algorithm guidance](https://grf-labs.github.io/grf/REFERENCE.html#variance-estimates). Minimal documentation improvement: say “official package defaults” rather than “tuned GRF” or “exact paper reproduction”; no numerical change is required by this audit.

### Local Linear Forest — PASS

`forest.R:16–18` calls `ll_regression_forest`; prediction at `forest.R:22` uses its own `predict.ll_regression_forest` method, confirmed from the installed namespace. Although default `enable.ll.split=FALSE` gives CART forest partitions, prediction still performs the official local weighted ridge regression. This is a supported local-linear-forest configuration, not ordinary GRF mislabeled LLF. [Official training API](https://grf-labs.github.io/grf/reference/ll_regression_forest.html).

Prediction defaults are all features in `linear.correction.variables`, `ll.weight.penalty=FALSE` and `ll.lambda=NULL`. The installed predictor calls `tune_ll_regression_forest`, evaluates a lambda path using out-of-bag predictions on context X/Y, chooses the lambda minimizing training OOB squared error, then predicts Xq with variance estimation. No query oracle enters the tuning routine. `forest_metadata.json` records the selected lambda repeated across query rows. The normal multiplier is applied to the returned **variance's square root** at `forest.R:26–30`. [Official prediction API](https://grf-labs.github.io/grf/reference/predict.ll_regression_forest.html).

Forest hyperparameters, including honesty and subsampling, have the same defaults as GRF, and forest-wide tuning is disabled. Thus only the local ridge penalty is tuned. No feature selection, experimental local-linear splitting, or full paper-experiment tuning was performed. There are 1,696 exactly zero saved native variances; all remain in the aggregate. Minimal fix is descriptive precision if broader tuning claims are made; no adapter bug was found.

### RF-IJ — PASS

`extra_methods.R:10–17` correctly fits a regression `ranger` forest with in-bag counts retained and asks `predict(...,type='se',se.method='infjack')`. Squaring the returned SE to obtain variance at line 16, then square-rooting once at lines 92–94, is algebraically correct. [Official prediction API](https://imbs-hl.github.io/ranger/reference/predict.ranger.html).

Installed ranger 0.18.0 uses 2,000 trees here versus its stock 500, `keep.inbag=TRUE` versus FALSE, one thread and a fixed task seed. Bootstrap replacement, fraction 1, regression minimum node size 5, variance splits, and `mtry=floor(sqrt(p))` are the native defaults. There is no honesty/sample-splitting option enabled and no hyperparameter tuning. The minimum-node parameter is a splitting threshold, not a guarantee that each terminal leaf contains five points. [Official fitting API](https://imbs-hl.github.io/ranger/reference/ranger.html).

Inspection of the actual installed `predict.ranger.forest` and `rInfJack` shows use of the native IJ covariance calculation, finite-tree bias correction, and default `calibrate=TRUE` empirical-Bayes calibration across query estimates. This calibration uses tree predictions and in-bag counts, not response/oracle coverage; it is an upstream stabilization, not an extra benchmark calibration step. All production tasks have at least 32 queries, so the function's query-count ≤20 skip condition does not apply. All 155,520 saved RF-IJ variances are positive. The adapter does not accidentally report raw per-tree variability or residual noise. Minimal fix: disclose the native calibrated IJ variant if describing the estimator more precisely than “ranger infjack”; no computational correction was found.

### DRF — PASS

`extra_methods.R:20–26` fits drf 1.3.1 and requests its native uncertainty weights. It uses 6,000 trees, 100 groups of 60, minimum node size 5, honest splitting with fraction .5, sampling fraction .5, FourierMMD with 10 features, and response scaling. Compared with the actual installed defaults, the changes are 6,000 versus 3,000 trees, node size 5 versus 15, and 100 versus 30 CI groups (default `ci.group.size=as.integer(num.trees/30)`). Other defaults include `mtry=min(ceiling(sqrt(p)+20),p)`, honesty pruning TRUE, alpha .05, imbalance penalty 0, node scaling FALSE, and a context-response median-heuristic kernel bandwidth. It is a fixed custom configuration using the native inference API, not an exact all-default or tuned paper replication.

`extra_methods.R:27–33` computes the conditional mean exactly as weights times the original context y, does the same within each uncertainty group, and takes sample variance across the resulting 100 means. The official inference documentation explicitly treats the group functionals as resampling estimates and uses their variance for a normal CI; **no division by 100 belongs here**. Using exact weighted means removes the extra sampling noise introduced by the manual's illustrative resampling approximation and is consistent with its functional definition. [Versioned CRAN author documentation/source](https://raw.githubusercontent.com/cran/drf/1.3.1/R/predict.R), [author repository](https://github.com/lorismichel/drf).

`run_extra_task.py:164–173` independently checks the group mean, sample variance and interval arithmetic. In this audit, all 1,280 retained remote `group_means.npz` arrays were independently rechecked against saved means and variances; every array has shape 100 × n_query and all checks passed. This is uncertainty of a mean functional, not `functional='sd'`, conditional response quantiles, or a prediction interval. No adapter bug was found.

### RF-U — native estimator fidelity PASS, validation/protocol FAIL

`modern_rfu.R:11–15` uses ordinary RLT regression, `reinforcement=FALSE`, `var.mode='matched'`, 10,000 trees, `mtry=max(1,floor(p/2))`, node size 5, half-sampling without replacement, and distributed importance. The matched mode's installed wrapper requires an even number of trees, forces the half-sample/no-replacement settings if needed, and enables distributed importance if absent. The adapter supplies those requirements correctly. This is matched-pair U-statistic variance, not RLT's separately available IJ mode.

The author `check_resamplepreset` and `src/r-interface/RBridge.cpp:35–58` generate disjoint paired samples of size floor(n/2); for odd n one observation is left outside a pair. The variance routine uses half the mean squared difference between paired tree predictions, minus the population variance across all trees, then the native floor described above. `run_modern_task.py:129–137` standardizes y using context mean/population SD and transforms mean, endpoints and SE back correctly. The native formula excludes future-observation noise; `qnorm(.975)` is used with its square root. [Pinned author RLT API](https://github.com/teazrq/RLT/blob/d83a648a15591bbd4f057322dfdea7a75f056992/R/RLT.r), [matched sampling](https://github.com/teazrq/RLT/blob/d83a648a15591bbd4f057322dfdea7a75f056992/src/r-interface/RBridge.cpp#L35-L58).

The base RLT defaults are 500 ordinary trees, sampling with replacement at fraction 1 and no variance mode. The benchmark's 10,000 matched trees are explicit inference choices, while mtry and node size retain defaults. No tuning is performed. All tasks used the first 10,000-tree attempt, but the absence of retries is not evidence of nonnegative pre-floor variance.

## Independent saved-output verification

For all five methods, this audit read every local config, metric and prediction file and compared task sets, input hashes against frozen metadata, production flags, complete query counts, finiteness, ordered endpoints, and recomputed coverage/width/RMSE. Each method has exactly **1,280 identical tasks / 155,520 queries**, exactly one statistical configuration after excluding task seeds and input hashes, and no truncated-query run in the result set. Launch source hashes match the current adapters, including the original `runs/full/launch.json` hashes for `forest.R` and `run_task.py`.

All 6,400 remote `predictions.csv` files were also read directly. Every CI matches its saved native variance and `qnorm(.975)`; the largest absolute half-width arithmetic difference was 1.11e-13 (CSV rounding). Package versions are uniform across every task: grf 2.6.1, ranger 0.18.0, drf 1.3.1, RLT 6.1.1. RF-U's standardized-to-original-unit transformations were additionally rechecked against local saved diagnostics. The following values were recomputed, not taken on trust from execution summaries:

| Method | Mean coverage | Mean interval length | Exactly zero native variance / width queries |
|---|---:|---:|---:|
| GRF | 0.54522705078125 | 0.719386408030377 | 765 |
| LLF | 0.6335113525390625 | 0.843499770719497 | 1,696 |
| RF-IJ | 0.53057861328125 | 0.726188893632815 | 0 |
| DRF | 0.5805023193359375 | 0.770346637431562 | 0 |
| RF-U | 0.6453704833984375 | 0.948954932552021 | 4,040 |

Each stress regime has 128 tasks, so the mean over these 1,280 task metrics equals the stated equal-regime aggregation. No normalization by a method's own scores was found. Fitting inputs contain X, y and Xq; the saved oracle is first loaded after predictions are saved (`run_task.py:195–204`, `run_extra_task.py:180–193`, `run_modern_task.py:137–146`). The review treats the frozen saved-oracle benchmark as given; it does not propose changing the DGP or target.

## Evidence limits and claim impact

No full model rerun, synthetic refit, or modification of author variance code was performed. The numerical checks use the already saved native outputs; they establish consistent arithmetic and complete pairing, not independent rederivation of every C++ estimator. For RLT the original archive, actual installed wrappers and installed shared library were directly linked as described above. For the CRAN packages the actual installed function bodies, package metadata and official author API/source were inspected; installed MD5 manifests were unavailable (`tools::checkMD5sums` returned NA), so this report does not claim a complete byte-for-byte CRAN binary provenance audit.

Supported claim: these are complete fixed-configuration evaluations through the named official packages, with correct mean-CI arithmetic. Unsupported claim: all methods are tuned reproductions of their papers. RF-U additionally cannot be described as having no clipping or having passed the promised raw-negative-variance retry gate. Its plotted number is reproducible from the saved native outputs, subject to that explicit limitation.
