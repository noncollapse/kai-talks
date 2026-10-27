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

<div class="eyebrow">Tabular foundation models · Statistical inference</div>
<h1 class="cover-title">Can Tabular Foundation Models<br><span>Amortize Statistical Inference?</span></h1>
<div class="cover-subtitle">Learning how precisely we know the average</div>
<div class="cover-authors"><b>Kai Ye</b> · Shijin Gong · Hongyi Zhou<br>Valentina Zangirolami · Chengchun Shi</div>
<div class="cover-bottom"><span>LSE · Stats-Powered AI</span><a href="https://arxiv.org/abs/2609.33114">arXiv:2609.33114</a></div>


<!--
The central question is whether we can learn a reusable procedure for uncertainty about an estimated average, much as a PFN learns a reusable prediction procedure. We will build the distinction visually before discussing the model. Source: https://arxiv.org/abs/2609.33114
-->

---
routeAlias: first-results
class: result-preview-slide
---

<div class="eyebrow">A first look · Stress tests</div>

# TabCon: reliable coverage, shorter intervals

<StressPreview />
<div class="source">14 methods · Original paired stress tasks · Coverage against the saved latent oracle · pp = percentage points.</div>

<!--
Open with the result before explaining how it is achieved. These are the ten stress settings from the supplied paper figure; regular_control is excluded. The six original methods use the paper numeric results, verified against the original figure's source SHA256 and the frozen main/Wald summary JSONs. GRF, Local Linear Forest, BDE, RF-IJ, DRF, BRAT-P, BRAT-D, and RF-U are additional completed evaluations on the same 1,280 recovered and verified task realizations, including all 155,520 original query points. These new methods use author/package implementations with documented compatibility adaptations and fixed configurations; all eight completed all tasks with finite outputs; this numerical gate does not certify training stability. Linear means Linear-Wald-HC3; RFF means RFF-Wald-HC3. Both are custom statistical implementations, not official-package baselines. Linear applies context-only PCA when necessary; RFF uses at most 64 random features. Their HC3/z formulas are correct, but ill-conditioned designs cause numerical sensitivity and six Linear replay discrepancies are documented. Historical points are retained. AMP (CrI) denotes a paper-based approximate martingale-posterior credible interval, not an ordinary frequentist CI; its author-code endpoint returned HTTP 401 during the audit, so exact source equivalence has not been established. TabPFN (PI) is the native predictive interval, evaluated here against the saved latent oracle rather than a future noisy outcome. This is a reference baseline with a different native target, not a claim that TabCon dominates every confidence-interval procedure. Code inspection showed that the Generator V2 oracle T(Z) is not guaranteed to equal E[Y|observed X]; do not describe this stress figure as independently verified conditional-mean coverage.

TabCon's unweighted average coverage across the ten settings is 0.95614013671875 (range approximately 0.9400–0.9842). Its mean interval length is 1.8581469892765767, compared with 3.209065453414952 for native TabPFN prediction intervals. The displayed 42% reduction is 1 minus the ratio of these arithmetic means, not a mean of per-setting percentage reductions. Every setting has 128 tasks, so equal-setting and equal-task weighting coincide. Short intervals alone are insufficient: Bootstrap is shorter but substantially undercovers in these results. Neither a universal coverage guarantee nor significance is asserted.

This scatter preview uses arithmetic mean interval length on a log x axis and signed per-setting coverage deviations from 95% on a linear y axis, in percentage points. Each point shows one method's average deviation; no range bars are displayed. Positive means overcoverage, negative means undercoverage, and closeness to zero is desirable. TabCon's mean deviation is +0.614013671875 pp, with a range from -1.0028076171875 to +3.4161376953125 pp; four settings under-cover and six over-cover. AMP also has mixed directions (one under, nine over). These per-setting ranges are not displayed: opposite deviations can cancel in the plotted mean. The old Pareto staircase and lower-left-is-better annotation are removed because signed coverage should be close to zero rather than simply minimized. Length is averaged in the original outcome units without normalization, so high-scale settings have greater influence on mean length. The original radar remains available as stress-opening-radar.svg. figures/scripts/draw_stress_tradeoff.py regenerates this preview and its summary JSON; the original result table and hash remain unchanged.

The first three additions are exported from complete per-query predictions by figures/scripts/export_additional_ci.py. Their numeric table and provenance are figures/data/stress_additional_ci_results.csv and stress_additional_ci_provenance.json. RF-IJ and DRF are exported and independently checked by figures/scripts/export_extra_ci.py, with separate stress_extra_ci_results.csv and stress_extra_ci_provenance.json. RF-IJ uses ranger 0.18.0 with 2,000 trees and native infinitesimal-jackknife standard errors. Its mean coverage is 0.53057861328125 and mean interval length is 0.7261888936328144. DRF uses the official drf 1.3.1 native uncertainty API with 6,000 honest trees, 100 CI groups, exact group-weighted means and their sample variance. Its mean coverage is 0.5805023193359375 and mean interval length is 0.7703466374315616. All 1,280 tasks and 155,520 queries passed per-query verification on Beast and locally. Its intervals are short but substantially undercover this saved target; no universal coverage conclusion is asserted. BART and GP were cancelled by the user on 27 October 2026, who excluded Bayesian credible-interval baselines. Their pilot and partial results are not plotted. DeepLR was cancelled by the user and is excluded. BDE mean length is strongly influenced by high_noise__053, whose mean interval length is about 16,948.6; one bootstrap-retrained network produced extreme predictions. This finite result is retained without trimming and flagged on the slide. The existing Bootstrap comparator is TabPFN mean predictions across bootstrap resamples of context rows, distinct from BDE's parametric bootstrap retraining. Both target uncertainty in the regression function, not future-outcome noise. The archived six-method radar is unchanged. See experiments/ci_baselines/PROTOCOL.md, PROTOCOL_EXTRA.md and PROTOCOL_MODERN.md for configurations, data pairing and limitations.

The latest additions are exported by figures/scripts/export_modern_ci.py into stress_modern_ci_results.csv and stress_modern_ci_provenance.json after all saved endpoints, standard errors, task/config hashes and metrics were independently checked remotely and locally. Each method uses all 1,280 tasks / 155,520 queries without trimming. BRAT-P: mean coverage 0.1536224365234375, mean length 0.2074908501043721. BRAT-D: 0.2644775390625 and 0.2666031319457618. RF-U: 0.6453704833984375 and 0.9489549325520208. These are results of fixed author README configurations on this benchmark, not tuned optimal performance or universal comparisons.

BRAT-P and BRAT-D use unmodified Boulevard 0.1.0a1, pinned commit ec0a4ede4155519b70fbca65ac73f9ece64da276. The interval mode is explicitly confidence. The package settings are not exact replications of the paper experiments: current ParallelBooster omits the paper’s sequential warm-start and the package uses histogram-cell inference rather than the paper experiment’s Nyström approximation. All context observations are retained for fitting; the documented prepare_inference() fallback estimates residual variance on the training data. The author README prefers held-out variance estimation, so optimistic training-residual estimates remain a limitation. No query outcomes or oracle residuals are used to fit or calibrate intervals. RF-U uses RLT 6.1.1, pinned commit d83a648a15591bbd4f057322dfdea7a75f056992, with the matched-sample U-statistic variance estimator. All 1,280 tasks returned finite nonnegative variance estimates at the original 10,000 trees; none triggered the wrapper retry. Audit correction: official RLT floors negative matched variances at zero before returning them, so this gate cannot detect pre-floor negatives. There are 4,040 saved zero-width intervals across 764 tasks, all retained. No claim is made that every raw variance estimate was positive.

