---
theme: default
title: Can Tabular Foundation Models Amortize Statistical Inference?
author: Kai Ye
info: |
  A visual introduction to PFNs, predictive uncertainty and TabCon.
  Based on arXiv:2609.33114.
transition: slide-left
routerMode: hash
colorSchema: light
fonts:
  provider: none
drawings:
  persist: false
class: cover-slide
---

<h1 class="cover-title">Can Tabular Foundation Models<br><span>Amortize Statistical Inference?</span></h1>
<div class="cover-authors">Kai Ye · Shijin Gong · Hongyi Zhou · Valentina Zangirolami · Chengchun Shi</div>
<div class="cover-bottom"><img class="lse-logo" width="72" height="72" src="https://upload.wikimedia.org/wikipedia/commons/5/51/LSE_Logo.svg" alt="London School of Economics and Political Science logo"><a href="https://arxiv.org/abs/2609.33114">arXiv:2609.33114</a></div>


<!--
The central question is whether we can learn a reusable procedure for uncertainty about an estimated average, much as a PFN learns a reusable prediction procedure. We will build the distinction visually before discussing the model. Source: https://arxiv.org/abs/2609.33114
-->

---
routeAlias: first-results
class: result-preview-slide
---

# Our Proposal: TabCon for Confidence Interval (CI) Construction

<StressPreview />

<!--
Open with the result before explaining how it is achieved. These are the ten stress settings from the supplied paper figure; regular_control is excluded. The six original methods use the paper numeric results, verified against the original figure's source SHA256 and the frozen main/Wald summary JSONs. GRF, Local Linear Forest, BDE, RF-IJ, DRF, BRAT-P, BRAT-D, and RF-U are additional completed evaluations on the same 1,280 recovered and verified task realizations, including all 155,520 original query points. These new methods use author/package implementations with documented compatibility adaptations and fixed configurations; all eight completed all tasks with finite outputs; this numerical gate does not certify training stability. Linear means Linear-Wald-HC3; RFF means RFF-Wald-HC3. Both are custom statistical implementations, not official-package baselines. Linear applies context-only PCA when necessary; RFF uses at most 64 random features. Their HC3/z formulas are correct, but ill-conditioned designs cause numerical sensitivity and six Linear replay discrepancies are documented. Historical points are retained. AMP denotes a paper-based approximate martingale-posterior credible interval, not an ordinary frequentist CI; its author-code endpoint returned HTTP 401 during the audit, so exact source equivalence has not been established. TabPFN (PI) is the native predictive interval, evaluated here against the saved latent oracle rather than a future noisy outcome. This is a reference baseline with a different native target, not a claim that TabCon dominates every confidence-interval procedure. Code inspection showed that the Generator V2 oracle T(Z) is not guaranteed to equal E[Y|observed X]; do not describe this stress figure as independently verified conditional-mean coverage.

TabCon's unweighted average coverage across the ten settings is 0.95614013671875 (range approximately 0.9400–0.9842). Its mean interval length is 1.8581469892765767, compared with 3.209065453414952 for native TabPFN prediction intervals. The displayed 42% reduction is 1 minus the ratio of these arithmetic means, not a mean of per-setting percentage reductions. Every setting has 128 tasks, so equal-setting and equal-task weighting coincide. Short intervals alone are insufficient: Bootstrap is shorter but substantially undercovers in these results. Neither a universal coverage guarantee nor significance is asserted.

This scatter preview uses arithmetic mean interval length on a log x axis and signed per-setting coverage deviations from 95% on a linear y axis, in percentage points. Each point shows one method's average deviation; no range bars are displayed. Positive means overcoverage, negative means undercoverage, and closeness to zero is desirable. TabCon's mean deviation is +0.614013671875 pp, with a range from -1.0028076171875 to +3.4161376953125 pp; four settings under-cover and six over-cover. AMP also has mixed directions (one under, nine over). These per-setting ranges are not displayed: opposite deviations can cancel in the plotted mean. The old Pareto staircase and lower-left-is-better annotation are removed because signed coverage should be close to zero rather than simply minimized. Length is averaged in the original outcome units without normalization, so high-scale settings have greater influence on mean length. The original radar remains available as stress-opening-radar.svg. figures/scripts/draw_stress_tradeoff.py regenerates this preview and its summary JSON; the original result table and hash remain unchanged.

The first three additions are exported from complete per-query predictions by figures/scripts/export_additional_ci.py. Their numeric table and provenance are figures/data/stress_additional_ci_results.csv and stress_additional_ci_provenance.json. RF-IJ and DRF are exported and independently checked by figures/scripts/export_extra_ci.py, with separate stress_extra_ci_results.csv and stress_extra_ci_provenance.json. RF-IJ uses ranger 0.18.0 with 2,000 trees and native infinitesimal-jackknife standard errors. Its mean coverage is 0.53057861328125 and mean interval length is 0.7261888936328144. DRF uses the official drf 1.3.1 native uncertainty API with 6,000 honest trees, 100 CI groups, exact group-weighted means and their sample variance. Its mean coverage is 0.5805023193359375 and mean interval length is 0.7703466374315616. All 1,280 tasks and 155,520 queries passed per-query verification on Beast and locally. Its intervals are short but substantially undercover this saved target; no universal coverage conclusion is asserted. BART and GP were cancelled by the user on 27 October 2026, who excluded Bayesian credible-interval baselines. Their pilot and partial results are not plotted. DeepLR was cancelled by the user and is excluded. BDE mean length is strongly influenced by high_noise__053, whose mean interval length is about 16,948.6; one bootstrap-retrained network produced extreme predictions. This finite result is retained without trimming; the extreme task is documented in these notes and the implementation audit. The existing Bootstrap comparator is TabPFN mean predictions across bootstrap resamples of context rows, distinct from BDE's parametric bootstrap retraining. Both target uncertainty in the regression function, not future-outcome noise. The archived six-method radar is unchanged. See experiments/ci_baselines/PROTOCOL.md, PROTOCOL_EXTRA.md and PROTOCOL_MODERN.md for configurations, data pairing and limitations.

The latest additions are exported by figures/scripts/export_modern_ci.py into stress_modern_ci_results.csv and stress_modern_ci_provenance.json after all saved endpoints, standard errors, task/config hashes and metrics were independently checked remotely and locally. Each method uses all 1,280 tasks / 155,520 queries without trimming. BRAT-P: mean coverage 0.1536224365234375, mean length 0.2074908501043721. BRAT-D: 0.2644775390625 and 0.2666031319457618. RF-U: 0.6453704833984375 and 0.9489549325520208. These are results of fixed author README configurations on this benchmark, not tuned optimal performance or universal comparisons.

