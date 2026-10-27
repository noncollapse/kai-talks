# Independent audit of the original six methods — 27 October 2026

Scope: Linear/Wald HC3, RFF/Wald HC3, native TabPFN PI, Bootstrap, AMP, and TabCon. Read-only source, configuration, checkpoint, and saved-result review; no full experiments or changes to results. PASS means the inspected implementation and saved-result lineage agree, not a coverage guarantee. The original DGP and saved oracle are taken as given.

## Verdicts

| Method | Verdict | Implementation and smallest action |
|---|---|---|
| Linear / Wald HC3 | **WARN** | The HC3 sandwich and normal-Wald interval formula are correct, but this is a custom NumPy implementation with context-only PCA in 330/1,280 tasks. Its matrix products are numerically fragile on ill-conditioned designs. Document PCA, z critical values, and the six known replay discrepancies; use the stable SVD formula below for a separately versioned correction. |
| RFF / Wald HC3 | **WARN** | Correct Gaussian random-feature map followed by the same custom HC3/z calculation. The 64 features are a cap, with context-only dimensionality/sample-size restrictions and median-distance bandwidth. Shares Linear's numerical issue and the small-sample residual-df exception. No official RFF CI package is being run. |
| TabPFN (PI) | **PASS**, with target qualification | Calls the official TabPFN V3 regressor's predictive quantiles. It is a prediction interval, assessed here against the common saved oracle, and should remain explicitly labelled PI. |
| Bootstrap | **PASS** | The actual plotted run uses 50 paired context-row resamples, **8 TabPFN estimators per refit**, and percentile quantiles of the predicted means. This is a custom bootstrap wrapper around official TabPFN, not a separate author baseline package. |
| AMP | **WARN** | The inspected custom implementation agrees with the cited AMP paper's update, learning-rate correction, and empirical-mean summary. Official author-source equivalence was **not established**: the paper's anonymous repository was inaccessible; the coordinating audit's direct HTTP request returned 401. Label as a paper-based reimplementation. Its native interpretation is an approximate martingale-posterior **credible interval**, a classification issue rather than an implementation error. |
| TabCon | **PASS** for inference and checkpoint lineage | Uses the authors' frozen source/shrink/expand heads and embedding-only task router, mixing exactly two expert distributions before extracting residual quantiles. All four checkpoint hashes match the original registry. No query oracle enters the prediction path. |

## Exact sources and execution lineage

Path abbreviations used below:

- `P` = `/Users/kyle/Library/CloudStorage/OneDrive-LondonSchoolofEconomics/writting papers/TRM_codex/Tabpfn_ci_PriorV3/implementation`
- `R` = Beast `/home/kyle/Documents/lab/tabpfn-epihead-prior-v3`
- `E` = `R/results/bootstrap_corrected_eval/bootstrap_b50_e8_ci99_selected_seed0_20260918_124652`
- `W` = `P/experiments/wald_baselines/common.py`
- `C` = `R/experiments/final_comparable_eval/common.py`
- `T` = current teaching workspace `/Users/kyle/Library/CloudStorage/OneDrive-LondonSchoolofEconomics/teaching/llm_short_course`

The **remote production** `C` has SHA256 `65c0e975791f3e829624f07f7b0fecd3a79f4dd28499048ddd7123c39bcd10e2`, exactly matching `E/protocol.json`. The remote production runner `experiments/tabpfn_ci_paper_eval/run_bootstrap_b50_selected.py` has SHA256 `738b1ba05043709650f5b4743a3a473aec42a0ccee787b225056fa56e77c22c7`, also matching that protocol. Therefore the stale local `P/experiments/final_comparable_eval/common.py`—whose bootstrap uses E=1—is **not** evidence about the plotted E=8 run.

`E/stress/run_config.json:2,11,19–20` records B=50, 128 episodes per regime, E=8, seed 770001. The runner passes those values to the stress program at lines 133–145 and 269–278. `C:1633–1648` passes the evaluator's actual ensemble count to Bootstrap.

The checked remote TabPFN checkout identifies official origin `https://github.com/PriorLabs/TabPFN.git`, commit `cafab9846ae8a8a68b55625fd8a75421360d40fd`, package version 8.0.8. Git reports no modifications to the official regression/core files. Its tracked modification only adds EpiHead exports in `src/tabpfn/__init__.py`; `epihead.py` and its test are added project files. This establishes the inspected source's origin; it is not an immutable historical environment capture.

## Method checks

