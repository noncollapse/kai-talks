# Can Tabular Foundation Models Amortize Statistical Inference?

[Open talk slides](https://noncollapse.github.io/kai-talks/tabular_foundation_inference/)

## Abstract

Can a model learn to construct confidence intervals across datasets, reducing
the need to repeat costly inference procedures for each new problem? This talk
introduces TabCon, a system built on a tabular foundation model for amortizing
statistical inference. It focuses on confidence intervals for regression
functions, combining sparse expert routing with reinforcement learning to
calibrate coverage. The discussion examines the balance between coverage,
interval length and computational cost, and the scope of inference learned
across problems.

## Contents

The current slides contain the title and outline for the following topics:

1. Motivation: amortizing statistical inference across datasets
2. Statistical target: confidence intervals for regression functions versus prediction intervals
3. Background: tabular foundation models and uncertainty quantification
4. TabCon: estimation-error distributions and sparse expert routing
5. Training: pre-training, supervised fine-tuning and reinforcement learning
6. Evaluation: coverage, interval length, inference time and ablations
7. Discussion: scope, limitations and future directions

## Paper

Kai Ye, Shijin Gong, Hongyi Zhou, Valentina Zangirolami and Chengchun Shi.
[Can Tabular Foundation Models Amortize Statistical Inference?](https://arxiv.org/abs/2609.33114)
arXiv:2609.33114, 2026.
