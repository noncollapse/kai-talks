# Baseline implementation audit — 27 October 2026

**Overall verdict: WARN.** The retained results use the documented interval formulas and APIs; no CI/PI return swap, erroneous square root, double response rescaling, or fabricated result was found. However, they are **not all unmodified official implementations or strict reproductions of the papers' experiments**. The differences and unresolved evidence limits below must accompany the comparison.

The user removed Inferable EBM. Its diagnostic job never started after the interrupted launch, and no further EBM analysis was performed. Its original complete outputs remain archived. The opening slide now shows **14 methods**, without EBM or the broken x-axis. All four numeric source CSVs and every retained plot value are unchanged. AMP's label now explicitly says **AMP (CrI)**. No commit, push or publication.

## Independent reviews

Three separate Codex reviewers read the sources and artifacts directly:

- [Original six methods](evidence/audit_original_methods_20261027.md): historical production source/configuration, checkpoints, formulas and original numeric tables.
- [Five forest methods](evidence/audit_forest_methods_20261027.md): GRF, LLF, RF-IJ, DRF, RF-U; installed packages, native variance APIs and complete saved outputs.
- [BDE and BRAT](evidence/audit_bde_brat_20261027.md): author source, compatibility patches, training choices, CI arithmetic and exact original-data replays.

PASS below means fidelity to the specified implementation/configuration within the checks performed. It is not a coverage guarantee, full training-convergence certificate, or proof of exact historical environment reconstruction.

## Method-by-method result

| Method | Implementation / interval check | Differences and qualifications |
|---|---|---|
| Linear / HC3 | Formula PASS; numerical WARN | Custom NumPy HC3 with normal critical values. Context-only PCA in 330 tasks. Six recorded Linear replay coverage discrepancies on ill-conditioned designs. |
| RFF / HC3 | Formula PASS; numerical WARN | Custom Gaussian random features plus HC3, at most 64 features; context-based bandwidth and dimension restrictions. Shares the numerical sensitivity of the HC3 matrix calculation. |
| TabPFN (PI) | PASS | Official native predictive quantiles. This reference is a PI, as labelled, rather than a mean-CI procedure. |
| Bootstrap | PASS | Custom paired-row bootstrap around official TabPFN: 50 refits, eight estimators per refit, percentile interval of predicted means. Historical production source hashes verified. |
| AMP (CrI) | Paper-formula PASS; official-source comparison unresolved | Paper-based reimplementation of approximate martingale-posterior credible intervals. Probability-grid interpolation/clipping are approximations. Author-code URL returned HTTP 401; exact code equivalence cannot be certified. |
| TabCon | Inference/checkpoint PASS | Four checkpoint hashes and production inference source agree with the registry. Frozen heads and query-embedding router, Top-2 mixture, residual quantiles and response conversion verified. |
| GRF | PASS | Official grf 2.6.1 regression-forest mean variance, 2,000 trees and stock statistical settings. No forest-size convergence study or hyperparameter tuning. |
| Local Linear Forest | PASS | Official locally linear predictions/variance. Default CART partitions; only local ridge penalty is selected with context OOB error. It is not fully tuned LLF. |
| RF-IJ | PASS | Official ranger 0.18.0 IJ SE, 2,000 trees. Includes the package's native bias correction and empirical-Bayes variance calibration. |
| DRF | PASS | Official drf 1.3.1 uncertainty weights. Exact group-weighted means, sample variance across 100 groups, **without dividing by 100**. 6,000 trees, node size 5: explicit fixed choices rather than all defaults. |
| RF-U | Native implementation PASS; historical validation WARN | Official RLT matched variance includes an internal zero floor. The wrapper could not detect negative variances already floored upstream. Prior “no clipping” assertion corrected. |
| BDE | Adapter/formula PASS; training/provenance WARN | Author ensemble, parametric bootstrap and Student-t CI. Documented compatibility fixes preserve Adam checkpoint state. One reproducible extreme variance-head fit remains. Seventeen early diagnostic archives have float32 precision without a separate format version. |
| BRAT-P | Adapter/formula PASS; protocol WARN | Pinned official package and README configuration. Current package initialization/inference differs from paper experiments; training-residual variance used instead of the preferred held-out estimator. |
| BRAT-D | Adapter/formula PASS; protocol WARN | Pinned official package and README configuration; signal/SE correction applied once. Same training-residual variance limitation. |