**Linear and RFF.** `W:307–384` fits median imputation, numeric scaling and reference-coded categories to context only; `W:387–412` removes constant columns and applies context-only rank-adaptive PCA for Linear. `W:415–429,479–506` constructs RFF frequencies with standard deviation `1 / bandwidth`, uniform phases, and `sqrt(2/m)` cosine scaling. Bandwidth uses only context distances. Feature count is capped at 64 and additionally by context size and encoded dimension.

`W:572–596` computes HC3 weights `e_i²/(1-h_i)²`, the sandwich covariance, and `center + norm.ppf(level) * se`. No observation-noise variance is added. The mathematical sandwich agrees with [official statsmodels HC3 documentation](https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLSResults.HC3_se.html). These are **z**, not Student-t, intervals; that is consistent with the stated Wald construction and should not be silently changed.

Two concrete limitations remain:

1. `W:406,481` forces at least one slope even when `n=9`. Saved raw metrics show residual df **7**, not 8, for episode 29 in all ten plotted regimes for both methods. If eight df is intended as a strict contract, allow an intercept-only basis for these tasks. Otherwise describe the parameter as a target with this explicit exception.
2. `W:532–535,572–591` constructs the inverse Gram matrix, uses it for coefficients and leverage, and multiplies the covariance sandwich. Maximum saved design condition numbers are about 3.08e7 (Linear) and 9.51e7 (RFF); 54 and 11 respective tasks exceed 1e6. The saved replay evidence already lists six Linear coverage mismatches and maximum width difference 0.05688837 (`T/talks/TabCon/experiments/ci_baselines/evidence/data-alignment.json:26–33`). A read-only diagnostic on those six existing inputs confirmed sensitivity: replacing the products with the equivalent stable SVD calculation changed current-backend coverage for `near_zero__038` from 0.96875 to 0.984375 and `heteroscedastic__127` from 0.75 to 0.734375. These are diagnostic values, not replacements for historical results.

The smallest numerical repair is to retain the same SVD rank cutoff and compute `Xplus = V diag(1/s) U.T`, `beta = Xplus @ y`, `h = row_sum(U**2)`, and query variance `sum_i [((Xq @ Xplus)[q,i] * e_i / max(1-h_i, 1e-8))**2]` (sum of squared influences). This avoids forming and subtracting ill-conditioned covariance products while preserving the statistical formula. Corrected results require a separately identified recomputation; do not overwrite the frozen historical values merely to improve agreement.

This is a **numerical robustness/replay warning**, not evidence that the HC3 statistical formula is wrong. There is no ridge penalty. Preserve the exact cutoff `s > max(max(X.shape)*float64_eps*max(s[0],1), 1e-8*max(s[0],1))`, leverage clipping to `[0,1]`, and denominator floor `max(1-h,1e-8)` (`W:516–537,575`). Historical values remain valid records of what that implementation computed.

A CPU-only equivalent-calculation audit is feasible without retraining: use frozen files under Beast `/home/kyle/Documents/lab/tabcon-ci-baselines-20261026/data/<task>/` (`raw.pkl`, `inputs.npz`, `oracle.npy`, `metadata.json`). Historical basis matrices were not located; reconstruct them with `PreparedWaldDesign.prepare`, the same projection/bandwidth/basis caps, and **nested seed** `stable_seed(stable_seed("stress", stress, episode_seed), method)` (`W:1359–1368`; `experiments/wald_baselines/eval_stress.py:73`). Save and use the same reconstructed design for old/stable numerical calculations. Existing `/home/kyle/miniconda3/envs/tabpfn_epihead` has the original import stack; the CI-baselines venv already has NumPy/SciPy for a standalone equivalent formula. Recorded original times across the 1,280 plotted tasks total 14.75 seconds Linear and 17.67 seconds RFF; a complete audit should be on the order of minutes with I/O, not GPU training. This is an estimate from historical timing, not a measured new full run. Changing z to t, changing the basis, or enforcing df=8 would change the statistical procedure and must be considered separately.

**Native TabPFN.** `C:98–113` selects `ModelVersion.V3`, E=8 from the run, disables automatic estimator scaling, and uses `fit_preprocessors`. `C:193–211` fits observed context outcomes and calls native `predict(..., output_type="quantiles")`. The displayed 95% interval is the native 0.025/0.975 predictive quantile pair. The existing slide's PI label and target qualification are appropriate (`T/talks/TabCon/slides.md:42`).