BRAT-P and BRAT-D use unmodified Boulevard 0.1.0a1, pinned commit ec0a4ede4155519b70fbca65ac73f9ece64da276. The interval mode is explicitly confidence. The package settings are not exact replications of the paper experiments: current ParallelBooster omits the paper’s sequential warm-start and the package uses histogram-cell inference rather than the paper experiment’s Nyström approximation. All context observations are retained for fitting; the documented prepare_inference() fallback estimates residual variance on the training data. The author README prefers held-out variance estimation, so optimistic training-residual estimates remain a limitation. No query outcomes or oracle residuals are used to fit or calibrate intervals. RF-U uses RLT 6.1.1, pinned commit d83a648a15591bbd4f057322dfdea7a75f056992, with the matched-sample U-statistic variance estimator. All 1,280 tasks returned finite nonnegative variance estimates at the original 10,000 trees; none triggered the wrapper retry. Audit correction: official RLT floors negative matched variances at zero before returning them, so this gate cannot detect pre-floor negatives. There are 4,040 saved zero-width intervals across 764 tasks, all retained. No claim is made that every raw variance estimate was positive.

Inferable EBM was removed from this comparison at the user’s request on 27 October 2026. Its raw results are retained in the experiment archive. The plot now contains fourteen methods on a continuous log x-axis. See experiments/ci_baselines/EXPERIMENT_AUDIT.md and its three independent evidence reports for the per-method implementation audit, configuration differences and remaining limitations.
-->

---
routeAlias: roadmap
clicks: 0
class: background-agenda
---

# Background

<BackgroundAgenda active="ci" />

<!--
The background agenda presents CI construction first, followed by tabular foundation models. The two topics link to their corresponding sections. The interval illustration animates automatically: each repeated sample produces an estimate and an interval, while the true mean stays fixed. Two intervals cover it and one misses it; these three schematic samples do not represent a nominal coverage rate. No presentation clicks are required. The diagrams are conceptual illustrations, not experiment results.
-->

---
routeAlias: confidence-intervals
class: advisor-background ci-example-slide
---



# CI Construction: A Classical Statistical Inference Problem

<p class="lead">What is the average house price in London?</p>

<div class="ci-example-grid">
<div>
<section class="panel ci-example-card ci-example-miss">
<div class="ci-example-truth">£500k</div>
<div class="ci-example-left">
<div class="ci-example-track"><span style="left:0;width:100%;background:#dc3545"></span></div>
<div class="ci-example-range" style="color:#dc3545">£460–490k</div>
</div>
</section>
<div class="ci-example-verdict" style="color:#dc3545" aria-label="Cross: misses the true mean">✗</div>
</div>
<div>
<section class="panel ci-example-card">
<div class="ci-example-truth">£500k</div>
<div class="ci-example-track"><span style="left:0;width:100%;background:#7c4dce"></span></div>
<div class="ci-example-range violet">£440–560k</div>
</section>
</div>
<div>
<section class="panel ci-example-card ci-example-preferred">
<div class="ci-example-truth">£500k</div>
<div class="ci-example-fit">
<div class="ci-example-track"><span style="left:0;width:100%;background:#0b9687"></span></div>
<div class="ci-example-range teal">£480–520k</div>
</div>
</section>
<div class="ci-example-verdict" style="color:#0b9687" aria-label="Tick: covers with a shorter interval">✓</div>
</div>
</div>

<p class="ci-example-takeaway">Ideally, a CI covers the truth and is as short as possible to remain informative.</p>

<!--
Illustrative London house-price example, not a current market statistic. Each box shows the same hypothetical true average, £500k. The first interval misses it; the second covers it but is wide; the third covers it and is shorter. Bar lengths are schematic for readability, not drawn on a common numerical scale; the endpoints state the actual intervals. Show all three examples together. In practice the true mean is unknown: we seek procedures with reliable repeated-sampling coverage and short intervals rather than selecting a realized interval by checking unknown truth. The next slide explains coverage.
-->

---
clicks: 1
class: advisor-background
---

<div class="eyebrow">Given a nominal level <MathTex tex="1-\alpha" /></div>

<h1>A CI should ideally cover the truth <MathTex tex="1-\alpha" /> of the time</h1>

<CoverageDemo />
<div class="source">Illustrative repeated-sampling intervals. One set of 20 need not contain exactly 19 successful intervals.</div>

<!--
Advance once to reveal the repeated-sampling intervals and then the coverage message. The underlying average stays fixed. Different datasets produce different estimates and intervals. A 95% procedure aims to cover that fixed target in about 95% of repeated experiments. This does not mean 95% of future outcomes fall in the confidence interval, and the frequentist statement is not a posterior probability assigned to the fixed target after observing one interval.
-->

---
clicks: 0
class: advisor-background
---

<div class="eyebrow">For decades, statisticians have been developing CI construction procedures</div>

#  Resulting in a Rich Literature on Statistical Inference

<div class="two mt-7 ci-paradigms">
<div class="panel">
<div class="eyebrow">Classical paradigm</div>
<h3>Compute CIs anew for each data</h3>
<ul>
<li>Asymptotic calculations: Wald intervals <a class="ci-method-ref" href="https://doi.org/10.1090/S0002-9947-1943-0012401-3">(Wald, 1943)</a>; delta method <a class="ci-method-ref" href="https://books.google.com/books?id=_db1jwEACAAJ">(Cramér, 1946)</a>.</li>
<li>Resampling: bootstrap <a class="ci-method-ref" href="https://doi.org/10.1214/aos/1176344552">(Efron, 1979)</a>.</li>
<li>Bayesian inference: credible intervals <a class="ci-method-ref" href="https://doi.org/10.1098/rstl.1763.0053">(Bayes, 1763)</a>.</li>
<li>…</li>
</ul>
</div>
<div class="panel" style="background:#eef2ff;border-color:#c3cff7">
<div class="eyebrow">Our new paradigm</div>
<h3>Learn the computing procedure itself</h3>
<ul>
<li>Approximate CI construction with a single neural network.</li>
<li>Learn its parameters through pre/post-training across simulated data.</li>
<li>Produce CIs for a new dataset in a single forward pass.</li>
</ul>
</div>
</div>

<!--
The contrast concerns where computation occurs. Conventional asymptotic, bootstrap and posterior procedures typically compute uncertainty anew for each dataset; their mathematical recipes are reusable, so we do not design a new method from scratch for each dataset. Bayesian credible intervals have a posterior-probability interpretation and are not automatically frequentist confidence intervals. Bayesian inference can also be amortized; the left box describes conventional per-dataset implementations, not an inherent limitation of these mathematical families. Our approach moves shared computation into training across tasks, then applies the learned interval procedure to a new dataset. The network still performs inference-time computation, and shared pre/post-training has a cost. At this level, the single network denotes the complete TabCon system, including its frozen foundation-model backbone and trained heads/router.
-->

---
routeAlias: background-tfm
clicks: 0
class: background-agenda advisor-background
---

# Background

<BackgroundAgenda active="tfm" />

---
routeAlias: foundation-models
clicks: 0
class: advisor-background
---

<div class="eyebrow">We have foundation models for images, language, …</div>

# One Model, Many Tasks Without Retraining

<FoundationModalities />

<div class="callout mt-6"><b>Tabular foundation models</b> adopt the same idea, but for <b>tabular data</b>.</div>