## Corrections made

1. **RF-U reporting:** corrected `PROTOCOL_MODERN.md`, `MODERN_RUN_STATUS.md` and speaker notes. RLT floors negative matched-sample variance internally. Saved results contain **4,040 zero-width intervals across 764 tasks** (2.598% of queries). The saved zeros cannot distinguish genuine zeros from negative pre-floor estimates. The historical “retry on raw negative variance” guarantee was not satisfied by inspecting returned values alone. No data were clipped or recomputed during this audit.
2. **BRAT scope:** documented that official-package execution is not exact paper-experiment reproduction. In addition to fixed README hyperparameters, BRAT-P skips the paper's sequential warm-start; current package inference uses histogram-cell calculations rather than the paper experiment's Nyström approximation. Both methods use the documented training-residual variance fallback. It can underestimate noise after fitting; results cannot be described as reproducing the paper's held-out variance procedure.
3. **Original-method descriptions:** made Linear/RFF's custom implementation and numerical limitations explicit; labelled AMP as a credible interval and documented the unavailable author-code comparison. Bootstrap is correctly identified from the production B50/E8 source, not a different current local E=1 copy.
4. **Display:** EBM excluded, continuous log x-axis restored, 14-method count and notes updated, labels repositioned and localhost preview visually checked. All retained numerical points are unchanged.

## Verification performed

- Every saved task output for the eight additional retained baselines was checked: **10,240 task results / 1,244,160 query intervals**, each method using the same 1,280 tasks and 155,520 queries. Configurations, input hashes, complete query counts, means, SE/variance, response transforms, endpoints and recomputed metrics agree. DRF's 1,280 group-mean matrices were independently checked.
- **Eight BRAT exact replays** (four original tasks per method) match saved means, influence norms and residual variances bitwise. Endpoints match at 1e-12 tolerance. Reconstructed training trajectories are finite; no persistent explosive fit was found in these replays. This does not certify every unrecorded historical training trajectory.
- BDE's authoritative endpoints reconstruct at 1e-12 even for the 17 float32 diagnostic archives. Their auxiliary variance values have rounding differences up to 2.984e-5 relative. The extreme run's checkpoints preserve optimizer state and its stored diagnostic replay reproduces the anomaly. It was not removed or replaced with a favourable seed.
- Original numeric source: **693 scalar values** (including the archived control regime and Global ablation) match the frozen summaries exactly; raw episode aggregates were independently recomputed. Only the specified ten regimes and six original methods enter the figure.
- Production main evaluation source/runner and four TabCon checkpoint hashes match the original registry. The original benchmark inputs were deterministically reconstructed and numerically checked; historical raw input arrays were not retained, so this is not a historical raw-array byte comparison.
- [Display/data-preservation check](evidence/ebm_display_removal_20261027.json) confirms the source CSV hashes and unchanged retained means. Preview: http://localhost:3031/#/first-results.

## Remaining limitations and appropriate next work

- **RF-U:** checking raw-negative variances would require a separately versioned rerun retaining individual tree predictions and computing the author's pre-floor matched variance. The current saved outputs cannot retrospectively establish that check. They do faithfully retain native RLT outputs.
- **Linear/RFF:** the HC3 mathematics is correct, but forming inverse-Gram covariance products is fragile. The original-method report provides an algebraically equivalent SVD influence calculation with the same rank cutoff, clipping and basis/seed rules. A separately identified recomputation should precede replacing the historical values. The nominal minimum residual df of eight also has an explicit df-seven exception on n=9 tasks.
- **AMP:** paper equations were checked, but official source remains inaccessible. Its label and provenance must remain “paper-based reimplementation / credible interval.” [The author's paper](https://arxiv.org/html/2505.11325v4#S3.SS6) explicitly describes the approximate posterior construction.
- **BDE and training provenance:** future runs should store immutable per-task source hashes and version diagnostic formats. Finite endpoints alone must not be labelled converged training. No such universal claim is made here.
- **BRAT variance:** a held-out or cross-fitted estimator would be a new declared training-only protocol, not a post-hoc multiplier selected using achieved coverage. This audit does not substitute one into the historical benchmark.

The frozen dataset and evaluation target were preserved throughout; no DGP change, oracle-based fitting, outcome-based parameter selection or removal of difficult tasks was performed. BART, GP and DeepLR remain cancelled.
