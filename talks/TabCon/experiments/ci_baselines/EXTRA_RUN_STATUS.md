# Additional baseline execution state — 27 October 2026

**RF-IJ and DRF are complete and plotted locally.** BART, GP and DeepLR remain
cancelled at the user's request. Do not restart or plot them. No GitHub commit,
push or publication was performed.

Beast root: `/home/kyle/Documents/lab/tabcon-ci-baselines-20261026`.

## Completed results

Both methods completed all 1,280 original paired tasks and all 155,520 queries,
with zero failed tasks. Saved intervals, metrics, data hashes and configurations
were independently verified on Beast and locally before export.

| Method | Average coverage | Average interval length |
| --- | --- | --- |
| RF-IJ | 0.53057861328125 | 0.7261888936328144 |
| DRF | 0.5805023193359375 | 0.7703466374315616 |

These averages use the unchanged original saved latent oracle. They do not
establish conditional-mean coverage guarantees; the original oracle caveat is
retained in the slide notes and provenance. The intervals are short and
substantially undercover the saved target.

The local opening scatter now contains eleven methods. The original six methods,
prior GRF/LLF/BDE results, and BDE's flagged extreme task are unchanged. The chart
continues to show points only, with no inset or range bars.

Export: `figures/scripts/export_extra_ci.py --methods rfij drf`.
Data: `figures/data/stress_extra_ci_results.csv` and
`figures/data/stress_extra_ci_provenance.json`.
Render: `figures/scripts/draw_stress_tradeoff.py`.
Preview: `http://localhost:3031/#/first-results`.

DRF provenance records prediction-manifest SHA256
`ce8fd2a15cb3df06500a338ba6a931bcc7a763378d268ebf26ca6cfe49104837`.
All source configurations, per-query predictions and metrics are retained under
`runs/extra_full/drf/`. The remote queue finished normally and aggregate checks
passed. The automatic completion follow-up can now be removed.

## Execution history

DRF used the official drf 1.3.1 uncertainty API with 6,000 honest trees and 100 CI
groups. It initially ran with three CPU workers, then resumed with six after GP
was cancelled. Each fit used one thread. The three in-flight DRF tasks were
allowed to finish before resumption; no data or model configuration changed.
The original launch and resumption records are retained. Final progress reports
1,280 finished and zero failed tasks. Log: `runs/extra_full/controller_drf.log`.

## Cancelled methods

All active GP workers were stopped. Its 380 complete tasks and three failures
are retained only for provenance and excluded from plotting. The failures
included line-search nonconvergence and a posterior numerical cross-check
mismatch on near-zero tasks. BART never entered a full queue: its largest
near-constant pilot remained unconverged at 32,000 retained draws per chain
(maximum R-hat 1.6809; minimum bulk ESS 6.31). The user excluded Bayesian credible
intervals, so no further BART/GP work is authorized by the existing scope.

Cancellation record: `runs/extra_full/cancellations.json`.
`aggregate_extra.py` reads it and excludes cancelled methods.

The context-size audit is `evidence/dataset-sizes.json`: realized range 9–2,039,
median 426.5, 180 tasks below 30 rows and 370 below 100. All 1,280 saved input arrays
were checked against their metadata.
