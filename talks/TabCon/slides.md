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
<div class="source"><a href="https://arxiv.org/html/2609.33114v1#A2.SS1">Ye et al., Appendix B.1</a>. Distributions and weights are illustrative. Top-2 routing is used for RL actions and deployment.</div>

<!--
The router's scores are transformed into mixing weights, the two largest weights are retained, and these are renormalized to sum to one. The example selects Global and Expansion with weights 0.35 and 0.65. Global is not required to be one of the selected experts. The stacked histogram shows actual binwise mixing of two normalized illustrative distributions: blue is the weighted Global contribution and purple is the weighted Expansion contribution. On the second click, read the mixture's 2.5% and 97.5% quantiles and combine them with the fixed point estimate to construct the nominal 95% confidence interval. Quantiles are extracted after mixing; the heads' endpoints are not averaged. The same task-level weights apply to every query point, while each query has its own residual distributions. SFT uses a dense mixture; the sparse selection shown here describes deployment and RL actions.
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
<section v-click="2"><span>03</span><h3>Router SFT</h3><p>Fit a dense mixture to the observed training errors.</p><b>Update ψ only</b><small>50,000 additional datasets</small></section>
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

# Train the router by scoring the mixture

<RouterSFT />
<div class="source"><a href="https://arxiv.org/html/2609.33114v1#S4">Section 4, Eqs. 5–6</a>; <a href="https://arxiv.org/html/2609.33114v1#A3.SS3">Appendix C.3</a>. Paper's dense SFT formulation illustrated. Backbone and all three heads stay frozen.</div>

<!--
Read the diagram as a forward pass followed by a backward pass. The three frozen heads provide error-bin probabilities. Query embeddings from the frozen TabPFN backbone feed the trainable router. On the first click, the router's dense weights mix all three distributions, and the known simulated estimation error supplies NLL plus CRPS supervision. The stacked bars are the actual weighted contributions of the three normalized illustrative distributions; the dashed vertical line marks one realized error. On the second click, the purple return path shows backpropagation through the mixing weights into the router. Only router parameters change; no gradients update the backbone or residual heads. A correct-expert class label is never required. Weights 0.25, 0.60, 0.15 are illustrative outputs, not measurements or an optimization trajectory. One query's distribution is drawn for clarity, while all queries in the task contribute to the loss through shared task-level weights. The final routing layer starts with zero weights and biases, so initial logits are zero and initial dense weights are uniform. The learned attention queries start from N(0,h^-1). Reported SFT uses 50,000 additional datasets, eta_3=1, lr 1e-4, weight decay 1e-4, accumulation four tasks, clip norm 1, 5% warm-up then cosine decay. Query counts cycle through 64,128,256,256. SFT does not enforce sparsity; RL then evaluates strict Top-2 actions.

Implementation distinction checked on 2026-10-24: this diagram illustrates the dense SFT formulation in arXiv v1 Section 4. The saved release_audit/20261017/checkpoints/router_sft/router_config.json instead reports top_k=2 and straight_through_topk=true, and the local configs/training/sft.json also selects Top-2. Thus the SFT objective alone does not enforce sparsity, but the actual SFT implementation can and does impose it through its gate. Do not claim SFT intrinsically requires dense routing.
-->

---
clicks: 2
class: detail-slide
---

<div class="eyebrow">Why post-training?</div>

# Why add sparse routing and RL?

<WhyRouterRL />
<div class="source"><a href="https://arxiv.org/html/2609.33114v1#S4">Ye et al., Section 4</a>. Schematic weights and interval. Top-2 can select any pair. Only selected residual heads execute; the shared backbone still runs.</div>


<!--
Two separate design motivations connect supervised distribution fitting to the next RL stage. First, dense softmax routing gives every expert positive weight. Expansion and Shrinkage are specialized for different coverage regimes, so including both is not automatically useful. Top-2 permits a more selective mixture; the example drops Shrinkage and renormalizes 0.25/0.60 to approximately 0.29/0.71. Any expert pair may be selected, including Expansion together with Shrinkage. Neither specialist is a deterministic width scaler, and combining them is not mathematically invalid. In the checked embedding-only deployment path, src/tabcon/evaluation/common.py runs the router before evaluating only selected heads, reducing residual-head computation from three to two. This is not a measured end-to-end speedup: the shared TabPFN backbone still runs.

Second, NLL and CRPS assess the learned estimation-error distribution but do not directly optimize the coverage probability and length of its confidence intervals. RL can score the final intervals against simulator truth, penalizing undercoverage and encouraging useful precision. It optimizes empirical training rewards, not a universal coverage guarantee. Sparsity comes from the Top-2 gate, while RL supplies the interval-focused objective; neither mathematically requires the other. The paper presents a dense SFT formulation, but the saved SFT checkpoint and current SFT config already impose Top-2 with a straight-through gradient estimator. The objective mismatch is therefore the central RL motivation even for that sparse SFT implementation. Reveal sparse selection on the first click, then interval rewards and the final takeaway on the second.
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