Inferable EBM was removed from this comparison at the user’s request on 27 October 2026. Its raw results are retained in the experiment archive. The plot now contains fourteen methods on a continuous log x-axis. See experiments/ci_baselines/EXPERIMENT_AUDIT.md and its three independent evidence reports for the per-method implementation audit, configuration differences and remaining limitations.
-->

---
routeAlias: roadmap
---

<div class="eyebrow">The route</div>

# Prediction, uncertainty, then TabCon

<div class="roadmap">
<a href="#/pfn"><span>01</span><div><b>PFNs</b><p>A model that learns across datasets</p></div></a>
<a href="#/two-questions"><span>02</span><div><b>Two kinds of uncertainty</b><p>A future outcome versus the underlying average</p></div></a>
<a href="#/tabcon"><span>03</span><div><b>TabCon</b><p>Learning to construct confidence intervals</p></div></a>
<a href="#/evidence"><span>04</span><div><b>The evidence</b><p>Coverage, interval length and computation</p></div></a>
</div>


<!--
The first half develops the intuition. The second half connects that intuition to the learning target, model architecture and evidence. The section links are clickable.
-->

---
routeAlias: tabular-timeline
class: timeline-slide
---

<div class="eyebrow">Before PFNs · A development timeline</div>

# How tabular learning evolved

<TabularTimeline />
<div class="source">Sources: <a href="https://doi.org/10.1109/TPAMI.2026.3657217">Jiang et al., TPAMI (2026)</a> · <a href="https://www.jmlr.org/papers/v23/21-0585.html">DRF</a> · <a href="https://doi.org/10.1073/pnas.2310151122">FIGS</a> · <a href="https://xgboost.readthedocs.io/en/stable/changes/v3.2.0.html">XGBoost 3.2</a> · <a href="https://arxiv.org/abs/2112.10510">PFNs</a> · <a href="https://github.com/PriorLabs/TabPFN/blob/main/CHANGELOG.md">TabPFN releases</a> · <a href="https://proceedings.mlr.press/v306/qu26a.html">TabICL v2</a> · <a href="https://research.google/blog/introducing-tabfm-a-zero-shot-foundation-model-for-tabular-data/">TabFM</a>.</div>

<!--
A single, fully visible timeline with four connected research directions. Solid lines group milestones within a direction. Dashed arrows show shared ideas or changes in training strategy, not direct paper-to-paper ancestry. Hovering a dashed connector or focusing it with the keyboard highlights its two related routes. These interactions do not hide content or require slide clicks.

Classical ML has an expanded pre-2016 inset: linear/logistic regression, kNN, SVM, CART, AdaBoost, random forests and gradient boosting. The inset compresses early history rather than assigning precise first-publication dates to these broad families. XGBoost (2016), LightGBM/CatBoost (2017) and NGBoost (ICML 2020) sit on the modern timeline. NGBoost extends gradient boosting to probabilistic prediction; it is not an inference method for the regression mean like TabCon. After NGBoost, this route continues with PGBM (KDD 2021), which efficiently produces probabilistic predictions with one tree ensemble; Distributional Random Forests (JMLR 2022), which estimate joint conditional distributions; and FIGS (PNAS 2025), which grows interpretable sums of trees. FIGS had a 2022 preprint; this timeline uses its journal publication year, consistent with the venue-year convention elsewhere. The 2026 endpoint is explicitly a software release: XGBoost 3.2 improves multi-target tree support and GPU external-memory training. These are parallel advances in probabilistic prediction, interpretability and scalable learning, not a chain of models replacing one another. The selected milestones do not imply that years without a label had no research.

The previously empty left region now contains general-ML foundations for each route: MLPs/autoencoders for learned representations; unsupervised pretraining followed by fine-tuning; and multitask/meta-learning for learning from related tasks. These are conceptual roots, not claims that all later models descend directly from a particular early method. Representative primary sources are Bengio et al. (NIPS 2006), Caruana (1997), and Hochreiter et al. (2001).

The two upper bridges are concrete architectural connections: NODE makes oblivious decision-tree ensembles differentiable and trains them end to end; TabR combines a neural network with a learned nearest-neighbor retrieval component. The latter applies to TabR, not the adjacent RealMLP label. Likewise, the tree bridge refers to NODE, not TabTransformer, which shares its 2020 milestone.

The two lower bridges describe changes in the unit or role of training. Neural representation learning can be used for pretraining followed by downstream adaptation. The PFN approach instead pretrains across sampled prediction tasks, learning a reusable prediction procedure. The arrow from the pretraining route to PFNs is conceptual, not a claim that PFNs derive from VIME, SubTab or any particular model shown above. The foundation-model route includes HyperFast as another approach. All model labels and nodes on this route use the same blue; green distinguishes TabCon as the focus of this talk.

The timeline now extends through October 2026. In addition to the survey's original examples, it includes TabPFN 2.5 (November 6, 2025), TabPFN 2.6 (March 24, 2026), TabPFN 3 (May 12, 2026), TabPFN 3.5 (September 15, 2026), TabICL v2 (ICML 2026), and Google's TabFM (June 30, 2026). These dates were verified against official reports, release notes and proceedings on October 26, 2026. Model names follow the official release naming; the model often called TabPFN v3 is styled TabPFN-3 in its report. The green TabCon branch explicitly says "via TabPFN 3"; the other 2026 releases are parallel developments.

Earlier examples retain the verified survey years. PFNs are listed by their 2022 conference year (preprint 2021); TabPFN is ICLR 2023; TabPFN v2 is Nature 2025; TabICL is ICML 2025. The full survey catalog remains in figures/specs/tabular-timeline-data.json, and the added releases and early conceptual roots are sourced in figures/specs/timeline-updates-2026.json. This remains a selection of milestones, not an exhaustive bibliography.

TabCon extends the reuse question from prediction to statistical inference about the regression mean. Its position identifies the destination of this talk, not a claim that it supersedes the displayed predictive methods.

New release sources: https://priorlabs.ai/technical-reports/tabpfn-3 ; https://github.com/PriorLabs/TabPFN/blob/main/CHANGELOG.md ; https://proceedings.mlr.press/v306/qu26a.html ; https://research.google/blog/introducing-tabfm-a-zero-shot-foundation-model-for-tabular-data/ .
Early conceptual sources: https://proceedings.neurips.cc/paper/2006/hash/5da713a690c067105aeb2fae32403405-Abstract.html ; https://doi.org/10.1023/A:1007379606734 ; https://doi.org/10.1007/3-540-44668-0_13 ; https://www.bioinf.jku.at/publications/older/1504.pdf .

Post-2020 classical milestones: https://arxiv.org/abs/2106.01682 ; https://www.jmlr.org/papers/v23/21-0585.html ; https://doi.org/10.1073/pnas.2310151122 ; https://xgboost.readthedocs.io/en/stable/changes/v3.2.0.html .

