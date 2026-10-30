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
## Slide 1 — Title (45 seconds)

Good afternoon, everyone.

Today, I am going to talk about our recent work, called **“Can Tabular Foundation Models Amortize Statistical Inference?”**

The main question of this paper is quite simple.

We already have foundation models for prediction. But can we also use foundation models for statistical inference?

And we choose confidence intervals as our first topic. In particular, can we train a model to construct confidence intervals for different datasets, without running a new statistical procedure every time?

Today, I will first introduce some background on confidence intervals and tabular foundation models. Then, I will explain our proposed method, called TabCon.
-->

---
routeAlias: first-results
class: result-preview-slide
---

# Our Proposal: TabCon for Confidence Interval (CI) Construction

<StressPreview />

<!--
## Slide 2 — Our Proposal: TabCon for CI Construction (1 minute 40 seconds)

Before going into the details, I want to show you some results from our method.

When we construct confidence intervals, we care about two things. First, we want the coverage to be close to our target of 95 percent. Second, we want the intervals to be as short as possible.

This figure shows these two things.

Each point represents one method, averaged across ten stress-test settings.

The horizontal axis shows the average interval length on a logarithmic scale. Shorter is better.

The vertical axis shows the signed difference between the actual coverage and our target of 95 percent, in percentage points. Above zero means overcoverage; below zero means undercoverage. So, closer to zero is better.

As you can see, TabCon gives a good balance between coverage and interval length.

Across ten different settings, its average coverage is about **95.6 percent**, which is very close to our target. At the same time, TabCon produces relatively short intervals. Compared with the original prediction intervals from TabPFN, our intervals are about **42 percent shorter**. Of course, these two intervals have different targets, which I will explain later.

Another important advantage is speed.

In the separate runtime benchmark that I will show later, TabCon is about **50 times faster** than bootstrap with 50 refits.

So the main message here is simple: **TabCon can produce short confidence intervals while keeping coverage close to 95 percent, and it is also much faster.**
-->

---
routeAlias: roadmap
clicks: 0
class: background-agenda
---

# Background

<BackgroundAgenda active="ci" />

<!--
## Slide 3 — Background (30 seconds)

Before introducing TabCon, I want to cover two background topics.

The first one is **confidence interval construction**, which is a classical problem in statistics.

The second one is **tabular foundation models**, which are a more recent development in machine learning.

I will explain both parts with simple examples.

Let's start with confidence intervals.
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
## Slide 4 — CI Construction: A Classical Statistical Inference Problem (1 minute 20 seconds)

Let's consider a very simple example.

Suppose we want to estimate the average house price in London.

Imagine that the true average price is 500 thousand pounds. Of course, in a real problem, we do not know this value.

We collect some house price data and calculate an estimate.

But giving only one number is often not enough. We also want to know how accurate our estimate is.

This is why we use a confidence interval.

Here, we have three possible intervals.

The first interval is from 460 to 490 thousand pounds. This interval does not contain the true average, so it is not a successful interval in this example.

The second interval is from 440 to 560 thousand pounds. It contains the true value, but it is quite wide.

The third interval is from 480 to 520 thousand pounds. It also contains the true value, but it is much shorter.

So ideally, we want our confidence intervals to cover the true value, while being as short as possible.

But since we do not know the truth in practice, how can we tell whether a method is good?
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
## Slide 5 — What Does 95% Confidence Mean? (1 minute 30 seconds)

A confidence interval is usually designed to have a certain coverage level.

For example, we often use 95 percent.

But what does this 95 percent actually mean?

Let's imagine that we can repeat the same experiment many times.

Each time, we collect a new dataset, calculate a new estimate, and construct a new confidence interval.

The important point is that **the true average stays fixed**.

But the data, the estimate, and the confidence interval can all change.

*Click once to show the repeated samples.*

Here, each horizontal line represents one confidence interval from one dataset.

The vertical dashed line is the true average.

Some intervals cover the true value, while others miss it.

If our method has 95 percent coverage, then over many repeated experiments, about 95 percent of these intervals should contain the true value.

For example, on average, about 19 out of 20 intervals should cover it.

This does not mean that the true value has a 95 percent probability of being inside one particular interval.

Instead, 95 percent describes how often the **method works across repeated datasets**.