**Bootstrap.** `C:1343–1364` samples n paired rows with replacement, changes the algorithm seed by repeat as explicitly recorded in `E/protocol.json`, refits TabPFN with eight estimators, extracts `output_type="mean"`, and takes pointwise empirical percentiles. It does not bootstrap noisy future outcomes or mistake an ensemble standard deviation for a CI. Loaded checkpoint reuse (`R/experiments/tabpfn_runtime.py:9–24`) reuses official modules while each resample is still fitted. B=50 limits tail-quantile precision, especially at 99%; it is the reported configuration, not a formula error.

**AMP.** `R/experiments/martingale_posterior_baseline.py` is byte-identical to the inspected local version (SHA256 `6451c227b127690ada96abd84dadd8e481816a6286c6dfc1939c61fe7a79ac8b`). Lines 47–64 implement the finite-N learning-rate correction; 108–160 initialize native predictive quantiles and perform the Gaussian-copula updates; 162–163 return the mean of each chain's forward labels. `C:1367–1392` extracts percentile intervals from those mean draws. Saved raw rows independently confirm B=50, N=50, rho=.99, grid=512. These components match Algorithm 1 and equations (2), (4) in [Nagler and Rügamer, arXiv:2505.11325v4](https://arxiv.org/html/2505.11325v4#S3.SS6). The 512-point probability grid, interpolation, tail clipping and monotonicity enforcement are implementation approximations. The same paper describes approximate Bayesian posterior inference and credible intervals; do not relabel AMP as an ordinary frequentist confidence-interval method. The paper links [author code](https://anonymous.4open.science/r/UQ_for_PFNs), but exact source comparison was unavailable in this audit. No removal of AMP is recommended or performed by this report.

**TabCon.** `C:762–809` freezes and loads the three heads plus router. `C:858–879` builds inference features with a zero placeholder target; `C:915–955` routes using query embeddings and mixes probabilities from exactly two active experts; `C:972–985` transforms residual quantiles to original response units. The oracle is first read at `C:987–998` for NLL after quantiles have been constructed. `R/TabPFN/src/tabpfn/epihead.py:262–268` fits and scales from context only.

The source, shrink, expand and router SHA256 values independently match `E/registry/selected_systems.json`: `b723a2ae…`, `1f15c655…`, `3088ea2d…`, `a17377be…`. The router configuration records exact top-2, embedding-only inputs, and best checkpoint step 37500. Training configuration uses E=2; final inference uses E=8. This is a recorded train/evaluation difference, not an undisclosed substitution.

The checked router training source constructs separate training and validation streams (`R/experiments/difficulty_moe_continuous_router/train.py:676–690`), with validation seed 409000033, distinct from stress seed 770001. Checkpoint selection uses that validation stream and its predefined coverage/CVaR criterion (`:1282–1349`). No test-oracle tuning is present in the inspected inference code. This review does not prove that no historical design decision was informed by benchmark results; such a claim would require a full development-history audit.

## Saved values and pairing

Scalar plot provenance: **PASS**. Fresh numerical rerun equivalence: **WARN**, specifically the documented ill-conditioned Linear tasks and incomplete historical raw-array preservation.

- Independently checked the copied CSV SHA256 `bb70b7690ca1913eae2f3c916a782ddab4813b4e0421cad5548b3b8d644bd06f` and **all 693 metric values** against the two frozen summary JSONs: exact agreement.
- Recomputed 495 main-method aggregate metrics from all 7,040 remote per-episode rows and 198 Wald aggregate metrics from all 2,816 local per-episode rows: no mismatch at 1e-12 tolerance. Each method/regime has 128 episodes. The extra control regime and Global ablation are intentionally excluded by `T/talks/TabCon/figures/scripts/draw_stress_preview.py:24–37`.
- Remote main summary SHA256 `7bc91fb193f9175c7938aa9a2615a55aa9a7c5f994d2249deb834a3ccf5e8b5f` exactly matches the local frozen summary. Metric code uses inclusive bounds and averages query metrics within each episode (`W:126–138`; native analogue `C`'s `metrics_from_quantiles`).
- Reconstruction validates generator hash, episode seeds/dimensions and Linear point RMSE; the separate RFF replay is recorded in `data-alignment.json`. Historical raw arrays were not retained, so numerical replay is not a historical byte-hash proof. `prepare_tasks.py:74–79` explicitly does not require original Linear interval equality, consistent with the numerical warning above.

No evidence of fabricated values, oracle use in predictions, hidden observation-noise addition to the mean-interval baselines, or incorrect B50/E8 attribution was found. An unqualified statement that all six are unmodified official implementations, or all six are frequentist CIs, would be incorrect.