<!--
Start from the familiar idea of a pretrained model that supports multiple downstream tasks. Vision foundation models work with images; language foundation models such as GPT work with text. The visuals are schematic examples of modalities and capabilities, not screenshots or outputs from a particular model. Tabular foundation models bring this reuse idea to rows and columns. This is an analogy, not a claim that their training data, objectives or architectures must be identical. The following slides introduce PFNs as the particular approach used by TabCon.
-->

---
routeAlias: tabular-timeline
clicks: 0
class: tabular-history-slide advisor-background
---

# How Learning on Tabular Data Evolved

<TabularEvolution />

<!--
Each row is an independent chronological timeline, not a shared time scale. Milestones link to representative primary sources, not necessarily the first invention of each broad method. Least squares was published by Legendre in 1805. Schoenberg's 1964 smoothing splines precede the 1972 GLM unification of linear, logistic and Poisson models; these regressions themselves are older. Cleveland's 1979 local polynomial smoother is a representative local-regression milestone, not the invention of all local polynomial methods. AdaBoost uses the 1997 journal year; its conference precursor appeared in 1995. The modern ML row begins with the 1986 backpropagation milestone for MLPs, not the invention of multilayer networks. Random forests and gradient boosting share the 2001 milestone. The separate deep-learning row is omitted for clarity.

The PFN paper is Transformers Can Do Bayesian Inference: preprint December 2021, ICLR 2022. The visible PFN date is explicitly its 2021 preprint year. This is a foundational PFN paper, not the first foundation-model paper in every sense. TabPFN follows at ICLR 2023 (2022 preprint); TabPFN v2 is Nature 2025. TabICL is ICML 2025, TabICL v2 ICML 2026: https://github.com/soda-inria/tabicl . LimiX paper: September 2025, https://arxiv.org/abs/2509.03505 . LimiX-2M is a 2-million-parameter model released November 2025, with a June 2026 paper https://arxiv.org/abs/2606.04485 ; it is distinct from LimiX-2, released September 2026, https://arxiv.org/abs/2609.17488 . Official release chronology: https://github.com/limix-ldm-ai/LimiX . TabPFN 2.5: November 2025; 2.6: March 2026; 3: May 2026; 3.5: September 2026, from official model reports and https://github.com/PriorLabs/TabPFN/blob/main/CHANGELOG.md . These are selected developments through October 2026, not an exhaustive catalog or a replacement hierarchy.
-->

---
routeAlias: pfn
clicks: 0
class: pfn-papers-slide advisor-background
---

# Tabular Foundation Models

<div class="pfn-paper-columns">
<section>
<div class="paper-year"><span>2021</span></div>
<h2>PFN</h2>
<div class="paper-venue">ICLR 2022</div>
<a class="paper-header-image" href="https://arxiv.org/abs/2112.10510"><img src="/figs/pfn-paper-header.png" alt="Original header of Transformers Can Do Bayesian Inference" /></a>
<a class="paper-title" href="https://arxiv.org/abs/2112.10510">Transformers Can Do<br>Bayesian Inference</a>
<p class="paper-focus">The general framework</p>
</section>
<section>
<div class="paper-year"><span>2023</span></div>
<h2>TabPFN</h2>
<div class="paper-venue">ICLR 2023</div>
<a class="paper-header-image" href="https://arxiv.org/abs/2207.01848"><img src="/figs/tabpfn-paper-header.png" alt="Original header of TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second" /></a>
<a class="paper-title" href="https://arxiv.org/abs/2207.01848">TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second</a>
<p class="paper-focus">Tabular classification</p>
</section>
<section>
<div class="paper-year"><span>2025</span></div>
<h2>TabPFN-v2</h2>
<div class="paper-venue">Nature 2025</div>
<a class="paper-header-image" href="https://doi.org/10.1038/s41586-024-08328-6"><img src="/figs/tabpfn-v2-paper-header.png" alt="Original header of Accurate predictions on small data with a tabular foundation model" /></a>
<a class="paper-title" href="https://doi.org/10.1038/s41586-024-08328-6">Accurate predictions on small data with a tabular foundation model</a>
<p class="paper-focus">Classification + regression</p>
</section>
</div>


<!--
PFN means Prior-Data Fitted Network: a general approach to learning approximate Bayesian posterior prediction under a synthetic task prior. The first paper was posted in December 2021 and published at ICLR 2022; use 2021 here to match the preceding timeline, with the conference year explicit in the citation. TabPFN is a concrete PFN trained for small tabular classification, published at ICLR 2023 (2022 preprint). TabPFN-v2 is the successor described in the 2025 Nature paper, extending the scope to classification and regression and larger, more varied datasets. PFN is the framework; TabPFN and TabPFN-v2 are successive tabular implementations, not three unrelated algorithms. The common recipe is pretraining on synthetic tasks, supplying a new dataset as context, and predicting without per-dataset gradient updates in standard in-context deployment. Later fine-tuning variants exist. Learned Bayesian prediction is relative to the training task prior; it is not an automatic frequentist CI guarantee.
-->

---
routeAlias: prior-labs
clicks: 0
class: advisor-background
---

# Prior Labs: From Research to Industry

<PriorLabsOverview />

<!--
Prior Labs commercializes the TabPFN family. The official product page offers TabPFN-3.5, with Python/open-source, API and enterprise deployment routes. The visual is a still from the official TabPFN-3.5 product demo, linked by the product page at https://app.vidzflow.com/v/2QLEwEEaoO ; image URL https://r2.vidzflow.com/thumbnails/2QLEwEEaoO_1789039685.jpg . Do not describe it as a screenshot of a customer deployment.

Funding: Balderton's 5 February 2025 announcement confirms a €9 million pre-seed round, led by Balderton with other investors. This is a publicly announced financing round, not an assertion about audited total lifetime funding. SAP announced completion of its acquisition on 17 July 2026. Prior Labs continues to operate as an independent entity within SAP. The company is acquired rather than independently publicly listed; do not imply an announced standalone IPO. SAP itself is publicly listed. SAP committed more than €1 billion over the following four years. This is a forward investment commitment, not additional VC already raised and not the acquisition purchase price. Acquisition terms were not disclosed. Information checked on 28 October 2026 against Prior Labs, Balderton and SAP primary sources.
-->

---
routeAlias: pfn-ecosystem
clicks: 0
class: ecosystem-slide advisor-background
---

# Since 2025, Over 100 Papers on PFNs Have Appeared

<PFNEcosystem />

<!--
The numeric title is supplied by the speaker. An independent bibliographic count of more than 100 PFN papers published since 2025 has not been established here; do not treat the selected references as substantiation of the number. Papers, model families, checkpoints and applications are different counting units.

The first category groups predictive models and architecture research. SOMTab is third as requested; it uses Mamba-based state-space mixing. TabFM is Google Research's tabular model; Kumo Tabular is NVIDIA's September 2026 release. Research-code availability does not imply all examples are commercial products with equivalent support or licenses. TabICL and LimiX version chronologies follow their official repositories.

Causal effect estimation: Do-PFN (Robertson et al., NeurIPS 2025), CausalPFN (Balazadeh et al., 2025), CausalFM (Ma, Frauen, Javurek and Feuerriegel, ICLR 2026), and Learning to Fluctuate: Statistical Foundations for Causal Tabular Pretraining (Zhiheng Zhang, 2026, arXiv:2609.26290). Zhang's method is fluctuation-supervised pretraining (FSP), not another paper named CausalPFN. These methods differ in priors and identifying assumptions; none makes arbitrary observational causal effects identifiable without assumptions.