Primary sources for the new connections and NGBoost: https://iclr.cc/virtual_2020/poster_r1eiu2VtwH.html ; https://proceedings.iclr.cc/paper_files/paper/2024/hash/4ef594af0d9a519db8fb292452c461fa-Abstract-Conference.html ; https://proceedings.mlr.press/v119/duan20a.html ; https://arxiv.org/abs/2112.10510 .
Other sources: https://doi.org/10.1109/TPAMI.2026.3657217 ; https://github.com/LAMDA-Tabular/Tabular-Survey ; https://openreview.net/forum?id=cp5PvcI6w8_ ; https://www.nature.com/articles/s41586-024-08328-6 ; https://proceedings.mlr.press/v267/qu25d.html ; https://arxiv.org/abs/2609.33114 .
-->

---
routeAlias: pfn
clicks: 2
---

<div class="eyebrow">01 · PFNs</div>

# Prior-Data Fitted Networks

<p class="lead">A Transformer can learn a prediction procedure across synthetic datasets.</p>

<div class="two mt-8">
<div class="panel"><div class="eyebrow">The familiar workflow</div><h3>One dataset</h3><p>Fit a model.<br>Use it to predict new rows.</p><div class="small mt-6">Learning happens on this dataset.</div></div>
<div v-click="1" class="panel" style="border-color:#bac9ff;background:#f1f4ff"><div class="eyebrow">The PFN idea</div><h3>Many training tasks</h3><p>Learn a network that can read a new dataset and make predictions.</p><div class="small mt-6">The dataset becomes the context.</div></div>
</div>
<div v-click="2" class="callout mt-6">Like in-context learning, with <b>rows of a table</b> as examples.</div>
<div class="source">Müller et al., <a href="https://arxiv.org/abs/2112.10510">Transformers Can Do Bayesian Inference</a>; Hollmann et al., <a href="https://doi.org/10.1038/s41586-024-08328-6">Nature, 2025</a>.</div>

<!--
PFN means Prior-Data Fitted Network. The prior is a distribution over possible data-generating tasks. In the standard use we discuss, training happens across simulated tasks, and the new dataset is supplied as context rather than used for gradient updates. Fine-tuning variants exist, but they are not needed for this explanation. Sources: https://arxiv.org/abs/2112.10510 and https://doi.org/10.1038/s41586-024-08328-6
-->

---
clicks: 2
---

<div class="eyebrow">PFN · Training</div>

# Practice on many possible worlds

<p class="lead">Generate tables, hide outcomes, and learn to predict them.</p>

<PFNFlow mode="train" />
<div class="source">Schematic training tasks. PFN background: <a href="https://arxiv.org/abs/2112.10510">Müller et al.</a> and <a href="https://doi.org/10.1038/s41586-024-08328-6">Hollmann et al.</a></div>

<!--
Advance twice. First hide a target, then show the training signal. The formula is the prior-data negative log-likelihood: q_theta is the network's predictive distribution, D is the observed context, and (x,y) is a held-out row from the same simulated task. The expectation averages over tasks drawn from the training prior and their sampled context/query rows; in practice this is estimated using a batch of negative log-likelihood terms. The hidden y is used to compute the loss, not supplied as an input when predicting it. For continuous outcomes, q_theta denotes a predictive density. The same network sees many relationships, noise levels and dataset sizes. This is where the reusable prediction procedure is learned. The tiny datasets are explanatory sketches, not experiments. The PFN approximates Bayesian posterior prediction under its synthetic task prior, rather than an arbitrary universal predictive distribution. Source: https://arxiv.org/html/2112.10510#S3
-->

---
clicks: 2
---

<div class="eyebrow">PFN · Deployment</div>

# A new table becomes the prompt

<p class="lead">Observed rows + a query row give a distribution over the missing outcome.</p>

<PFNFlow mode="predict" />
<div class="source">Illustrative house-price table, prices in £k. Standard in-context use of a pretrained PFN; no gradient updates on this dataset.</div>

<!--
Advance to send the new table into the frozen model, then reveal a predictive distribution. In regression, the output can express several plausible values of the next outcome. The values and density here are illustrative and are not outputs from a fitted TabPFN model. Source for the workflow: https://doi.org/10.1038/s41586-024-08328-6
-->

---
clicks: 2
---

<div class="eyebrow">Predictive uncertainty</div>

# A distribution can give a prediction interval

<PredictiveDensity />
<div class="source">Illustrative Gaussian predictive distribution, mean £500k and standard deviation £80k. Nominal 95% mass under this distribution.</div>

<!--
A distribution is not itself an interval. One way to obtain an interval is to read off its 2.5th and 97.5th percentiles. The shaded region contains 95% of this model distribution. Reliable real-world predictive coverage still depends on calibration and assumptions. This interval targets a new observed sale price and combines outcome variation with uncertainty in our knowledge.
-->

---
routeAlias: two-questions
clicks: 1
---

<div class="eyebrow">02 · Two targets</div>

# One house, two different questions

<p class="lead">Fix its observed features: floor area, location, age, and so on.</p>

<div class="two mt-8">
<div class="panel" style="border-top:4px solid #4263eb"><span class="pill">Future outcome</span><h3>What might this house sell for?</h3><p>A range for one future transaction.</p><div class="mt-7 blue font-bold">Prediction interval</div></div>
<div v-click="1" class="panel" style="border-top:4px solid #0b9687"><span class="pill" style="background:#e9f8f4;color:#0b9687">Underlying average</span><h3>How precisely do we know the average price?</h3><p>A range for the mean among houses with these features.</p><div class="mt-4 teal font-bold">Confidence interval</div></div>
</div>
<div class="source">The target in this paper is the regression mean f(x) = E[Y | X = x]. This is an association, not a causal effect.</div>

<!--
Hold the covariates fixed in both questions. Individual houses can still differ in unobserved ways. For the second question, those differences do not change the target: the average for houses with these observed features. The current paper studies this conditional mean, not a causal treatment effect. Source: https://arxiv.org/html/2609.33114v1#S3
-->

---
clicks: 3
---

<div class="eyebrow">Two targets · One picture</div>

# The average and the individual can differ

<IntervalLab mode="compare" />
<div class="source">Simulated illustration: linear mean, independent Gaussian noise, known noise scale. These are analytical example intervals, not TabCon outputs.</div>

<!--
First show the fitted mean, then the broad predictive band, then the confidence band. At 100 square metres, the blue range concerns a new house and the green range concerns the average. Width alone does not tell us which interval is better: first choose the target. The bands are pointwise 95% intervals in a simple correctly specified Gaussian example, not simultaneous confidence bands.
-->

---
clicks: 2
---

<div class="eyebrow">An interactive thought experiment</div>

# What changes when we collect more data?

<IntervalLab mode="grow" />
<div class="source">Simulated illustration with known Gaussian noise. Advance with the arrow key or select a sample size. Bands are pointwise, not simultaneous.</div>

<!--
Advance through 20, 80 and 320 observations, or use the buttons. More data makes the average more precise in this well-specified example, while the range for a new sale retains irreducible outcome variation. This is intuition, not a general guarantee of monotone interval shrinkage for every fitted model or every realized dataset.
-->

