# Display update — 2026-10-27

Inferable EBM was removed from the comparison at the user's request. No additional EBM diagnostic run was started. Its original source, configurations and all 1,280 task outputs remain archived unchanged. The opening figure now displays **14 methods**, without EBM or the broken x-axis. No commit or push.

The completion record below describes the archived four-method run; it is not the current display selection. Remaining-method source/adapter audit reports are stored under `evidence/audit_*_20261027.md`.

---

# Additional CI baselines — completed 2026-10-27

All four authorized methods completed all **1,280 original tasks / 155,520 queries each**, with no failed or omitted tasks. No Git commit, push or publication. BART, GP and DeepLR remain cancelled.

| Method | Mean coverage | Mean interval length |
|---|---:|---:|
| BRAT-P | 15.3622% | 0.207491 |
| BRAT-D | 26.4478% | 0.266603 |
| RF-U | 64.5370% | 0.948955 |
| Inferable EBM† | 79.2661% | 7.60628 × 10^13 |

The existing aggregation is unchanged: equal query weights within tasks, equal task weights within each of ten stress settings, then equal setting weights. Coverage uses exactly the saved target of the existing plot; no DGP or oracle changed.

† **EBM has unstable fits.** Its author-provided experimental full-prediction CI interface returns finite but extreme outputs on some tasks. In `high_noise__042` (n=51, p=139 encoded), standardized point predictions reach 1.38e15 and residual variance is 9.88e29, before any interval rescaling. Its task mean interval length is 5.54e16. 807 of 1,280 tasks have standardized training residual variance above 1e6. This is a numerical-instability result, not a usable calibrated interval benchmark. All raw results are retained; the figure uses a clearly marked log x-axis break to show the extreme point alongside the other fourteen methods.

## Verification

- All 20 production pilots passed and were independently verified locally.
- All 5,120 full task outputs / 622,080 query intervals were checked on Beast and locally. Input/config/manifest and saved prediction hashes agree. Original-unit transformations and standard errors agree with saved official variance/influence diagnostics. Coverage and length were recomputed from saved endpoints.
- RF-U used 10,000 trees on every task; no wrapper retry or query omission occurred. **Correction after source audit:** official RLT internally floors negative matched variances at zero; the wrapper cannot detect pre-floor negatives. Saved results have 4,040 zero-width intervals across 764 tasks, retained unchanged. The earlier assertion that no clipping occurred was not justified.
- BRAT-P, BRAT-D and EBM retain every context row and use the author's documented training-residual variance fallback. The README generally recommends held-out residual estimation; no query labels, oracle residuals or outcome-based interval calibration were used.
- Existing six methods, GRF/LLF/BDE (including BDE's extreme task), RF-IJ and DRF results remain unchanged. GRF/LLF/BDE table SHA-256: `e0b719ac2a0669f8eb9c2f3e3b573fe92e25b1f598612f1cb2135e165ec2c41a`.
- Independent evidence: `evidence/modern_completion_verification.json`. Protocol: `PROTOCOL_MODERN.md`. Complete saved outputs: `runs/modern_full/{bratp,bratd,rfu,iebm}/`. Each includes configuration, raw predictions/SE, diagnostics, launch hashes, summary and provenance.

## Local presentation

At completion, the opening graph contained **15 methods** (the current display has 14 after the user removed EBM), points only, no inset or range bars, with signed under/overcoverage. SVG, PNG and PDF regenerated. Source count, speaker notes, EBM/BDE flags and README updated. Browser preview visually checked at http://localhost:3031/#/first-results; points and labels are visible and no labels overlap. Preview screenshot: `/tmp/tabcon-modern-results-preview.png`.

Completion monitoring is paused after this verified local update; no further polling is needed.

Official archive SHA-256: Boulevard `a51028d9a9990d69cad25a9a6cda1a31828fb2dfde3087fc589b012849f468ad`; RLT `545a425422c418a39022429021c283f60c797d6809463b275d2cd3115c34f947`. Installed versions: Boulevard 0.1.0a1, scikit-learn 1.8.0, RLT 6.1.1. Original queued configurations and author source were not changed during or after the run.