UQ: The first three entries are the three works discussed at the end of Section 2 of TabCon: Nagler and Rügamer, Uncertainty Quantification for Prior-Data Fitted Networks using Martingale Posteriors (arXiv:2505.11325, first posted 2025; revised 2026, cited as 2026 in TabCon); Ng, Fong, Frazier, Knoblauch and Wei, TabMGP: Martingale Posterior with TabPFN (ICML 2026, arXiv:2510.25154); Fortini, Ng, Petrone, Rousseau and Wei, Uncertainty Decomposition for Bayes-Filtered Transformers via Bayesian Predictive Inference (2026, arXiv:2602.04596). Additional references: Melnychuk et al., Frequentist Consistency of Prior-Data Fitted Networks for Causal Inference (ICML 2026, arXiv:2603.12037), with one-step posterior correction (OSPC); Florian D. van Leeuwen, Conformal Prediction for Tabular Prior-Data Fitted Networks with Missing data (AI for Tabular Data workshop at EurIPS 2025). Conformal prediction targets predictive coverage, while martingale posteriors and OSPC address other inferential quantities; these are not interchangeable frequentist CI guarantees. Sources checked 28 October 2026.
-->

---
clicks: 2
class: advisor-background
---

# How Do Tabular Foundation Models Work?

<p class="lead">A training dataset (predictors &amp; labels) + test predictors → a distribution over test labels.</p>

<PFNFlow mode="predict" />

<!--
Advance to send the new table into the frozen model, then reveal a predictive distribution. In regression, the output can express several plausible values of the next outcome. The values and density here are illustrative and are not outputs from a fitted TabPFN model. Source for the workflow: https://doi.org/10.1038/s41586-024-08328-6
-->

---
clicks: 2
class: advisor-background
---

# How to Train Tabular Foundation Models

<p class="lead">Generate datasets, mask outcomes, and learn to predict them.</p>

<PFNFlow mode="train" />

<!--
Advance twice. First hide a target, then show the training signal. The formula is the prior-data negative log-likelihood: q_theta is the network's predictive distribution, D is the observed context, and (x,y) is a held-out row from the same simulated task. The expectation averages over tasks drawn from the training prior and their sampled context/query rows; in practice this is estimated using a batch of negative log-likelihood terms. The hidden y is used to compute the loss, not supplied as an input when predicting it. For continuous outcomes, q_theta denotes a predictive density. The same network sees many relationships, noise levels and dataset sizes. This is where the reusable prediction procedure is learned. The tiny datasets are explanatory sketches, not experiments. The PFN approximates Bayesian posterior prediction under its synthetic task prior, rather than an arbitrary universal predictive distribution. Source: https://arxiv.org/html/2112.10510#S3
-->

---
clicks: 0
class: advisor-background
---

<div class="eyebrow">These models already quantify uncertainty by producing predictive distributions</div>

# Through Which Prediction Intervals (PIs) Can Be Drawn

<PredictiveDensity />

<!--
Advance once to reveal the central 95% predictive mass and the PI; advance again to compare the separate CI for the mean. A distribution is not itself an interval. One way to obtain an interval is to read off its 2.5th and 97.5th percentiles. The shaded region contains 95% of this model distribution. Reliable real-world predictive coverage still depends on calibration and assumptions. This interval targets a new observed sale price and combines outcome variation with uncertainty in our knowledge. The blue PI is approximately £343k–£657k under an illustrative Gaussian predictive distribution with mean £500k and standard deviation £80k. The green CI £480k–£520k is a separate illustrative interval for the unknown mean; it is not computed by taking narrower quantiles of the same outcome distribution. Both bars use the same price scale. The example demonstrates different targets and is not a real fitted TabCon result.
-->




---
clicks: 2
class: advisor-background
---

# CI v.s. PI

<IntervalLab mode="grow" />

<!--
Advance through 20, 80 and 320 observations, or use the buttons. More data makes the average more precise in this well-specified example, while the range for a new sale retains irreducible outcome variation. This is intuition, not a general guarantee of monotone interval shrinkage for every fitted model or every realized dataset.
-->

---
routeAlias: tabcon
clicks: 0
---

<div class="eyebrow">When tabular foundation models meet statistical inference</div>

# TabCon in One Slide

<TabConIntro />

<!--
*Suggested time: 1 minute*

Now, let's move to our proposed method, TabCon.

Before going into the details, I want to show you the main idea in one slide.

As we discussed before, TabPFN can take a new dataset and make predictions without any new training.

But our goal is different. We want to do statistical inference.

More specifically, we want to construct confidence intervals for the unknown regression mean.

Here is the basic idea.

We give a dataset to our model.

The model produces two outputs.

The first output is a point estimate of the regression mean.

The second output is a confidence interval for this mean.

For the point estimate, we directly use the pretrained TabPFN model.

For the confidence interval, we introduce a new model that learns the uncertainty of this estimate.

The important thing is that, after training, we can produce both outputs without updating the model on a new dataset.

So, we are trying to extend the idea of foundation models from prediction to statistical inference.
-->

---
routeAlias: tabcon-roadmap
clicks: 1
---

# Our Contributions

<TabConContributions />

<!--
*Suggested time: 1 minute*

Our work has four main contributions.

First, we introduce a new approach to confidence interval construction.

Instead of computing a confidence interval from scratch for every new dataset, we train a model to learn how to construct it.

Second, we propose a new model architecture.

It includes three different models for estimating uncertainty, and a router that decides how to combine them.

Third, we introduce a new training process.

We first train these uncertainty models with supervised learning.

Then, we use reinforcement learning to improve the router.

Finally, we evaluate our method on different synthetic and semi-synthetic datasets.

Our results show that TabCon can produce relatively short confidence intervals, while keeping coverage close to the target level.

It is also much faster than methods that need repeated model fitting.

I will explain these four points one by one.

*Click to highlight the first contribution.*

Let's start with the basic idea.
-->

---
routeAlias: tabcon-main-idea
clicks: 0
---

<div class="eyebrow">1. Amortized CI construction</div>

# Learn Residuals to Build CIs

<ResidualTrainingIdea />

<!--
*Suggested time: 2 minutes*

The first question is: how can we use a foundation model to construct confidence intervals?

Our idea is to learn the distribution of estimation errors.

Let's look at this figure.

First, we generate a synthetic dataset.

Since the dataset is generated by us, we know the true regression function.

So, for any given input x, we know the true mean, f of x.

Now, we give the dataset to a pretrained TabPFN model.

TabPFN produces a point estimate, f-hat of x.

Of course, this estimate may not be exactly equal to the true mean.

There may be some estimation error.

So, we calculate the difference between the estimated mean and the true mean.

We call this difference the **estimation residual**.

Here, the residual is defined as f-hat minus f.

We are not looking at the difference between an observed outcome and its prediction.
Instead, we are looking at the difference between the estimated mean and the true mean.

