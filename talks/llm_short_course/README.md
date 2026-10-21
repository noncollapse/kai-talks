# Large Language Models: Principles and Training Methods

Chengchun Shi · Kai Ye · Shijin Gong

[Open talk slides](https://noncollapse.github.io/kai-talks/llm_short_course/)

## Abstract

This short course introduces the principles behind large language models and
how they are trained to follow instructions and solve reasoning tasks. Starting
with tokenization, embeddings and the Transformer architecture, it develops the
objectives and intuition behind pre-training, supervised fine-tuning and
preference optimization. The course then connects inference-time reasoning with
reinforcement learning using verifiable rewards, emphasizing policy gradients,
baseline estimation and the statistical ideas behind efficient learning.

## Contents

1. Introduction to large language models
2. Tokenization, embeddings, positional encoding and Transformer foundations
3. Pre-training and supervised fine-tuning
4. Preference optimization and RLHF: reward models, PPO and DPO
5. Inference-time reasoning: chain of thought, self-consistency, tree search and ReAct
6. Reinforcement learning with verifiable rewards: GRPO, policy gradients and advantage estimation

## Papers

Selected papers covered in the course:

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — Transformer architecture.
- [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) — Instruction tuning and RLHF.
- [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347) — PPO.
- [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/abs/2305.18290) — DPO.
- [DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models](https://arxiv.org/abs/2402.03300) — GRPO and mathematical reasoning.
- [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948) — Reasoning through reinforcement learning.