---
clicks: 2
---

<div class="eyebrow">Why confidence intervals?</div>

# A point estimate hides how much we know

<p class="lead">Both analyses estimate the average price at £500k.</p>

<div class="two mt-7">
<div class="panel text-center"><div class="small">Less information</div><div class="big-number mt-3">£500k</div><div style="height:4px;background:#7c4dce;margin:30px 8px 14px"></div><div class="violet text-xl">£440k–£560k</div><p class="small">A broad range remains compatible.</p></div>
<div v-click="1" class="panel text-center"><div class="small">More information</div><div class="big-number mt-3">£500k</div><div style="height:4px;background:#0b9687;margin:30px 110px 14px"></div><div class="teal text-xl">£488k–£512k</div><p class="small">The average is more tightly located.</p></div>
</div>
<div v-click="2" class="callout green mt-5">Confidence intervals help us report precision and judge whether more evidence is needed.</div>
<div class="source">Hypothetical estimates and intervals, used only to illustrate precision. A confidence interval does not measure every source of uncertainty or bias.</div>

<!--
The point estimate is the same, but the scientific message is different. A narrow interval can support a precise statement about the average. A broad interval can show that further data would be valuable. Neither interval alone resolves model misspecification, unmeasured confounding or a bad sampling design. The example concerns an association, not a causal effect.
-->

---
clicks: 1
---

<div class="eyebrow">Confidence, intuitively</div>

# What does “95% confidence” mean?

<CoverageDemo />
<div class="source">Illustrative repeated-sampling intervals. One set of 20 need not contain exactly 19 successful intervals.</div>

<!--
Advance once to reveal all 20 intervals and the coverage count. The underlying average stays fixed. Different datasets produce different estimates and intervals. A 95% procedure aims to cover that fixed target in about 95% of repeated experiments. This does not mean 95% of future outcomes fall in the confidence interval, and the frequentist statement is not a posterior probability assigned to the fixed target after observing one interval.
-->

---
clicks: 1
---

<div class="eyebrow">The computational question</div>

# Must every new dataset start from scratch?

<div class="two mt-8">
<div class="panel"><div class="eyebrow">Resampling at deployment</div><h3>A bootstrap workflow</h3><p>Resample the dataset many times.<br>Refit the predictor each time.<br>Compare the resulting estimates.</p><div class="small mt-6">The computation repeats for each dataset.</div></div>
<div v-click="1" class="panel" style="background:#eef2ff;border-color:#c3cff7"><div class="eyebrow">Learning across tasks</div><h3>An amortized workflow</h3><p>Learn the interval procedure beforehand.<br>Apply it to a new dataset.</p><div class="blue mt-8 font-bold">Can the PFN idea extend to inference?</div></div>
</div>
<div class="source">Amortization moves computation into shared training. It does not eliminate training cost. Bootstrap is one example of a dataset-specific procedure.</div>

<!--
Bootstrap is a familiar way to estimate how an estimator varies, though it requires assumptions and does not automatically work for every estimator. The question here is whether a learned procedure can avoid repeated deployment-time resampling. The computational cost of shared pretraining still exists.
-->

---
class: section-slide
routeAlias: tabcon
---

<div class="eyebrow">03 · TabCon</div>

# Learn how the<br>estimate can be wrong

<p class="lead">Training tasks reveal the true average.<br>That gives us a new learning target.</p>
<div class="section-no">03</div>
<div class="source" style="color:#8391ad"><a href="https://arxiv.org/abs/2609.33114">Ye et al., Can Tabular Foundation Models Amortize Statistical Inference?</a></div>

<!--
In a simulated training world, we know the regression function. That lets us teach the network about estimation error rather than only the next noisy outcome. Source: https://arxiv.org/html/2609.33114v1#S3
-->

---
clicks: 2
---

<div class="eyebrow">From prediction to inference</div>

# TabPFN predicts outcomes. We want the mean.

<div class="outcome-decomposition">
<div><MathTex tex="Y" /><small>Observed outcome</small></div><i>=</i><div class="teal"><MathTex tex="f(x)" /><small>The mean we care about</small></div><i>+</i><div class="violet"><MathTex tex="\epsilon(x)" /><small>Outcome noise</small></div>
</div>
<div class="target-comparison">
<section><span class="detail-label">TabPFN’s predictive distribution</span><div class="target-math blue"><MathTex tex="q_\theta(y\mid x,D)" /></div><p>A distribution for <b>f(x) + ε(x)</b>.<br>Its quantiles describe possible outcomes.</p></section>
<section v-click="1" class="mean-target"><span class="detail-label">Our inferential target</span><div class="target-math teal"><MathTex tex="f(x)=\mathbb{E}[Y\mid X=x]" /></div><p>How precisely do the data<br>locate this <b>unknown mean</b>?</p></section>
</div>
<div v-click="2" class="target-shift">Change the learning target: <b>outcomes → estimation residuals.</b></div>
<div class="source">E[ε(x) | X = x] = 0. Predictive uncertainty includes outcome noise and uncertainty about the mean. <a href="https://arxiv.org/html/2609.33114v1#S3">Ye et al., Section 3</a>.</div>

<!--
Start from the outcome decomposition Y=f(x)+epsilon(x), with zero conditional-mean noise. Epsilon(x) denotes a random outcome deviation at fixed features x; its distribution may depend on x. Standard TabPFN learns a predictive distribution for Y, which is a noisy realization of f(x), rather than a confidence distribution for the fixed regression mean itself. Its predictive spread can reflect both outcome variation and uncertainty about the estimated mean. Reveal our target f(x), then the change of learning target. We do not simply subtract a noise realization from a prediction: we train a new residual distribution for estimation error. This sets up the next slide. Source: https://arxiv.org/html/2609.33114v1#S3
-->

---
clicks: 2
---

<div class="eyebrow">TabCon · Change what the model predicts</div>

# Learn residuals to build confidence intervals

<div class="residual-learning">
<section><span class="detail-label">Define the estimation residual</span><div class="target-math violet"><MathTex tex="r(x)=\widehat f(x)-f(x)" /></div><p>TabPFN estimate − known synthetic mean.</p></section>
<div class="residual-arrow">→</div>
<section v-click="1"><span class="detail-label">Learn its distribution</span><div class="target-math blue"><MathTex tex="q_\phi(r\mid x,D)" /></div><p>TabPFN features → residual heads.</p></section>
</div>
<div v-click="2" class="residual-to-ci">
<div class="residual-proof-label">Confidence coverage = residual coverage</div>
<div class="residual-proof"><MathTex tex="\begin{aligned}&\mathbb{P}_D\!\Bigl(\widehat f(x)-Q_{1-\alpha/2}(x)\leq f(x)\leq\widehat f(x)-Q_{\alpha/2}(x)\Bigr)\\[2pt]&=\mathbb{P}_D\!\Bigl(Q_{\alpha/2}(x)\leq\textcolor{#7c4dce}{\widehat f(x)-f(x)}\leq Q_{1-\alpha/2}(x)\Bigr)\\[2pt]&=1-\alpha\end{aligned}" display /></div>
</div>
<div class="residual-definition">Across datasets <b>D</b>, <b>f(x) stays fixed</b> and the interval changes. Set α = 0.05 for 95% coverage.</div>
<div class="source"><a href="https://arxiv.org/html/2609.33114v1#S3">Ye et al., Section 3, Eq. 2</a>. Oracle identity for fixed x and continuous sampling errors: Q denotes true residual quantiles. TabCon learns <MathTex tex="\widehat Q" />; coverage needs calibration.</div>