This is the key idea behind confidence intervals.
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
## Slide 6 — Classical Statistical Inference and Our New Idea (1 minute 35 seconds)

Statisticians have developed many different methods for constructing confidence intervals.

For example, we have the Wald interval, the delta method, and bootstrap.

We also have Bayesian methods, which give credible intervals. These have a different statistical meaning.

The methods shown on the left have different ideas, but in their usual form, they share one feature.

When we get a new dataset, we need to run the required calculations for that dataset.

For example, bootstrap needs to repeatedly sample from the data and calculate new estimates.

This can be expensive, especially when we have many datasets or many test points.

So we ask a different question.

**Instead of calculating confidence intervals from scratch for each dataset, can we learn how to calculate them?**

This is our main idea.

We first train a neural network using many simulated datasets.

During training, the network learns how estimation errors behave under different conditions.

After training, when we receive a new dataset, we can construct confidence intervals with a single forward pass.

We call this **amortized statistical inference**.

In simple words, we spend computation during training, and then reuse what the model has learned for many new datasets.

To make this possible, we build on tabular foundation models.
-->

---
routeAlias: background-tfm
clicks: 0
class: background-agenda advisor-background
---

# Background

<BackgroundAgenda active="tfm" />

<!--
## Slide 7 — Background: Tabular Foundation Models (20 seconds)

Now, let's move to the second background topic: tabular foundation models.

The main idea is to train one model that can work on many different datasets.
-->

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
## Slide 8 — One Model, Many Tasks Without Retraining (1 minute 15 seconds)

Today, foundation models are widely used in different areas.

For example, in computer vision, we have models that can work with images.

They can help with image generation, image understanding, and many other tasks.

For language, we have models like GPT.

A single language model can answer questions, write text, translate languages, and solve many different problems.

The important idea is that we do not need to train a completely new model for every new task.

Instead, we train a large model first and then reuse it.

Tabular foundation models adopt a similar idea, but for tabular data.

Tabular data is the data we usually see in statistics.

For example, a dataset may have rows for different houses, and columns for house size, number of bedrooms, and price.

We train one model on many datasets, and then use it to make predictions on new datasets.

This is very different from training a new regression model for every dataset.
-->

---
routeAlias: tabular-timeline
clicks: 0
class: tabular-history-slide advisor-background
---

# How Learning on Tabular Data Evolved

<TabularEvolution />

<!--
## Slide 9 — How Learning on Tabular Data Evolved (1 minute 20 seconds)

This slide shows how methods for tabular data have developed over time.

At the top, we have classical statistical methods.

For example, linear regression has been used for more than 200 years.

Later, we developed other methods, such as generalized linear models.

In the middle, we have modern machine learning methods.

These include neural networks, support vector machines, random forests, and gradient boosting.

Many of these methods are still widely used for tabular prediction. But in most cases, we need to train the model again when we move to a new dataset.

At the bottom, we have a newer direction: tabular foundation models.

Starting from PFNs in 2021, we have seen the development of TabPFN and several other model families.

More recently, we have seen newer versions of TabPFN, TabICL, and LimiX.

The main change is that we can learn from many datasets during pretraining, rather than learning everything from one dataset.
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
## Slide 10 — Tabular Foundation Models (1 minute 15 seconds)

Here are three important papers in the development of tabular foundation models.

The first one is PFN, which stands for **Prior-Data Fitted Network**.

The first PFN paper appeared in 2021 and was published at ICLR 2022. It introduced the idea of training a transformer on many simulated datasets, so that it can learn to make predictions using a new dataset as context.

The second paper is TabPFN, published at ICLR 2023.

It applied this idea to small tabular classification problems and showed that very fast predictions were possible.

The third paper is TabPFN version 2, published in Nature in 2025.

This version supports both classification and regression, and can work with more types of tabular data.

PFN gives us the general framework, and TabPFN develops this idea for real tabular prediction tasks.

Our method, TabCon, builds on this family of models, but focuses on statistical inference instead of only prediction.
-->

---
routeAlias: prior-labs
clicks: 0
class: advisor-background
---

# Prior Labs: From Research to Industry

<PriorLabsOverview />

<!--
## Slide 11 — Prior Labs: From Research to Industry (1 minute 10 seconds)

Tabular foundation models are not only an academic research topic.

