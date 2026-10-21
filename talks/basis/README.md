# BASIS: Batchwise Advantage Estimation from Single-Rollout Information Sharing for LLM Reasoning

[Open talk](https://noncollapse.github.io/kai-talks/basis/)

## Abstract

Reinforcement learning for language-model reasoning depends on useful advantage
estimates, but obtaining them can require a separate value model or multiple
rollouts per prompt. This talk introduces BASIS, which estimates baselines by
sharing reward information across prompts in a training batch while sampling
one rollout per prompt. It explains how an offline value signal, batchwise
refinement and online calibration work together, and examines their effects on
estimation error, training efficiency and the stability of policy learning.

## Contents

1. LLM reasoning, reinforcement learning and the role of a baseline
2. PPO and GRPO: value estimation and rollout costs
3. Sharing information across prompts in a training batch
4. Batchwise refinement and best linear unbiased estimation
5. Offline value signals and online calibration
6. The BASIS baseline and its statistical interpretation
7. Experiments: reasoning performance, estimation error, efficiency and robustness

## Paper

Shijin Gong, Erhan Xu, Kai Ye, Giulia Livieri, Francesco Quinzan and Chengchun Shi.
[BASIS: Batchwise Advantage Estimation from Single-Rollout Information Sharing for LLM Reasoning](https://arxiv.org/abs/2605.27293)
arXiv:2605.27293, 2026.