<!--
The key move is to reuse TabPFN's representations but change the prediction target from Y to r(x)=f-hat(x)-f(x). The residual heads predict a distribution, not only one residual value. In synthetic training tasks, f is known, so r is available as supervision. At deployment, the model sees only the observed context and query features, not the true mean. The backbone and point predictor remain frozen in the reported implementation; lightweight residual heads and the router are trained as explained next. Epsilon(x)=Y-f(x) is outcome noise, whereas r(x)=f-hat(x)-f(x) is estimation error; using the noisy residual Y-f-hat(x) would target a different distribution. The three-line display explains the interval by an equivalent event: f lies inside the confidence interval exactly when the estimation residual lies between its two quantiles. The violet term identifies that residual and matches its definition above. P_D means probability over repeated draws of the training dataset D at fixed x and fixed regression function f. The larger residual quantile determines the lower confidence endpoint. Q denotes true sampling-error quantiles, and the final equality assumes a continuous error distribution; with atoms, generalized quantiles give coverage at least 1-alpha. In practice TabCon substitutes learned quantiles Q-hat, so the oracle equality is intuition, not an automatic guarantee for learned intervals. Post-training calibrates their coverage empirically. Source: https://arxiv.org/html/2609.33114v1#S3
-->

---
clicks: 3
---

<div class="eyebrow">TabCon · Architecture</div>

# Three residual heads, one sparse MoE router

<TabConFlow />
<div class="source">Simplified from Ye et al., Figure 1 and Appendix B.1. Heads and router share frozen backbone embeddings. Top-2 mixes distributions before quantiles are extracted.</div>

<!--
This is a sparse mixture of three residual experts. The frozen TabPFN-v3 backbone supplies the same query embeddings to all three heads and to the router. Solid arrows carry representations or distributions; the dashed purple connection carries routing weights. The three heads appear together, followed by the attention-based router, then an illustrative Top-2 choice. In the implementation in Appendix C.3, each residual head is a lightweight MLP on frozen backbone query embeddings. The specialists train primarily on tasks where the global intervals under- or overcover. The top-2 router chooses task-level mixture weights. The weights here are illustrative. They mix distributions, not interval endpoints or quantiles. During router post-training, all residual heads stay frozen.
-->

---
clicks: 2
class: detail-slide
---

<div class="eyebrow">Inside TabCon · What we reuse</div>

# Reuse the backbone. Change the prediction target.

<TabPFNReuse />
<div class="source">Schematic of <a href="https://arxiv.org/html/2609.33114v1#A3.SS3">TabCon, Appendix C.3</a> and the <a href="https://github.com/PriorLabs/TabPFN/blob/main/src/tabpfn/architectures/tabpfn_v3.py">TabPFN-v3 regression architecture</a>. Shared head design does not imply shared trained weights.</div>

<!--
TabPFN's feature-processing layers and in-context transformer are reused and frozen. We take their final query representations. The original regression decoder remains frozen and supplies the point estimate. Its output projection is a Linear-GELU-Linear MLP. TabCon's residual heads follow the same MLP form, with residual bins as the output target. The heads have separate trainable parameters. The paper says the specialists start from the trained Global head; it does not establish that Global is initialized from the original prediction head. The feature-encoding box groups the input/distribution embedding and feature-aggregation stages. Reveal the residual branch, then emphasize the change of prediction target.
-->

---
clicks: 3
routeAlias: router-details
class: detail-slide
---

<div class="eyebrow">Inside the router · Read the whole query set</div>

# Attention + statistics summarize the query set

<RouterEncoder />
<div class="source"><a href="https://arxiv.org/html/2609.33114v1#A2.SS1">Ye et al., Appendix B.1</a>. Query-set aggregation shown for one ensemble member; downstream routing is simplified. Std = standard deviation. Attention weights and expert scores are illustrative.</div>

<!--
The diagram focuses on query-set aggregation within one ensemble member. Frozen TabPFN produces query embeddings conditioned on the observed context; a shared trainable encoder produces tokens h_i. Two branches read these same tokens in parallel. Learned attention queries produce four weighted averages u_j. The other branch computes an unweighted mean and population standard deviation across query points, separately for each token coordinate. These are not statistics of raw covariates, predicted outcomes, residuals, or the u_j vectors. Standard deviation describes variation among the encoded query points; it is not itself an uncertainty estimate for f(x). The mean and standard deviation supply overall average and variation alongside the learned summaries. Including them is an architectural choice, not a mathematical requirement or a demonstrated necessity without an ablation. Concatenate all six vectors. The downstream routing network is collapsed here; the implementation then applies an estimator projection, aggregates across ensemble members using mean and standard deviation, and maps the task representation to expert scores. Parameters are shared across members, while tokens and all summaries depend on the member's input. Reveal attention, then the parallel statistics and concatenated summary, then downstream expert scores. Heatmap and expert scores are illustrative.
-->

---
clicks: 2
class: detail-slide
---

<div class="eyebrow">Inside the router · From experts to an interval</div>

# Choose two experts, then mix their distributions

<RouterWeights />
<div class="source"><a href="https://arxiv.org/html/2609.33114v1#A2.SS1">Ye et al., Appendix B.1</a>. Distributions and weights are illustrative. Top-2 routing is used in SFT, RL and deployment.</div>

<!--
The router's scores are transformed into mixing weights, the two largest weights are retained, and these are renormalized to sum to one. The example selects Global and Expansion with weights 0.35 and 0.65. Global is not required to be one of the selected experts. The stacked histogram shows actual binwise mixing of two normalized illustrative distributions: blue is the weighted Global contribution and purple is the weighted Expansion contribution. On the second click, read the mixture's 2.5% and 97.5% quantiles and combine them with the fixed point estimate to construct the nominal 95% confidence interval. Quantiles are extracted after mixing; the heads' endpoints are not averaged. The same task-level weights apply to every query point, while each query has its own residual distributions. The final model uses Top-2 during both SFT and RL. In SFT, a straight-through estimator supplies a dense-softmax proxy gradient while the forward mixture stays sparse. RL samples Top-2 routing actions; deployment uses the selected pair deterministically.
-->

---
clicks: 3
class: detail-slide
---

<div class="eyebrow">Training · The order matters</div>

# First learn the heads. Then learn to route.

