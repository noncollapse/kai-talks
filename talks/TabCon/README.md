# Can Tabular Foundation Models Amortize Statistical Inference?

[Open talk slides](https://noncollapse.github.io/kai-talks/TabCon/)

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

1. Opening results: 14 methods on the same ten stress settings, comparing coverage and interval length
2. A timeline of tabular learning, followed by PFNs: learning a prediction procedure across datasets
3. From predictive distributions to prediction intervals
4. Two questions: a future outcome and the underlying average
5. Why confidence intervals matter, with interactive illustrations
6. TabCon architecture: frozen embeddings, residual MLPs and task-level routing
7. Global and specialist head training: error distributions, coverage regimes and KL anchoring
8. Router SFT: Top-2 residual mixtures with straight-through gradients
9. Router RL: Top-2 actions, RLOO and verifiable interval-quality rewards
10. Trainable versus frozen parameters across the training stages
11. Evidence: Standard ID/OOD, stress tests and semi-synthetic benchmarks
12. Coverage, interval length, inference time and summary

## Local baseline verification

[Implementation audit](experiments/ci_baselines/EXPERIMENT_AUDIT.md): official APIs, fixed configurations, adapters and remaining limitations. EBM is excluded; its original outputs remain archived.

## Paper

Kai Ye, Shijin Gong, Hongyi Zhou, Valentina Zangirolami and Chengchun Shi.
[Can Tabular Foundation Models Amortize Statistical Inference?](https://arxiv.org/abs/2609.33114)
arXiv:2609.33114, 2026.