They are also getting attention from industry.

One example is Prior Labs, the company behind the TabPFN family.

Here, you can see their TabPFN 3.5 product.

It allows users to work with tabular data through Python or an API.

In February 2025, Prior Labs raised 9 million euros in early funding.

SAP also committed more than one billion euros over four years.

As the slide notes, the acquisition was completed in July 2026, with Prior Labs continuing to operate independently.

I think this is an interesting example of how quickly this research area is moving.

A method that started as an academic paper is now being developed for practical business use.
-->

---
routeAlias: pfn-ecosystem
clicks: 0
class: ecosystem-slide advisor-background
---

# Since 2025, Over 100 Papers on PFNs Have Appeared

<PFNEcosystem />

<!--
## Slide 12 — Recent Research on PFNs (1 minute 10 seconds)

Over the past two years, we have also seen a lot of new research on PFNs.

This slide shows some examples.

We can roughly divide this research into three groups.

The first group focuses on better prediction models.

For example, we have TabICL, LimiX, SOMTab, TabFM, and Kumo Tabular.

These works try to improve prediction quality, model speed, or the range of tasks the models can handle.

The second group focuses on causal inference.

For example, Do-PFN and CausalPFN study how foundation models can help estimate causal effects.

The third group focuses on uncertainty.

These papers study how to measure uncertainty or how to separate different sources of uncertainty.

Our work is most closely related to this third direction.

But we focus on a more specific question:

Can we use a tabular foundation model to construct **confidence intervals for an unknown regression mean**, with good coverage and short interval lengths?

Before answering that, we need to understand how these models work.
-->

---
clicks: 2
class: advisor-background
---

# How Do Tabular Foundation Models Work?

<p class="lead">A training dataset (predictors &amp; labels) + test predictors → a distribution over test labels.</p>

<PFNFlow mode="predict" />

<!--
## Slide 13 — How Do Tabular Foundation Models Work? (1 minute 30 seconds)

Let's look at a simple example.

Suppose we have a dataset about house prices.

Each row represents one house.

The first column is the size of the house, the second column is the number of bedrooms, and the third column is the price.

Now, suppose we have a new house.

It has an area of 100 square meters and three bedrooms.

But we do not know its price.

Our goal is to predict that price using the existing data.

*Click once to show the data entering the model.*

We give the whole table to a pretrained tabular foundation model.

The model uses the known rows as context, and tries to understand the relationship between the input features and the house prices.

An important point is that we do not need to update the model weights for this new dataset.

*Click again to show the output distribution.*

After reading the data, the model produces a predictive distribution.

This is different from only predicting one number.

The distribution tells us which house prices the model considers more or less likely. We can use its mean or median as our final point prediction.
-->

---
clicks: 2
class: advisor-background
---

# How to Train Tabular Foundation Models

<p class="lead">Generate datasets, mask outcomes, and learn to predict them.</p>

<PFNFlow mode="train" />

<!--
## Slide 14 — How to Train Tabular Foundation Models (1 minute 45 seconds)

The training process is actually quite simple to understand.

Instead of collecting one very large real-world dataset, we can generate many simulated datasets.

Each dataset follows a different data-generating process.

For example, one dataset may have a simple relationship between the input and output.

Another may have a curved relationship.

And another may have a different level of noise.

*Click once to show the hidden outcomes.*

During training, we hide some output values from the model.

The model can see the input features, and it can also see the other rows where the outputs are known.

Then we ask it to predict the hidden values.

Of course, since the datasets are simulated, we know the correct answers.

*Click again to show the training loss.*

We use these correct answers to calculate the training loss.

Here, the formula is the negative log-likelihood.

The idea is simple.

If the model gives a high probability to the correct answer, the loss is small.

If it gives a low probability to the correct answer, the loss is large.

We update the model to reduce this loss.

We repeat this process over many different simulated datasets.

In this way, the model learns a general prediction procedure that can be reused across tasks.

After training, we can give it a completely new dataset and make predictions without training it again.
-->

---
clicks: 0
class: advisor-background
---

<div class="eyebrow">These models already quantify uncertainty by producing predictive distributions</div>

# Through Which Prediction Intervals (PIs) Can Be Drawn

<PredictiveDensity />

