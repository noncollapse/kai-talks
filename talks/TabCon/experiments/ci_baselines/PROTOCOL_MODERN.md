# BRAT-P, BRAT-D, RF-U and Inferable EBM

Authorized 2026-10-27. Local results and slide updates only; no commit, push or publication.

## Frozen paired evaluation

Reuse the existing 1,280 tasks and all 155,520 queries, with identical context arrays, query arrays, stored oracle and original context-only encoding. No regeneration or subsampling of tasks/queries. Manifest SHA-256: `e0c6d45113f315dee8f0b8943e83710b46c57f45e81feb0f9686fcbe07dd39b3`.

Each task validates its input hash. Responses are centered and scaled using context responses only, then predictions and interval endpoints are transformed back. Fitters receive X, y and Xq only; the evaluator opens the oracle only after intervals have been saved. Existing original-six, GRF/LLF/BDE, and RF-IJ/DRF results remain unchanged. BART, GP and DeepLR remain cancelled.

## Author implementations

- BRAT-P / BRAT-D: [Boulevard](https://github.com/boosting-inference/Boulevard), commit `ec0a4ede4155519b70fbca65ac73f9ece64da276`, `ParallelBooster` / `DropoutBooster`. [NeurIPS 2025 paper](https://papers.neurips.cc/paper_files/paper/2025/hash/2f383b17f62bb308b50f20b4e679c9de-Abstract-Conference.html).
- Inferable EBM: the same author package's `ExplainableBooster`, numeric main effects without interactions. [AISTATS 2026 paper](https://proceedings.mlr.press/v300/fang26a.html). The current author implementation explicitly marks full-prediction intervals as experimental; this is not an independently certified reproduction of every setting in the paper.
- RF-U: [RLT](https://github.com/teazrq/RLT), commit `d83a648a15591bbd4f057322dfdea7a75f056992`, `var.mode="matched"`. Xu, Zhu and Shao's [infinite-order U-statistic variance estimator](https://arxiv.org/abs/2202.09008), EJS 2024. Plain regression forest, not reinforcement learning splits.

Official packages are unmodified and isolated in `venv_modern` / `rlib_modern`; archive hashes, Python freeze and R build logs are recorded remotely in `evidence/`.

## Fixed configurations

The exact machine-readable settings are in `configuration()` in `run_modern_task.py` and each output's `config.json`. These are fixed author README examples, not selected using query labels, oracle coverage or interval length.

| Method | Configuration |
|---|---|
| BRAT-P | 70 rounds × 6 trees, subsample .8, depth 8, at most 64 leaves, min leaf 4, 64 bins, drop first round |
| BRAT-D | 700 iterations, learning rate .8, dropout .1, subsample .8, depth 6, at most 64 leaves, min leaf 2, 64 bins |
| Inferable EBM | 160 rounds, learning rate .6, full-row feature updates, warmup 10, depth 4, min leaf 8, 32 bins, no leave-one-out updates |
| RF-U | 10,000 trees, half-sample matched pairs without replacement, mtry floor(p/2), min node 5, one thread |

Boulevard explicitly uses `mode="confidence"`; its default prediction interval is never used. `prepare_inference()` uses the package's documented training-residual variance fallback, retaining all context rows for fitting. No held-out observations exist outside the frozen context, and this protocol does not split the context or apply outcome-calibrated width inflation. Training-residual noise estimates can be optimistic; this choice must remain visible when reporting results. The README generally prefers held-out variance estimation. No test/oracle residuals are used.

RF-U uses normal intervals around the official prediction with the official matched-sample sampling variance. No observation-noise term is added. RLT automatically requires distribution-based importance computation for active variance modes; it is retained. Predeclared retries increase the forest to 40,000 and then 160,000 trees only when the **returned** sampling variances are nonfinite or negative. The wrapper performs no clipping, query omission, or selection by achieved coverage. **Audit correction (2026-10-27): the pinned RLT implementation itself floors negative matched-sample variances at zero before returning them. The retry gate therefore cannot detect those pre-floor negatives.** Saved results contain 4,040 zero variances / zero-width intervals across 764 tasks; saved zeros alone do not distinguish originally negative estimates from genuine zeros. All are retained unchanged. A task failing all observable checks blocks a complete result for that method.

## Source-fidelity audit correction (2026-10-27)

BRAT-P and BRAT-D use the pinned author package, but are not exact reproductions of the paper experiments. The package's parallel version omits the paper's sequential warm-start; its current inference implementation uses histogram-cell calculations instead of the paper experiment's Nyström approximation. Both use the documented training-residual variance fallback here, whereas the paper experiment and preferred README workflow use held-out residuals. Saved interval arithmetic and eight targeted original-data replays passed. The audit found no adapter scaling error or persistent explosive final fits. See `EXPERIMENT_AUDIT.md` and `evidence/audit_bde_brat_20261027.md`.

## Validation and completion

Five production-config pilots cover the smallest context, largest context, largest encoded feature count, the previous BDE extreme task, and asymmetric outliers. Reduced smoke runs are separate and never enter evaluation. Gates check shapes, finiteness, ordering, paired hashes and independently recomputed interval endpoints; predictive accuracy/coverage does not decide whether a task is retained.

For Boulevard, independently verify residual variance, official signal scale, influence norm and `mean +/- z * SE`. For RF-U verify the variance and normal endpoints. Save original-unit mean, endpoints and SE, plus standardized inference diagnostics, context scale, package versions and any retry/fallback metadata. Zero or narrow intervals are not silently widened. The EBM API may yield near-zero influence norms for constant fitted terms; preserve and disclose such outcomes.

Full queues use per-method locks and immutable config/source hashes. Aggregate only after all 1,280 tasks and 155,520 queries succeed for a method. Recompute coverage, length and RMSE from saved endpoints and oracle independently, and repeat verification after local sync. Equal query weight within each task, equal task weight within regime, equal regime weight overall, as in the existing figure. Never publish partial averages.

Only completed methods enter a separate `stress_modern_ci_results.csv`, then the opening scatterplot. Preserve points-only format, signed under/overcoverage, no inset or range bars. Update slide count/source and notes after verified completion. Retain the existing saved-oracle scope statement without changing the target.