These are two different things.

Because we use synthetic datasets, we can calculate this estimation residual during training.

We can then use it as a supervised learning target.

Our new residual model takes the features from the pretrained TabPFN backbone and learns to predict a distribution of estimation residuals.

We repeat this process across many synthetic datasets.

In this way, the model learns how the TabPFN estimate can be wrong under different data settings.

When we receive a new dataset, we no longer know the true mean.

So we cannot calculate the real estimation residual.

But we can use our trained model to predict its distribution.

Finally, we use this distribution to construct a confidence interval.

This is the main idea behind TabCon.
-->

---
routeAlias: tabcon-oracle-coverage
clicks: 0
class: oracle-coverage-slide
---

<div class="eyebrow">1. Amortized CI construction</div>

# Learn Residuals to Build CIs

<div class="oracle-ci-definition"><MathTex tex="C_\alpha(x)=\left[\widehat f(x)-Q_{1-\alpha/2}(x),\;\widehat f(x)-Q_{\alpha/2}(x)\right]" display /></div>
<p class="oracle-quantiles"><MathTex tex="Q_\tau(x)" />: true τ-quantile of the residual <MathTex tex="\widehat f(x)-f(x)" />.</p>

<div class="oracle-beamer-block">
<div class="oracle-block-heading">Proposition 1</div>
<div class="oracle-block-body oracle-theorem-body">The interval <MathTex tex="C_\alpha(x)" /> covers the regression mean <MathTex tex="f(x)" /> with probability at least <MathTex tex="1-\alpha" />.</div>
</div>

<div class="oracle-beamer-block oracle-proof-block">
<div class="oracle-block-heading">Proof</div>
<div class="oracle-block-body"><MathTex tex="\begin{aligned}\mathbb{P}\!\left(f(x)\in C_\alpha(x)\right)&=\mathbb{P}\!\left(Q_{\alpha/2}(x)\leq\widehat f(x)-f(x)\leq Q_{1-\alpha/2}(x)\right)\\[7pt]&\geq (1-\alpha/2)-\alpha/2=1-\alpha.\end{aligned}" display /></div>
</div>


<!--
*Suggested time: 2 minutes*

Now, let's explain why learning the estimation residual is useful for confidence interval construction.

We define the residual as the difference between the estimate and the true value.

At a fixed input x, the dataset is random, so the residual has a sampling distribution.

If we know its true quantiles, we can use them to construct a confidence interval, as shown in the formula. The interval C alpha covers the mean f of x with probability at least one minus alpha.

The proof is simple. The true value is inside the interval exactly when the residual falls between the two quantiles.

However, in practice, we do not know the true residual distribution.

Our model learns it from simulated data, so calibration is important for achieving the target coverage.
-->

---
routeAlias: tabcon-architecture-roadmap
clicks: 0
---

# Our Contributions

<TabConContributions :active="2" />

<!--
*Suggested time: 30 seconds*

So far, we have introduced the main idea.

We learn the distribution of estimation residuals, and then use its quantiles to construct confidence intervals.

But one single residual model may not work equally well for every type of dataset.

For some datasets, it may produce intervals that are too short.

For other datasets, its intervals may be too wide.

This leads to our second contribution: a new model architecture.
-->

---
class: method-slide
clicks: 3
---

<div class="eyebrow">2. A new architecture for tabular foundation models</div>

# Three Residual Experts, One Sparse MoE Router

<TabConFlow />

<!--
*Suggested time: 2 minutes*

This slide shows the architecture of TabCon.

Our model is based on a mixture-of-experts structure, or MoE.

The basic idea is to have several experts and let a router decide which ones to use.

In our case, we have three residual experts.

*Click to reveal the three experts.*

The first one is called the **Global Head**.

It is trained on a broad range of synthetic datasets.

Its goal is to learn the general distribution of estimation residuals.

But we know that the Global Head may not perform equally well in every setting.

So, we introduce two additional experts.

The second one is called the **Expansion Head**.

It focuses on datasets where the Global Head tends to produce intervals that are too narrow.

The third one is called the **Shrinkage Head**.

It focuses on datasets where the Global Head tends to produce intervals that are too wide.

All three heads use the same pretrained TabPFN backbone.

We do not train three separate TabPFN models.

Instead, we reuse the frozen backbone and attach three smaller residual models to it.

*Click to reveal the router.*

Now, how do we decide which expert to use?

This is the job of the router.

The router reads information from the current dataset and produces weights for the three experts.

*Click to show the Top-2 selection.*

We use sparse routing, which means that only two experts are selected for each task.

The third expert receives zero weight. The selected pair depends on the task; any pair of experts can be selected.

We then combine the selected experts' residual distributions using their weights.

One important detail is that we combine the **distributions**, not the final confidence interval endpoints.

After getting the combined distribution, we calculate its quantiles and construct our confidence interval.

So the idea is quite simple.

Different datasets may need different ways to estimate uncertainty.

Our three experts provide different choices, and the router learns how to combine them.
-->



---
clicks: 4
routeAlias: router-details
class: detail-slide
---

<div class="eyebrow">2. A new architecture for tabular foundation models</div>

# The Sparse MoE Router

<RouterEncoder />

<!--
*Suggested time: 2 minutes 20 seconds*

Now, let's look more closely at the router.

The main question is: how does the router understand the current dataset?

First, the pretrained TabPFN backbone produces an embedding for each query point.

These embeddings contain information about the query points and the observed dataset.

We then pass these embeddings through a small trainable encoder.

This gives us a set of query tokens.

But the router needs to make one decision for the whole task.

So we need to combine all the query tokens into one summary.

Here, we use two methods.

*Reveal the attention branch.*

The first method is attention.

We introduce four learned query vectors.

Each vector calculates attention weights over the query tokens.

Then it takes a weighted average of these tokens.

So, we get four different summary vectors.

Each one can focus on different information in the query set.

*Reveal the statistics branch.*

The second method is much simpler.

We calculate the mean and standard deviation of the query tokens.

The mean gives us information about the average representation.

The standard deviation describes how much the token values vary across the query points.

So, now we have six summary vectors in total.

Four come from attention.

One is the mean.

And one is the standard deviation.

We concatenate these vectors to get a summary of the query set.

*Reveal the final routing network.*

In the full model, we also combine information across TabPFN ensemble members.

We then pass the result through a small neural network.

Finally, the router produces three scores, one for each expert.

We apply softmax to convert them into weights.

*Click to show the Top-2 weights.*

Then we keep only the two largest weights and normalize them again.

The result is a sparse mixture.
-->

---
routeAlias: tabcon-training-roadmap
clicks: 0
---

# Our Contributions

<TabConContributions :active="3" />

<!--
*Suggested time: 30 seconds*

Now we have introduced the model architecture.

We have three residual experts and a router that combines them.

We divide training into several stages.

The main idea is to first train the residual experts, and then train the router.
-->

---
clicks: 3
class: detail-slide
---

<div class="eyebrow">3. A new training paradigm for tabular foundation models</div>

# First Pretrain the Specialists, Then Post-Train the Router