<!--
## Slide 15 — Drawing Prediction Intervals (1 minute 30 seconds)

*The distribution and prediction interval are already visible; there are no reveal clicks on this slide.*

Now, let's look more closely at the uncertainty produced by these models.

As we have just seen, tabular foundation models can produce predictive distributions.

Here, we have an example of a predictive distribution for house prices, centered around 500 thousand pounds.

We can take the 2.5th and 97.5th percentiles of this distribution.

The blue shaded region between these two cutoffs contains 95 percent of the predictive probability.

This gives us a 95 percent prediction interval. In this example, it runs from about 343 to 657 thousand pounds.

This interval describes the price of a **new house**, given its features and the observed data.

The price of an individual house can differ from the average even when the features are similar. This is outcome noise.

But suppose we want to estimate the unknown average price, rather than predict the price of one new house.

Then we need a confidence interval for that mean.

**Prediction intervals and confidence intervals answer different questions.**

On the next slide, we will compare them directly and see how they change as we collect more data.
-->




---
clicks: 2
class: advisor-background
---

# CI v.s. PI

<IntervalLab mode="grow" />

<!--
## Slide 16 — CI vs. PI: What Changes with More Data? (1 minute 30 seconds)

Now, let's see what happens when we collect more data.

This figure shows a simple regression problem.

The horizontal axis is house size, and the vertical axis is house price.

The blue region is the prediction interval for a new house.

The green region is the confidence interval for the average price at a given house size.

Let's first look at the case with 20 observations.

We only have a small amount of data, so there is still a lot of uncertainty about the average price.

*Click once to show 80 observations.*

Now, we have 80 observations.

We can see that the green confidence band becomes narrower.

This is because we have more information to estimate the average relationship.

But the blue prediction band is still quite wide.

*Click again to show 320 observations.*

Now, we have 320 observations.

The green band becomes even narrower.

But the blue band does not shrink nearly as much.

Why?

Because even if we know the average price very well, individual house prices can still be different from that average.

This is the difference between **estimation uncertainty** and **outcome noise**.

And this is exactly the problem we want to address.

TabPFN already gives us predictive uncertainty.

But for statistical inference, we want to know how accurately we have estimated the unknown mean.

So, in the next part, I will introduce TabCon and explain how we train a model to learn this estimation uncertainty directly.
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

We first train the residual experts, then train the router with supervised fine-tuning.

Finally, we use reinforcement learning to improve the router toward our interval objectives.

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

*Click 1: reveal the three experts.*

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

*Click 2: reveal the router weights.*

Now, how do we decide which expert to use?

This is the job of the router.

The router reads information from the current dataset and produces weights for the three experts.

*Click 3: reveal Top-2 selection, the mixture, and quantile extraction together.*

We use sparse routing, which means that only two experts are selected for each task.

The third expert receives zero weight. The selected pair depends on the task; any pair of experts can be selected.

In the example shown, we combine Global with weight 0.35 and Expansion with weight 0.65; Shrinkage has zero weight.

We combine the selected experts' residual distributions using these weights.

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

In the full implementation, a small trainable encoder transforms these embeddings into query tokens. This diagram focuses on how we pool and route those representations.

But the router needs to make one decision for the whole task.

So we need to combine all the query tokens into one summary.

Here, we use two methods.

*Click 1: reveal attention pooling.*

The first method is attention.

We introduce four learned query vectors.

Each vector calculates attention weights over the query tokens.

Then it takes a weighted average of these tokens.

So, we get four different summary vectors.

Each one can focus on different information in the query set.

*Click 2: reveal mean/std pooling and the combined query-set summary.*

The second method is much simpler.

We calculate the mean and standard deviation of the query tokens.

The mean gives us information about the average representation.

The standard deviation describes how much the token values vary across the query points.

So, now we have six summary vectors in total.

Four come from attention.

One is the mean.

And one is the standard deviation.

We concatenate these vectors to get a summary of the query set.

*Click 3: reveal the feedforward network and the three softmax weights.*

In the full model, we also combine information across TabPFN ensemble members.

We then pass the result through a small neural network.

Finally, the router produces three scores, one for each expert.

We apply softmax to convert them into weights.

*Click 4: show the Top-2 weights.*

Then we keep only the two largest weights and normalize them again.

