# VRPO: Robust Reinforcement Learning from Human Feedback for Large Language Models Fine-Tuning

[Open talk slides](https://noncollapse.github.io/kai-talks/vrpo/)

## Abstract

Reinforcement learning from human feedback often relies on a Bradley–Terry
model of preferences, whose assumptions may not capture how people compare
responses. This talk introduces variance-reduced preference optimization
(VRPO), which uses an auxiliary preference model to improve reward and policy
estimation when the primary preference model is misspecified. Starting with
language-model training and RLHF, it explains the statistical motivation,
the role of the auxiliary model and the variance-reduction objective, then
examines experiments on controlled sentiment generation, summarization and
helpful and harmless dialogue.

## Contents

1. Large language models, tokenization and training
2. Reinforcement learning and human feedback
3. Preference modeling: Bradley–Terry models and DPO
4. Preference model misspecification
5. VRPO: auxiliary models and variance reduction
6. Experiments: IMDb, TL;DR and Anthropic Helpful and Harmless
7. Example responses and discussion

## Paper

Kai Ye, Hongyi Zhou, Jin Zhu, Francesco Quinzan and Chengchun Shi.
[Robust Reinforcement Learning from Human Feedback for Large Language Models Fine-Tuning](https://arxiv.org/abs/2504.03784)
arXiv:2504.03784, 2025.
