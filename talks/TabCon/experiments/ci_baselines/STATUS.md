# Experiment status

Completed on 2026-10-26: GRF, Local Linear Forest and BDE each finished all 1,280
original paired tasks (155,520 queries), with zero failed tasks. All per-query
predictions and recomputed coverage/length metrics passed the final verification.

DeepLR was cancelled at the user's request; its partial results are excluded.
The frozen dataset and complete results are saved locally under `data/` and
`runs/full/`, respectively, as well as on beast.

The three completed methods are added to the local opening scatter using the
same equal-task/equal-setting aggregation as the original methods. Original
paper data are unchanged. BDE has one extreme but finite high-noise result;
it is retained without trimming and flagged on the slide.

Audit on 2026-10-27 traced this BDE outlier to a reproducible, local explosion in
one base member's predicted noise scale at epoch 77, amplified by the official
parametric bootstrap. Exact replay matches bitwise; checkpoint and CI checks
pass. Three alternate training seeds and an explicit gradient-clipping diagnostic
avoid the extreme width on this task. These diagnostics do not replace production
results. See `BDE_AUDIT.md` and `evidence/bde-audit.json`.

Remote directory: `/home/kyle/Documents/lab/tabcon-ci-baselines-20261026`.
Source and configuration details: `PROTOCOL.md`. Plot provenance:
`../../figures/data/stress_additional_ci_provenance.json`.

No GitHub commit or push has been made.