<div class="training-stages">
<section><span>01</span><h3>Global</h3><p>Learn estimation errors across the training task family.</p><b>Update θ<sub>G</sub></b><small>50,000 synthetic datasets</small></section>
<section v-click="1"><span>02</span><h3>Specialists</h3><p>Clone Global; specialize using its coverage profile.</p><b>Update θ<sub>E</sub>, θ<sub>S</sub></b><small>Regime-based supervision</small></section>
<section v-click="2"><span>03</span><h3>Router SFT</h3><p>Fit a Top-2 mixture with straight-through gradients.</p><b>Update ψ only</b><small>50,000 additional datasets</small></section>
<section v-click="3"><span>04</span><h3>Router RL</h3><p>Reward sparse mixtures that produce better intervals.</p><b>Update ψ only</b><small>100,000 additional datasets</small></section>
</div>
<div class="detail-message">The TabPFN backbone and point predictor remain frozen throughout.</div>
<div class="source"><a href="https://arxiv.org/html/2609.33114v1#S4">Section 4</a> and <a href="https://arxiv.org/html/2609.33114v1#A3.SS3">Appendix C.3</a>. Stages use independently generated training tasks; evaluation datasets are separate.</div>

<!--
The two specialists are trained before router SFT. SFT here names the initialization of the router, not another round of updating the heads. The residual head training is itself supervised. Do not imply that all network parameters are updated end-to-end. Once the specialists have been learned, the Global and both specialist heads are fixed throughout post-training. A separate specialist-stage task count is not specified in C.3, so no count is asserted here.
-->

---
clicks: 2
class: detail-slide
---

<div class="eyebrow">Stage 01 · Global head</div>

# Teach the head where the estimation error lands

<div class="training-pipeline"><div><span>Simulate a task</span><b>True mean <MathTex tex="f(x)" /></b></div><i>→</i><div><span>Frozen predictor</span><b>Estimate <MathTex tex="\widehat f(x)" /></b></div><i>→</i><div><span>Supervised target</span><b><MathTex tex="e=\widehat f(x)-f(x)" /></b></div></div>
<div v-click="1" class="loss-display"><MathTex tex="\mathcal{L}_{G}=\underbrace{\mathrm{NLL}}_{\text{fit the observed error}}+0.20\,\underbrace{\mathrm{CRPS}}_{\text{fit the cumulative distribution}}" /></div>
<div v-click="2" class="two detail-pair"><section><h3 class="blue">NLL</h3><p>Put probability on the bin containing the known training error.</p></section><section><h3 class="violet">CRPS</h3><p>Respect the ordering of error values, not just which bin is correct.</p></section></div>
<div class="parameter-line"><span class="update-tag">UPDATE · Global MLP θ<sub>G</sub></span><span class="frozen-tag">FROZEN · Backbone + point predictor</span></div>
<div class="source"><a href="https://arxiv.org/html/2609.33114v1#S4">Section 4, Eq. 3</a>; <a href="https://arxiv.org/html/2609.33114v1#A3.SS3">Appendix C.3</a>. The target is estimation error, not <MathTex tex="Y-\widehat f(x)" />.</div>

<!--
Each synthetic task supplies a context, query features and the oracle conditional mean. The frozen predictor produces f-hat. The head reads the frozen query embedding and predicts error-bin probabilities. NLL is cross-entropy for the realized error bin; CRPS compares the cumulative distribution to the realized error. We optimize only Global's MLP weights and biases. Eta_1 controls the contribution of CRPS relative to NLL. The task prior and discretization determine what error patterns the head can learn. Reported optimization uses AdamW, lr 3e-4, weight decay 1e-4, accumulation across eight tasks and norm clipping at 1.
-->

---
clicks: 2
class: detail-slide
---

<div class="eyebrow">Stage 02 · Calibrating the score cutoffs</div>

# Use coverage scores to find two cutoffs

<CoverageThresholds />
<div class="source">Coverage-score definition: <a href="https://arxiv.org/html/2609.33114v1#S4">Section 4</a>. Dataset-level calibration follows the training implementation. Histogram is illustrative.</div>

<!--
This slide covers threshold calibration only; specialist assignment comes next. Run the frozen Global head on many separate synthetic calibration datasets. For each dataset, C_alpha is the fraction of its query residuals inside the corresponding predicted intervals, equivalently the fraction of oracle means inside the resulting confidence intervals. Compute S by averaging signed coverage deviations over levels, with normalized weights proportional to 0.25, 0.50, 1 and 2. A negative S indicates weighted undercoverage; a positive S indicates weighted overcoverage. Gather these dataset-level scores and set s_1 and s_2 to their empirical one-third and two-thirds quantiles, as in src/tabcon/training/calibrate.py. The histogram is illustrative, with cutoffs computed from its cumulative bin counts; it is not an experimental result. Keep these two cutoffs fixed for subsequent specialist training. First reveal the score distribution, then reveal its quantile cuts and the saved thresholds. The levels are secondary configuration details, not the point of this slide. Dataset-level calibration follows the checked implementation; arXiv v1 Section 4 instead describes averaging across datasets within each DGP before partitioning DGPs. This empirical score across a query set is a training signal, not a repeated-sampling coverage guarantee from a single dataset.
-->

---
class: detail-slide
---

<div class="eyebrow">Stage 02 · Training the two specialist heads</div>

# Use the cutoffs to assign specialist supervision

<SpecialistTraining />
<div class="source"><a href="https://arxiv.org/html/2609.33114v1#S4">Eq. 4</a> and <a href="https://arxiv.org/html/2609.33114v1#A3.SS3">Appendix C.3</a>. KL direction: KL(p<sub>Global</sub> ‖ p<sub>specialist</sub>).</div>

<!--
Compute S anew for each training dataset, then compare with the fixed s_1 and s_2 from the previous slide. Select each score range to show which losses are active. For S <= s_1, Expansion gets NLL plus 0.20 CRPS plus 0.005 KL; Shrinkage gets only KL. For s_1 < S < s_2, both receive only KL. For S >= s_2, Shrinkage receives the supervised terms and Expansion receives only KL. The inclusive boundaries match calibration_bucket in the implementation, so equality is not left undefined. Both specialists start as copies of Global. These are dataset-level assignments, not fixed DGP labels, and new tasks need not fall into exact thirds. Global remains frozen. Neither specialist is a fixed multiplicative width adjustment: each predicts a full error distribution, without a guarantee that Expansion always widens or Shrinkage always narrows every interval. Numerical coefficients and optimizer details are retained in notes rather than emphasized in the diagram.
-->

---
clicks: 2
class: detail-slide
---

<div class="eyebrow">Stage 03 · Router SFT</div>

# SFT: Top-2 forward, straight-through backward

<RouterSFT />
<div class="source">Final-model training implementation, verified against the selected SFT checkpoint. Weights are illustrative; the backbone and all three heads stay frozen.</div>

<!--
The final model's SFT already uses Top-2 routing. This slide follows the original training implementation, not the dense-SFT description in arXiv v1. Local verification on 2026-10-24: release_audit/20261024/lineage_recheck/sft_live_recheck.json records top_k=2 and straight_through_topk=true in the selected 40,000-step SFT checkpoint; its hash matches the initializer recorded by the final RL run. All 2,501 saved SFT training records have exactly two positive mixture weights. The historical source hashes independently match historical_source_check.json: core.py 49f259d7d5f6bdf673b099f69fe0e766d16090c9de54e0a40afecd3f4e2c3779; train.py dbf16d842d26bc4ceca398e25088f999268bef92d9b51d8c7d3ed976260b9d7c.