In this example, Global, Expansion, and Shrinkage start at 0.28, 0.52, and 0.20. After Top-2 selection, the weights become 0.35, 0.65, and zero.

The result is one sparse mixture shared by the query points in this task.
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

*Click 1: reveal the specialists.*

In the second stage, we train the two specialist heads.

We first look at how the Global Head performs on different datasets.

Some datasets have lower coverage than our target.

Others have higher coverage.

We use this information to train the Expansion and Shrinkage heads on different groups of datasets.

After this stage, all three residual experts are ready.

*Click 2: reveal router SFT.*

In the third stage, we train the router using supervised fine-tuning, or SFT.

At this point, the three experts are frozen.

Only the router is trained.

It learns how to combine the experts to predict the estimation residual distribution, using 50 thousand additional datasets.

*Click 3: reveal router RL.*

Finally, in the fourth stage, we use reinforcement learning on 100 thousand additional datasets to further improve the router.

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

As shown in the formula, we combine NLL with 0.20 times CRPS.

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

First, we evaluate the trained Global Head on synthetic datasets from the DGPs we want to characterize.

For each dataset, we construct confidence intervals and measure coverage across its query points.

In our method, we measure coverage at several coverage levels and combine their differences into one score.

A negative score means the model tends to undercover.

A positive score means it tends to overcover.

We collect the coverage scores across the synthetic calibration data.

The histogram is a schematic illustration of this score distribution.

We then choose two thresholds.

The first threshold is the one-third quantile.

The second threshold is the two-thirds quantile.

These thresholds divide the score distribution into relatively low, middle, and high groups. They are not simply the boundaries between negative and positive scores.

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

*Initial state: Low score is already selected. The reveal order is Low → High → Middle.*

In the first case, the coverage score is at or below the first threshold.

This places the dataset in the lower-coverage group.

So, we use NLL and CRPS to train the Expansion Head on this dataset, while also retaining its KL regularization toward Global.

Its goal is to learn a residual distribution that may help improve coverage.

For the other specialist, we use a KL loss to keep its output close to the Global Head.

*Click 1: switch to High score.*

In the second case, the coverage score is at or above the second threshold.

This places the dataset in the higher-coverage group.

So, we use NLL and CRPS to train the Shrinkage Head on this dataset, again retaining its KL regularization toward Global.

Its goal is to learn a distribution that may give shorter intervals while keeping enough coverage.

Again, the other specialist is kept close to Global using the KL loss.

*Click 2: switch to Middle score.*

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

RL starts from the SFT model and further improves the routing decisions. Both stages use Top-2 routing; the three experts remain frozen. The change is the training objective.

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

The whole example is visible at once. The four candidates shown here are illustrative.

Their rewards are 0.2, 0.8, minus 0.1, and 0.5.

A higher reward means a better result under our reward function.

Now, how do we decide which action should be encouraged?

We calculate an advantage.

In RLOO, the baseline for one candidate is the average reward of all the **other** candidates.

This is why it is called leave-one-out.

*Candidate B is selected initially. This page uses the A–D buttons, not next-slide reveal clicks.*

For example, let's consider candidate B.

Its reward is 0.8.

The other three rewards are 0.2, minus 0.1, and 0.5.

Their average is 0.2.

So, the advantage of B is 0.8 minus 0.2, which equals positive 0.6.

This means candidate B performs better than the other choices on this dataset.

We use these advantages to update the router.

The basic idea is to increase the probability of routing choices with positive advantages, and decrease the probability of choices with negative advantages.

The policy gradient is calculated using the log probability of the sampled router scores. The pi term on the slide is shorthand for this action probability.

The positive advantage-weighted log-probability expression is maximized; a gradient-descent implementation minimizes its negative.

In our actual training, we use 16 sampled routing choices per task.
-->

---
class: detail-slide
---

<div class="eyebrow">3.4. RL-based Router training</div>

# Six Reward Components

<RewardComponents />

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

The coverage score penalizes both undercoverage and overcoverage when empirical coverage deviates from the target beyond the allowed tolerance.

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

A flame means trainable, a snowflake means frozen, and a dash means not used at that stage. The two pretraining columns correspond to Global training and specialist training, respectively.

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

# Three Synthetic and One Semi-Synthetic Datasets

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

