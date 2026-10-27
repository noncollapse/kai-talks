# BDE extreme-result audit — 2026-10-27

The outlier is a reproducible **training instability in one original member's
noise-scale output**, propagated through the official parametric bootstrap.
No CI/PI mix-up, interval-aggregation bug, checkpoint collision, or optimizer-state
restoration failure was found in the current run. This does not establish that
BDE generally produces enormous intervals on these data.

All diagnostics used the frozen `high_noise__053` inputs: 976 context rows,
48 encoded features (49 raw), and the same 256 queries. Input SHA256:
`f5d2f69a64719f09611d8d444ad25fd69f140e52658a1621ceb28192f79ba489`.
Production results, plotting data and the slide figure were not replaced.
Nothing was pushed to GitHub.

## Observed failure chain

1. **Original data are ordinary in response scale.** Context responses range
   from -2.5135 to 10.7184, with standard deviation 1.96746.
2. **One input row has unusually large standardized coordinates.** Original
   context row 831 (zero-based) is the only one of 976 rows with the rare value
   of binary feature `x16`. Its standardized value is 31.225. The same row has
   standardized values -15.588 for `x13` and `x23`, whose minority values occur
   four times. These are existing data features, not newly added observations.
3. **Base member 1 becomes unstable at epoch 77.** Its largest context log-scale
   output is 0.864 at the end of epoch 76, 15.668 at epoch 77 and 17.856 at
   epoch 78. At epoch 80, the affected row's log-scale is 15.928. The official
   transformation is `sigma = (exp(log_sigma) + 1e-3) * y_std`, giving
   **16,264,385** on this row; the member's median context sigma is only 0.546.
   Batch-level observations locate the onset at optimizer iteration 2,374 in
   epoch 77. The rare-row log-scale changes from -2.514 at iteration 2,373 to
   0.369, 2.878, 4.976, then keeps rising. Large standardized coordinates are
   a plausible contributor; this audit does not isolate feature scaling as the
   sole cause.
4. **Parametric bootstrap amplifies the bad scale estimate.** The official
   `gen_extra_deep_ensemble` samples at the original context inputs using the
   fitted mean and sigma. Member 1 produces a synthetic response of
   **-5,886,797.30** at row 831. Its bootstrap response mean becomes -6,028.27
   and standard deviation **188,335.34**. The other members' bootstrap response
   standard deviations are approximately 1.80–1.88.
5. **Retrained predictions inherit this inflated response scale.** Official
   `ExtraTrainedNetwork` standardizes the newly sampled responses and reverses
   that standardization when predicting. Its query means span -424,593.50 to
   13,262.63. The other four retrained members remain approximately within
   -1.87 to 8.81. Its normalized training loss decreases; the primary failure
   has already happened in the original member's sigma output.
6. **The official CI formula then produces huge widths.** The squared difference
   between each original and bootstrap mean enters the estimated variance.
   This task's mean CI length is **16,948.5957**, coverage 100%. The original
   ensemble point prediction remains reasonable (RMSE 0.79495), which explains
   why checking only prediction RMSE or finite values did not flag the failure.

All outputs remain finite. Average training loss also fails to diagnose the
problem: the affected base member's final epoch loss is -0.6632. This is local
scale-output instability, not evidence that all network weights became NaN.

## Controlled diagnostics

Only training randomness or the explicitly listed optimization setting changes;
the data, architecture, 80/56/24 epoch protocol, regularization, and CI procedure
are held fixed. These are single-task diagnostics, **not replacement benchmark
results or seed selection**. The three additional seeds were fixed as original
seed + 1, + 2, + 3 before running them. No query/oracle-based training selection
was introduced.

| Diagnostic | Seed | Maximum base context sigma | Mean CI length | Coverage |
| --- | ---: | ---: | ---: | ---: |
| Original / exact replay | 601967104 | 16,264,385 | 16,948.5957 | 100.00% |
| Same data, seed + 1 | 601967105 | 5.5674 | 3.5980 | 93.75% |
| Same data, seed + 2 | 601967106 | 20.3938 | 3.4774 | 94.92% |
| Same data, seed + 3 | 601967107 | 22.6113 | 3.6849 | 94.92% |
| Original seed, global gradient norm clipped at 1 | 601967104 | 6.3290 | 3.1979 | 95.31% |

The original outcome was reproduced twice with observations added: all original
and bootstrap query means and CI variance arrays are **bitwise identical** to
the original saved results. Clipping is an exploratory stabilization test, an
explicit change from the author's optimizer defaults. Its result supports a
training-instability diagnosis; it does not validate clipping as a general fix.

## Implementation checks

- Five deployed upstream files match their pinned official Git blob hashes.
  Runtime copies match the recorded compatibility patches. Base architecture,
  exponential scale output, epochs, ensemble size and L2 follow the author's
  [Section 4.2](https://arxiv.org/html/2202.10903v2#S4.SS2).
- The adapter independently reconstructs the analytic CI from the original
  and bootstrap mean predictions. It matches the official CI return. The
  simulated PI is discarded; observation noise is not directly added to the CI.
- All five original epoch-56 checkpoints have the same weights **and every Adam
  state variable** as the exact replay. Each has 1,736 optimizer updates.
  The original checkpoint files were not changed by the check.
- The separate serialization regression check passes: Adam slots, iteration
  counter, and the next training update are preserved. The previously fixed
  SavedModel compatibility issue is not the cause of this outlier.
- Task working directories are isolated. The failure occurs in base training
  before checkpoint reload for bootstrap; it is not caused by bootstrap loading
  another task's checkpoint.
- The additional-method CSV still has SHA256
  `e0b719ac2a0669f8eb9c2f3e3b573fe92e25b1f598612f1cb2135e165ec2c41a`.
  The existing SVG hash still matches its saved figure manifest.

## Implication and next step

The plotted BDE overall mean length of 14.7675 is dominated by this one task
(about 89.66% of the sum of the 1,280 task mean widths). Treat that point as an
**unstable training run requiring qualification**, not as a clean statement
about the method's usual interval efficiency. The three alternate seeds are too
few and too task-specific to estimate the general failure rate.

Before changing the benchmark, define a consistent stabilization protocol using
training/validation diagnostics: monitor maximum context log-sigma as well as
loss, and evaluate measures such as gradient clipping or a smaller learning
rate. Then apply the chosen protocol to all BDE tasks and report it as an
adaptation. Do not selectively change only this task's seed or delete its width.
The official-default result and these diagnostic runs should remain auditable.

## Evidence and reproduction

- Compact evidence with hashes: `evidence/bde-audit.json`.
- Detailed epoch/batch and per-member arrays: `runs/audit/bde_high_noise_053_seed_0/`.
- Other seeds and clipping: neighboring `runs/audit/bde_high_noise_053_*` directories.
- Checkpoint integrity: `runs/audit/checkpoint_audit.json`.
- Feature identification: `runs/audit/feature_audit.json`.
- Full diagnostic models remain on beast under
  `/home/kyle/Documents/lab/tabcon-ci-baselines-20261026/runs/audit/`.
- `diagnose_bde.py` observes the unchanged adapter and optionally changes only
  a declared seed offset or global gradient clipping. Use a fresh output directory.
- `audit_bde_checkpoints.py` checks the pinned sources and compares the original
  checkpoints to the exact replay without training or overwriting them.

The existing benchmark's stored-oracle caveat in `PROTOCOL.md` still applies.
It does not explain the exploding width: the instability is visible in context
training and bootstrap generation before any evaluation oracle is loaded.