<TrainingStages />
<div class="detail-message">RL post-training may be unnecessary for prediction but essential for complex scientific tasks involving statistical inference.</div>

<!--
*Suggested time: 2 minutes*

This slide shows our complete training process.

We divide it into four stages.

*Start with the Global stage, which is already visible.*

In the first stage, we train the Global Head.

We generate many synthetic datasets.

For each dataset, we know the true regression mean.

We use the frozen TabPFN model to calculate the point estimate.

Then we calculate the estimation residual and use it to train the Global Head.

In our setup, this stage uses 50 thousand synthetic datasets.

*Click to reveal the specialists.*

In the second stage, we train the two specialist heads.

We first look at how the Global Head performs on different datasets.

Some datasets have lower coverage than our target.

Others have higher coverage.

We use this information to train the Expansion and Shrinkage heads on different groups of datasets.

After this stage, all three residual experts are ready.

*Click to reveal router SFT.*

In the third stage, we train the router using supervised fine-tuning, or SFT.

At this point, the three experts are frozen.

Only the router is trained.

It learns how to combine the experts to predict the estimation residual distribution.

*Click to reveal router RL.*

Finally, in the fourth stage, we use reinforcement learning to further improve the router.

This is important because our final goal is not only to predict residuals.

We want confidence intervals with good coverage and short lengths.

So we use rewards that directly measure these properties.

Now, I will explain each stage in more detail.
-->

---
clicks: 0
class: detail-slide global-training-slide
---

<div class="eyebrow">3.1. Training the Global Head</div>

# Similar Training, New Target: From Outcomes to Residuals

<div class="training-pipeline"><div><span>Simulate a dataset</span><b>Ground truth <MathTex tex="f(x)" /></b></div><i>→</i><div><span>Frozen regression head</span><b>Estimate <MathTex tex="\widehat f(x)" /></b></div><i>→</i><div><span>Supervised target</span><b><MathTex tex="r(x)=\widehat f(x)-f(x)" /></b></div></div>
<div class="loss-display"><MathTex tex="\mathcal{L}_{G}=\mathrm{NLL}+0.20\,\mathrm{CRPS}" /></div>
<div class="two detail-pair"><section><h3 class="blue">NLL (negative log-likelihood)</h3><p>Following TabPFN-3, we discretize all variables, making NLL minimization equivalent to cross-entropy minimization.</p></section><section><h3 class="violet">CRPS (continuous ranked probability score)</h3><p>CRPS generalizes absolute prediction error to predictive distributions.</p></section></div>


<!--
*Suggested time: 2 minutes*

Let's start with the Global Head.

The training process is very similar to the original TabPFN training process.

But we change the prediction target.

Original TabPFN learns to predict outcomes.

Our Global Head learns to predict estimation residuals.

As shown in this figure, we first generate a synthetic dataset.

Because we control the data generation process, we know the true mean.

Then, we use the frozen regression model to calculate an estimate.

The difference between the estimate and the true mean gives us the residual.

This is our training label.

Now, we want the Global Head to learn the full distribution of these residuals.

We use two loss functions.

The first one is **negative log-likelihood**, or NLL.

Following TabPFN, we divide the possible residual values into many bins.

The model outputs a probability for each bin.

NLL encourages the model to assign a high probability to the bin containing the true residual.

The second loss is called **CRPS**.

CRPS is another way to evaluate a predicted distribution.

The important difference is that CRPS also takes the order of the bins into account.

It compares the predicted cumulative distribution with the observed residual, accounting for how far probability mass lies from that residual.

So, we combine NLL and CRPS.

We minimize this loss by updating only the Global Head.

After training, the Global Head can predict a residual distribution for a new dataset.

But it may still give intervals that are too wide or too narrow.

So we introduce two specialist heads.
-->

---
clicks: 0
class: detail-slide
---

<div class="eyebrow">3.2. Training the Specialists</div>

# Define Coverage Scores to Cluster DGPs

<CoverageThresholds />


<!--
*Suggested time: 2 minutes*

Before training the specialists, we need to answer one question.

How can we know which datasets need wider intervals, and which ones need shorter intervals?

To do this, we define a **coverage score**.

First, we take a set of new synthetic datasets.

For each dataset, we use the trained Global Head to construct confidence intervals.

So we can directly calculate the coverage of the Global Head.

In our method, we measure coverage at several coverage levels and combine their differences into one score.

A negative score means the model tends to undercover.

A positive score means it tends to overcover.

Now, we calculate these scores across many synthetic datasets.

This gives us a distribution of coverage scores, as shown in the figure.

We then choose two thresholds.

The first threshold is the one-third quantile.

The second threshold is the two-thirds quantile.

We save these two thresholds.

In the next stage, we will use them to decide which specialist receives supervised training on each dataset.
-->

---
clicks: 2
class: detail-slide specialist-training-slide method-slide
---

<div class="eyebrow">3.2. Training the Specialists</div>

# Use Different Data Subsets to Train Different Specialists

<div class="small">For each new training DGP, compute its coverage score <MathTex tex="S" /> and compare it with the quantile thresholds <MathTex tex="s_1" /> and <MathTex tex="s_2" />. If</div>

<SpecialistTraining />


<!--
*Suggested time: 2 minutes 10 seconds*

Now, let's see how we train the two specialist heads.

First, we initialize both specialists using the trained Global Head.

So, at the beginning, all three heads produce the same distribution.

Then, we train the specialists using different groups of datasets.

For each new synthetic training dataset, we calculate its coverage score using the Global Head.

Then, we compare this score with the two thresholds from the previous slide.

Let's consider three cases.

*Show the low-score case.*

In the first case, the coverage score is at or below the first threshold.

This places the dataset in the lower-coverage group.

So, we use this dataset to train the Expansion Head.

Its goal is to learn a residual distribution that may help improve coverage.

For the other specialist, we use a KL loss to keep its output close to the Global Head.

*Show the high-score case.*
In the second case, the coverage score is at or above the second threshold.

This places the dataset in the higher-coverage group.

So, we use this dataset to train the Shrinkage Head.

Its goal is to learn a distribution that may give shorter intervals while keeping enough coverage.

Again, the other specialist is kept close to Global using the KL loss.

*Show the middle-score case.*

In the third case, the score is between the two thresholds.

These datasets do not strongly belong to either extreme group.

So, we use the KL loss for both specialists.

This helps them stay close to the original Global Head.

An important detail is that Expansion and Shrinkage are not just fixed rules for making intervals wider or shorter.

They are two neural networks that learn different residual distributions.

After this stage, we have three trained experts.

The Global Head learns general uncertainty.

The Expansion Head focuses on undercoverage cases.

And the Shrinkage Head focuses on overcoverage cases.

Now we need to train the router to combine them.
-->

---
clicks: 0
class: detail-slide
---

<div class="eyebrow">3.3. SFT-based Router training</div>

# Construct the Supervised Learning Loss

<RouterSFT />

<!--
*Suggested time: 2 minutes 10 seconds*

Now, let's move to the router.

The first step is supervised fine-tuning, or SFT.

At this stage, all three residual heads are frozen.