Read the diagram as a forward pass followed by a backward pass. Frozen TabPFN query embeddings feed a trainable task router. The three frozen residual heads are all evaluated during SFT. On click one, retain the two largest softmax weights, set the third to zero, and renormalize. The example's Global / Expansion / Shrinkage softmax weights are 0.25 / 0.60 / 0.15; its mixture weights are 0.25/0.85, 0.60/0.85, and zero (rounded to 0.29 / 0.71 / 0). The histogram uses the unrounded weights and has only two contributions. The pair is selected anew for each task; any pair can be selected, including Expansion + Shrinkage. All queries of a task share the pair and its weights, while each query has its own residual distributions. The known simulated estimation errors supervise the mixture using NLL + CRPS (CRPS weight 1 in this run). There are no correct-expert labels.

On click two, the return path shows the straight-through update to the router only. The exact gate is weights = dense_weights + (sparse_weights - dense_weights).detach(). Forward values equal the sparse Top-2 weights. Backward differentiation uses the dense-softmax proxy Jacobian; this is an approximate gradient, not the true derivative of discrete selection and not an assertion that the forward loss used a dense mixture. All three routing scores can change, allowing a different pair to be selected later. No gradients update the backbone or frozen experts. The final router layer is initialized to zero, so initial logits tie and the first pair follows torch.topk's tie handling. The illustrative weights are learned-output examples, not initial values.
-->

---
clicks: 2
class: detail-slide
---

<div class="eyebrow">Why post-training?</div>

# Why RL after Top-2 SFT?

<WhyRouterRL />
<div class="source"><a href="https://arxiv.org/html/2609.33114v1#S4">Section 4</a>: interval-focused RL objectives. Both training stages use Top-2 in the verified final-model implementation. Diagrams are illustrative.</div>

<!--
SFT and RL share a Top-2 task router and the same frozen backbone and residual experts. RL continues from the SFT checkpoint; it does not introduce sparsity. SFT learns from simulated estimation errors with NLL + CRPS and a straight-through gradient estimator. These losses assess the full error distribution, but do not directly optimize the coverage probability and length of the derived confidence intervals.

On click one, reveal the RL stage: sample Top-2 routing actions, construct the resulting intervals, score their coverage and length against simulator truth, and update the router with RLOO. The interval sketches illustrate coverage and width, not measured before/after results. On click two, reveal the central motivation: align training with how the final intervals are evaluated. RL optimizes empirical rewards and does not give a universal coverage guarantee. Any expert pair is allowed; mixing Expansion and Shrinkage is not inherently invalid. Avoid attributing lower head-computation cost to the switch from SFT to RL: SFT already has two nonzero mixture weights, and its training loop computes all three frozen expert outputs.
-->

---
clicks: 3
routeAlias: rl-details
class: detail-slide
---

<div class="eyebrow">Stage 04 · Router RL with verifiable rewards</div>

# RLOO: compare routes on the same task

<RLOODemo />
<div class="source">RLOO = REINFORCE Leave-One-Out · <a href="https://arxiv.org/html/2402.14740v1#S2.SS3">Ahmadian et al., §2.3</a>; <a href="https://arxiv.org/html/2609.33114v1#S4">TabCon, §4</a>. Four routes and rewards are illustrative. K = number of samples; z = sampled router scores.</div>

<!--
One iteration uses a single synthetic task T: the same observed data, query set, frozen embeddings and expert outputs for every candidate. Initialize the policy from the SFT router. The router produces relative logit means, then adds Gaussian exploration noise to sample scores z_i from q_psi(z | T). Apply softmax and Top-2 with renormalization to obtain candidate mixture weights. Each candidate gives a different residual mixture, confidence intervals and a scalar reward measuring their quality across the same task. First click: reveal the four example rewards. These are arbitrary demonstration values, not actual experiments.

Second click: explain the baseline before the update. For every candidate i, b_i = sum_{j != i} r_j / (K - 1), and A_i = r_i - b_i. The selected B has reward 0.8; the other three rewards are 0.2, -0.1 and 0.5. Their mean is 0.2, so A_B = +0.6. B's own reward is visibly crossed out when calculating its baseline. Click C for a negative example: its baseline is 0.5 and A_C = -0.6. The leave-one-out operation removes a candidate's reward from its own baseline; it does not remove a query point, expert, or training dataset. Comparing routes on the same task supplies a task-specific reference without training a separate value critic. Even a positive raw reward may have a negative advantage: A earns +0.2 but has baseline +0.4.

Third click: minimize -mean_i stopgrad(A_i) log q_psi(z_i | T). The log density here describes the sampled router scores, not the three expert mixing weights and not a density calculated after the noninvertible Top-2 projection. Holding sampled scores and advantages fixed, gradients through log q update the router to favor above-baseline samples and discourage below-baseline samples. Every sampled candidate contributes; the algorithm does not simply pick the maximum-reward candidate as a label. The aggregate parameter update need not increase every individual sample's density because gradients share parameters. There is no gradient through the reward, interval quantiles, or coverage indicators; the backbone and heads stay frozen. Repeat on fresh synthetic tasks. At deployment, use the deterministic Top-2 router output without candidate sampling or oracle rewards.

Implementation checked in src/tabcon/training/policy.py and rl.py. The saved RL training record uses K=16, with paired antithetic Gaussian perturbations of the two logits relative to the Global reference, exploration sigma annealed from 1.0 to 0.1, softmax, and exact Top-2. The policy loss computes (sum(reward)-reward)/(K-1), detaches advantages, and averages their products with Gaussian log densities. Four candidates are used only to keep the worked example readable. The original RLOO independent-sampling unbiasedness argument should not be asserted for this antithetic implementation without further analysis; no unbiasedness claim is made on the slide.
-->

---
class: detail-slide
---

<div class="eyebrow">Stage 04 · What makes an interval worth rewarding?</div>

# Six reward components, three roles

<RewardComponents />
<div class="source"><a href="https://arxiv.org/html/2609.33114v1#A2.SS2">Appendix B.2 · Post-training reward function</a>.</div>

<!--
All three groups and all six components are visible on entry, with no incremental reveal. The groups organize overlapping purposes for the talk; they are not a claim of six independent objectives or a different reward definition. Explain the distinctions without formulas. The target is the true regression function, not a noisy future outcome.

Interval precision: WIL rewards a reduction in average interval width relative to the Global head on the same task. WIS also uses width but includes the distance of missed targets from the interval; its full definition includes the median error as well. The distinction is width alone versus a score that also measures how badly an interval misses. Both rewards compare the routed result with the Global reference.

Coverage calibration: CS penalizes total coverage falling below or above the nominal target beyond a tolerance. Tail balance checks lower and upper misses separately. Two intervals can have the same overall coverage but differ in which side contains the misses; the tail term distinguishes them. This concerns miss probabilities, not geometric symmetry around the point estimate.

Extra safeguards: CVaR uses the same undercoverage information as CS but adds emphasis to the worst shortfalls across tasks. CS already penalizes individual undercoverage; CVaR further changes the emphasis toward the severe tail rather than introducing an entirely independent signal. Excess width overlaps with WIL, which continuously favors shorter intervals, but adds a penalty only after widening exceeds a budget relative to the Global head. The extra penalty is downweighted when coverage is insufficient. These terms encourage useful behavior during training rather than guarantee coverage for every new dataset. Their incremental necessity requires ablation evidence. Detailed reward normalization, adaptive weights, and scope aggregation are in Appendix B.2.
-->