The second benchmark is the **stress-test benchmark**, which is separate from the standard ID and OOD evaluations.

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
clicks: 3
class: evidence-results
---

<div class="eyebrow">4. Strong empirical performance</div>

# Coverage and Interval Length

<BenchmarkResults />

<!--
*Suggested time: 2 minutes 20 seconds*

Now, let's look at the main results.

This figure compares TabCon with several baseline methods.

As I mentioned earlier, we need to consider coverage and interval length together.

A very short interval is not useful if it misses the true value too often.

*Standard ID is selected initially. Use the four setting buttons on this slide; advancing the slide does not switch benchmarks.*

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

*Select the Standard OOD button.*

Now, let's look at the out-of-distribution results.

TabCon still achieves about **95.3 percent coverage**.

This suggests that the model can generalize to the unseen function families in this benchmark.

*Select the Stress-test button.*

In the stress-test setting, the average coverage is about **95.6 percent**.

Again, this is close to the target.

*Select the CC18 button.*

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
clicks: 0
class: evidence-results
---

<div class="eyebrow">4. Strong empirical performance</div>

# Computation

<RuntimeChart />

<!--
*Suggested time: 1 minute 10 seconds*

Now, let's look at the computation cost.

One of the main reasons for using a foundation model is that we can reuse what it learned during training.

This is also an important advantage of TabCon.

For a new dataset, we only need to run the pretrained backbone, residual heads, and router.

We do not need to train a new model or run repeated bootstrap samples.

Here, we compare the inference time of different methods on a logarithmic time axis.

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
routeAlias: ablation
class: evidence-results
clicks: 0
---

<div class="eyebrow">4. Strong empirical performance</div>

# Ablation: Why Specialists and RL Matter

<div class="ablation-intro">Coverage probability on six DGPs · 95% nominal level</div>
<div class="ablation-figure">
<div class="ablation-chart"><span class="ablation-ylabel">Coverage probability</span><img src="/figs/ablation-figure3.svg" alt="Figure 3: coverage of Global head, SFT model, and TabCon on six selected DGPs; dashed lines mark 95%." /></div>
<div class="ablation-legend"><span><i class="global-marker"/>Global head (G)</span><span><i class="sft-marker"/>SFT model (S)</span><span><i class="tabcon-marker"/>TabCon (T)</span></div>
</div>
<div class="detail-message">Both specialists and RL training bring coverage closer to nominal level across DGPs.</div>

<!--
Source: Figure 3, https://arxiv.org/pdf/2609.33114. Original vector artwork is retained without estimating values from the chart. Global is the global head, SFT is the specialist mixture after supervised router training, and TabCon includes RL post-training. These six selected DGPs illustrate both undercoverage and overcoverage; they do not establish a universal coverage guarantee.
-->

---
class: future-research-slide
clicks: 0
---

<div class="eyebrow">Future research</div>

# A New Era of Statistical Analysis?

<div class="future-research-content">
<ul class="future-questions">
<li>Hypothesis testing?<a class="future-reference" href="https://arxiv.org/abs/2502.20925">Duong, Hoang &amp; Nguyen (2025) · Amortized Conditional Independence Testing</a></li>
<li>Variable selection?<a class="future-reference" href="https://arxiv.org/abs/2610.21950">Luo (2026) · SelectPFN</a></li>
<li>Clustering?<a class="future-reference" href="https://arxiv.org/abs/2601.21656">Zhao, Wang, Tan &amp; Zhang (2026) · TabClustPFN</a></li>
<li>Demystifying PFNs?<a class="future-reference" href="https://arxiv.org/abs/2510.23254">Ma, Wang &amp; Samworth (2025) · Optimal In-context Adaptivity and Distributional Robustness of Transformers</a></li>
</ul>
<a class="future-paper" href="https://arxiv.org/abs/2609.33114" target="_blank" rel="noopener"><img src="/figs/tabcon-paper-qr.svg" alt="QR code linking to the TabCon paper on arXiv"/><span>Read our paper</span><small>arXiv:2609.33114</small></a>
</div>

<div class="future-thanks">Thank you!</div>

<!--
Future directions extend amortized statistical inference beyond confidence intervals to hypothesis testing, variable selection, and experimental design. These are open research questions. The QR code links to https://arxiv.org/abs/2609.33114.
-->