Only the router is trainable.

The router takes the embeddings of the current dataset and produces three scores.

We convert these scores into weights using softmax.

But we do not use all three experts in the final mixture.

Instead, we use Top-2 routing.

Let me explain this with an example.

Suppose the router produces three weights.

The Global Head gets 0.25.

The Expansion Head gets 0.60.

And the Shrinkage Head gets 0.15.

We keep the two largest weights.

So, we keep Global and Expansion, and set the Shrinkage weight to zero.

Then, we normalize the remaining two weights.

The final weights are about 0.29 and 0.71.

We use these weights to combine the residual distributions from the two selected heads.

We also use NLL and CRPS to evaluate the mixture distribution.

Then, we update the router to reduce this loss. We use a straight-through gradient estimator: the forward mixture is Top-2, while the backward pass uses a dense-softmax proxy gradient.

After SFT, the router has learned a reasonable way to combine the experts.
-->

---
clicks: 0
class: detail-slide method-slide
---

<div class="eyebrow">3.4. RL-based Router training</div>

# Why RL after SFT?

<WhyRouterRL />


<!--
*Suggested time: 1 minute 40 seconds*

Why do we need reinforcement learning after SFT?

The reason comes from the difference between our training loss and our final goal.

During SFT, we use NLL and CRPS.

These losses measure how well the model predicts the distribution of estimation residuals.

But our final goal is not simply to predict a good distribution.

We want confidence intervals that have the right coverage and are as short as possible.

These are related goals, but they are not exactly the same.

This is why we introduce reinforcement learning.

Instead of only measuring the quality of the full residual distribution, we directly evaluate the confidence intervals.

We ask two questions.

First, how close is the coverage to our target?

Second, how short is the interval?

We combine these measures into a reward.

Then, we use reinforcement learning to update the router.

RL starts from the SFT model and further improves the routing decisions.

Our goal is to make the training objective closer to the actual statistical task.
-->

---
clicks: 0
routeAlias: rl-details
class: detail-slide method-slide
---

<div class="eyebrow">3.4. RL-based Router training</div>

# RLOO: A Leave-One-Out Version of GRPO

<RLOODemo />


<!--
*Suggested time: 2 minutes 30 seconds*

Now, let's look at the reinforcement learning algorithm.

We use RLOO, which stands for REINFORCE Leave-One-Out.

It is closely related to group-based policy gradient methods, such as GRPO.

The basic idea is to try several routing choices on the same dataset, compare their rewards, and use these comparisons to improve the router.

Let's look at the example.

We start with one synthetic dataset.

For this dataset, the router produces a distribution over possible routing choices.

During RL training, we add some random noise to the router scores.

This allows us to sample different routing choices.

Different choices can select different pairs of experts or different mixture weights.

So, we get different confidence intervals for the same dataset.

Here, we have four candidate choices.

Their rewards are 0.2, 0.8, minus 0.1, and 0.5.

A higher reward means a better result under our reward function.

Now, how do we decide which action should be encouraged?

We calculate an advantage.

In RLOO, the baseline for one candidate is the average reward of all the **other** candidates.

This is why it is called leave-one-out.

For example, let's consider candidate B.

Its reward is 0.8.

The other three rewards are 0.2, minus 0.1, and 0.5.

Their average is 0.2.

So, the advantage of B is 0.8 minus 0.2, which equals positive 0.6.

This means candidate B performs better than the other choices on this dataset.

We use these advantages to update the router.

The basic idea is to increase the probability of routing choices with positive advantages, and decrease the probability of choices with negative advantages.

The policy gradient is calculated using the log probability of the sampled router scores.

In our actual training, we use 16 sampled routing choices per task.
-->

---
class: detail-slide
---

<div class="eyebrow">3.4. RL-based Router training</div>

# Six Reward Components, Three Types

<RewardComponents />
<div class="source"><a href="https://arxiv.org/html/2609.33114v1#A2.SS2">Appendix B.2 · Post-training reward function</a>.</div>

<!--
*Suggested time: 1 minute 50 seconds*

Now, the next question is: how do we define a good reward for confidence intervals?

We use six reward components, divided into three groups.

The first group focuses on **interval precision**.

We want shorter intervals, but not at the cost of very poor coverage.

The first component is WIL. It encourages shorter intervals compared with the Global Head.

The second component is WIS. This score considers both interval width and whether the true target falls outside the interval.

If the interval misses the true value by a large amount, it receives a larger penalty.

The second group focuses on **coverage calibration**.

The coverage score penalizes intervals when their empirical coverage is too far from the target.

The tail balance term checks the missed targets below and above the interval separately.

For example, even if the total coverage looks good, most of the missed targets may be above the interval.

We also want to avoid this problem.

The third group provides **extra safeguards**.

CVaR puts more focus on datasets with especially severe undercoverage.

The excess-width penalty activates only when widening exceeds an allowed budget relative to the Global Head's intervals.

Together, these reward components help the router learn a better balance between coverage and interval length.

Of course, these rewards do not give a strict coverage guarantee.

They provide training signals that encourage better confidence intervals.
-->

---
class: detail-slide ownership-slide
---

<div class="eyebrow">3. Model training (summary) </div>

# Which Model Is Optimized at Each Stage?

<table class="ownership-table">
<thead><tr><th>Model</th><th>Pretraining</th><th>Pretraining</th><th>SFT</th><th>RL</th></tr></thead>
<tbody>
<tr><td>Regression head</td><td class="frozen-cell" title="Frozen">❄️</td><td class="frozen-cell" title="Frozen">❄️</td><td class="frozen-cell" title="Frozen">❄️</td><td class="frozen-cell" title="Frozen">❄️</td></tr>
<tr><td>Global head</td><td class="learned-cell" title="Trained">🔥</td><td class="frozen-cell" title="Frozen teacher">❄️</td><td class="frozen-cell" title="Frozen">❄️</td><td class="frozen-cell" title="Frozen">❄️</td></tr>
<tr><td>Expansion</td><td title="Not used yet">—</td><td class="learned-cell" title="Trained">🔥</td><td class="frozen-cell" title="Frozen">❄️</td><td class="frozen-cell" title="Frozen">❄️</td></tr>
<tr><td>Shrinkage</td><td title="Not used yet">—</td><td class="learned-cell" title="Trained">🔥</td><td class="frozen-cell" title="Frozen">❄️</td><td class="frozen-cell" title="Frozen">❄️</td></tr>
<tr><td>Router</td><td title="Not used yet">—</td><td title="Not used yet">—</td><td class="learned-cell" title="Trained">🔥</td><td class="learned-cell" title="Trained">🔥</td></tr>
</tbody>
</table>
<div class="small" style="text-align:center;margin-top:12px">“—” denotes not used during training.</div>

<!--
*Suggested time: 1 minute 20 seconds*

This slide summarizes which parts of TabCon are trained at each stage.

I think this is important because we do not train the whole model at the same time.

First, the pretrained TabPFN backbone and regression head are always frozen.

We never update these parameters.

In the first training stage, we only update the Global Head.

In the second stage, we freeze Global and train the Expansion and Shrinkage heads.