---
class: detail-slide
---

<div class="eyebrow">Training · Parameter ownership</div>

# Which weights move at each stage?

<table class="ownership-table">
<thead><tr><th>Module</th><th>Global fit</th><th>Specialists</th><th>Router SFT</th><th>Router RL</th></tr></thead>
<tbody>
<tr><td>TabPFN backbone + point predictor</td><td>Frozen</td><td>Frozen</td><td>Frozen</td><td>Frozen</td></tr>
<tr><td>Global residual MLP · θ<sub>G</sub></td><td class="learned-cell">Train</td><td>Frozen teacher</td><td>Frozen</td><td>Frozen</td></tr>
<tr><td>Expansion + Shrinkage · θ<sub>E</sub>, θ<sub>S</sub></td><td>Not yet used</td><td class="learned-cell">Train</td><td>Frozen</td><td>Frozen</td></tr>
<tr><td>Router · ψ</td><td>Not yet used</td><td>Not yet used</td><td class="learned-cell">Train</td><td class="learned-cell">Train</td></tr>
</tbody>
</table>
<div class="router-parameters"><b>Router ψ includes</b><span>Query encoder + LayerNorm</span><span>4 attention-query vectors</span><span>Member projection</span><span>Routing MLP</span></div>
<div class="detail-message">At deployment, every learned parameter is frozen. A new dataset changes activations and routing weights.</div>
<div class="source"><a href="https://arxiv.org/html/2609.33114v1#A2.SS1">Appendix B.1</a> and <a href="https://arxiv.org/html/2609.33114v1#A3.SS3">C.3</a>. RL also updates reward-control multipliers / CVaR thresholds; these are separate from policy weights ψ.</div>

<!--
Distinguish model parameters from hyperparameters and outputs. Theta_G, theta_E and theta_S are MLP weights and biases. Psi contains the router's learned normalization, encoding, pooling-query, projection and routing parameters. The per-task vector w is an output, not a new parameter optimized on the deployment dataset. The adaptive dual variables and CVaR thresholds mentioned in the reward specification are training-control state, separate from psi. No gradient updates or oracle mean are needed at deployment. The mixture weights are computed from context and query embeddings.
-->

---
routeAlias: evidence
---

<div class="eyebrow">04 · Evidence</div>

# Three benchmarks, one known target

<EvaluationDesign />
<div class="source"><a href="https://arxiv.org/html/2609.33114v1#S5">Section 5</a> and <a href="https://arxiv.org/html/2609.33114v1#A3.SS1">Appendix C.1–C.2</a>. Standard ID, Standard OOD, Stress-test and CC18 are reported separately. All evaluation datasets are generated afresh.</div>

<!--
We need ground truth for the regression mean to score confidence intervals directly. There are three benchmark designs, yielding the four result settings on the next slide: Standard ID, Standard OOD, Stress-test and CC18. Stress-test is a separately generated and reported evaluation suite, not a subset of saved Standard ID/OOD evaluation datasets. It does share the broad ID generator and several mechanisms with the training prior. A stress condition therefore need not be out of distribution: for example, a discontinuous target is a possible draw in the broad prior, whereas its stress configuration forces that target regime while retaining Gaussian noise and clean features as the reference.

Appendix C.1 distinguishes broad joint variation in the Standard benchmark from controlled stress settings that isolate target, noise, or feature difficulties. Examples include bounded, quantized and discontinuous functions; near-zero or high noise, heavy tails, heteroskedasticity and asymmetric outliers; and categorical features with missing values. Code checked in src/tabcon/evaluation/synthetic.py, src/tabcon/evaluation/stress.py, src/tabcon/data/stress.py and make_stress_generator in src/tabcon/data/pfn_episode_generator_v2.py. The stress list has 11 conditions including regular_control, and each condition generates multiple episodes. These condition counts must not be added to sampled mechanism counts as though they were the same unit. The standard conditional evaluator defaults to 32 sampled mechanisms per ID/OOD generator; the marginal evaluator instead samples an episode stream. The previous large 64-DGP headline is omitted here so the overview does not imply that it counts all evaluation settings or that stress is an extra set of 11 individual DGPs.

The CC18 benchmark preserves covariates from 13 real datasets but simulates responses from known regression functions. It is semi-synthetic, not a claim that the true regression mean is known on a fully observational dataset. ID describes the generator family; specific evaluation datasets are new. Sources: Section 5 and Appendix C.1–C.2.
-->

---
---

<div class="eyebrow">Results · 95% nominal level</div>

# Coverage and precision belong together

<BenchmarkResults />
<div class="source"><a href="https://arxiv.org/html/2609.33114v1#S5.T1">Ye et al., Table 1</a>. Exact table values; switch settings above. Interval lengths use each benchmark's response scale.</div>

<!--
Start with standard ID. TabCon is close to the coverage target, while the bootstrap intervals are short but undercover here. PI is wider because its original target is the noisy outcome. Switch to OOD, stress-test or CC18 to show the same comparison. These are averages over datasets and query points, not a guarantee for every subgroup or individual query. The selected baselines omit Linear and RFF to keep the chart readable. Compare lengths within a benchmark rather than across benchmarks with different response scales.
-->

---
---

<div class="eyebrow">Results · Computation</div>

# A fast interval for a new dataset

<RuntimeChart />
<div class="callout"><b>0.21 s</b> for TabCon versus <b>10.71 s</b> for 50 bootstrap refits in this setting.</div>
<div class="source">Ye et al., Table 2. C = 256 context rows, Q = 256 queries. Median of 30 runs, NVIDIA RTX 6000 Ada. Deployment time excludes shared training.</div>

<!--
This is one concrete row of the runtime table, rather than an unqualified speedup claim. The horizontal axis is logarithmic. TabCon takes 0.2097 seconds, compared with 10.7106 for bootstrap, about 51 times faster here. PI takes 0.2137 and AMP 0.2772 seconds. The main point is avoiding repeated deployment-time refitting, not that all computation disappears. Source: https://arxiv.org/html/2609.33114v1#S5.T2
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
Return to the opening housing example. The right interval depends on the question. The contribution is to extend amortization from predicting outcomes to constructing intervals for the regression mean. Invite questions about the learning target, calibration or deployment cost.
-->

---
---

<div class="eyebrow">Further reading</div>

# Papers behind the talk

<div class="reference-list">
<div><span>PFNs</span><a href="https://arxiv.org/abs/2112.10510">Transformers Can Do Bayesian Inference</a><p>Müller et al. · ICLR 2022</p></div>
<div><span>TabPFN</span><a href="https://doi.org/10.1038/s41586-024-08328-6">Accurate predictions on small data with a tabular foundation model</a><p>Hollmann et al. · Nature 2025</p></div>
<div><span>TabCon</span><a href="https://arxiv.org/abs/2609.33114">Can Tabular Foundation Models Amortize Statistical Inference?</a><p>Ye, Gong, Zhou, Zangirolami and Shi · 2026</p></div>
</div>


<!--
The charts before the evaluation section are didactic simulations. The coverage and runtime charts transcribe values from Tables 1 and 2 of the TabCon paper.
-->