Then, we freeze all three residual experts.

During SFT, we update only the router.

And during RL, we continue updating only the router.

So, the training process is very clear.

We first learn how estimation errors behave.

Then, we learn how to combine the different error distributions.

And finally, we use RL to improve the quality of the resulting confidence intervals.

At deployment time, all model parameters are frozen.

A new dataset only changes the model's outputs, including the mixture weights produced by the router. Its learned parameters stay fixed.

There is no additional training.

This is the key advantage of amortized inference.
-->

---
routeAlias: tabcon-experiments-roadmap
clicks: 0
---

# Our Contributions

<TabConContributions :active="4" />

<!--
*Suggested time: 30 seconds*

Now, we have finished the methodology.

We have introduced how TabCon learns estimation residuals, how the three experts work, and how we train the router using SFT and RL.

Next, I want to show you our experimental results.

We focus on three main questions.

Does TabCon achieve coverage close to the target?

Can it produce relatively short intervals?

And how much computation time can it save?
-->

---
routeAlias: evidence
---

<div class="eyebrow">4. Strong empirical performance</div>

# Three benchmarks, one known target

<EvaluationDesign />

<!--
*Suggested time: 1 minute 40 seconds*

To evaluate confidence intervals, we need to know the true regression mean.

This is not easy with real-world datasets, because the true mean is usually unknown.

So, we use three benchmark designs.

The first one is the **standard synthetic benchmark**.

We generate datasets from different regression models, feature distributions, and noise settings.

We consider both in-distribution and out-of-distribution cases.

For the in-distribution setting, the evaluation datasets are new, but they come from the same broad family of data-generating processes used in training.

For the out-of-distribution setting, we use function families that were not seen during training.

This helps us test whether TabCon can generalize.

The second benchmark is the **stress-test benchmark**.

Here, we create more challenging data settings.

For example, we consider very low noise, high noise, heavy-tailed noise, and different types of regression functions.

The goal is to see whether our method can still work under difficult conditions.

The third benchmark is **CC18**.

Here, we take input features from 13 real datasets.

But we generate the outcomes using known regression functions.

So, this benchmark has realistic input features, while still allowing us to calculate the true mean.

For all these benchmarks, we evaluate two main metrics.

The first is coverage probability.

We want it to be close to our nominal target of 95 percent.

The second is average interval length.

We want intervals to be short, as long as the coverage remains close to the target.
-->

---
---

<div class="eyebrow">Results · 95% nominal level</div>

# Coverage and precision belong together

<BenchmarkResults />

<!--
*Suggested time: 2 minutes 20 seconds*

Now, let's look at the main results.

This figure compares TabCon with several baseline methods.

As I mentioned earlier, we need to consider coverage and interval length together.

A very short interval is not useful if it misses the true value too often.

Let's first look at the standard in-distribution setting.

TabCon achieves about **95.5 percent coverage**.

This is very close to our 95 percent target.

At the same time, its average interval length is about 2.68.

Now compare this with the original prediction interval from TabPFN.

Its average length is about 4.03.

So, TabCon produces a much shorter interval in this benchmark.

Of course, the original prediction interval is designed for a new outcome, while our confidence interval targets the regression mean.

We include it as a useful reference, rather than treating them as exactly the same statistical problem.

Another interesting baseline is bootstrap.

Bootstrap produces much shorter intervals here, but its coverage is only about 59 percent.

This is far below our target.

So, the short interval alone is not enough.

*Switch to the OOD setting.*

Now, let's look at the out-of-distribution results.

TabCon still achieves about **95.3 percent coverage**.

This suggests that the model can generalize to the unseen function families in this benchmark.

*Switch to the stress-test setting.*

In the stress-test setting, the average coverage is about **95.6 percent**.

Again, this is close to the target.

*Switch to the CC18 setting.*

Finally, on CC18, TabCon achieves about **96.5 percent coverage**.

Its average interval length is about 1.07.

The original TabPFN prediction interval is much wider, with an average length of about 2.65.

These results show that TabCon performs well across several different benchmark settings.

One thing to keep in mind is that these are average results.

Some individual datasets still have undercoverage.

So we do not claim that TabCon guarantees 95 percent coverage for every dataset.

Our main finding is that it gives a good balance between coverage and interval length across these evaluations.
-->

---
---

<div class="eyebrow">Results · Computation</div>

# A fast interval for a new dataset

<RuntimeChart />
<div class="callout"><b>0.21 s</b> for TabCon versus <b>10.71 s</b> for 50 bootstrap refits in this setting.</div>

<!--
*Suggested time: 1 minute 10 seconds*

Now, let's look at the computation cost.

One of the main reasons for using a foundation model is that we can reuse what it learned during training.

This is also an important advantage of TabCon.

For a new dataset, we only need to run the pretrained backbone, residual heads, and router.

We do not need to train a new model or run repeated bootstrap samples.

Here, we compare the inference time of different methods.

In this setting, TabCon takes about **0.21 seconds**.

In comparison, bootstrap with 50 samples takes about **10.71 seconds**.

So, TabCon is about **50 times faster**.

And remember that we only use 50 bootstrap samples.

In practice, bootstrap methods may use many more samples.

Of course, TabCon requires computation during its original training.

But once the model is trained, we can reuse it across many new datasets.

This is exactly the benefit of amortized statistical inference.
-->

---
class: closing-slide
---

<div class="eyebrow">Summary</div>

# What do we want the interval to describe?

<div class="two mt-9">
<div><div class="text-sm blue font-bold uppercase tracking-widest">A future observation</div><h2 class="mt-4 !text-4xl">Predictive<br>uncertainty</h2><p class="text-lg text-slate-500 mt-5">PFNs learn to predict from context.</p></div>
<div><div class="text-sm teal font-bold uppercase tracking-widest">An unknown average</div><h2 class="mt-4 !text-4xl">Estimation<br>uncertainty</h2><p class="text-lg text-slate-500 mt-5">TabCon learns to construct intervals for the mean.</p></div>
</div>
<div class="closing-line">Confidence intervals tell us how precisely the data locate the average.</div>
<div class="mt-6 text-sm"><a href="https://arxiv.org/abs/2609.33114">Read the paper · arXiv:2609.33114</a></div>


<!--
*Suggested time: 1 minute*

Finally, let me summarize this work.

The main question of our paper is:

**Can we use tabular foundation models for statistical inference, instead of only prediction?**

We focus on confidence interval construction.

The key difference is the type of uncertainty we want to measure.

For prediction, we care about a future outcome.

This includes the noise in the outcome itself.

But for statistical inference, we care about how precisely we can estimate an unknown mean.

These are two different targets.

Our method, TabCon, learns the distribution of estimation residuals and uses it to construct confidence intervals.

We introduce three residual experts and a sparse router.

We train the experts using supervised learning, and then improve the router using reinforcement learning.

Our experiments show that TabCon can achieve coverage close to the target, while producing relatively short intervals and reducing inference time.

More broadly, we hope this work opens up a new direction: using foundation models not only for prediction, but also for statistical inference.

**Thank you for listening. I would be happy to take any questions.**
-->
