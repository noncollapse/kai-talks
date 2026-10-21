# Can Tabular Foundation Models Amortize Statistical Inference?

论文：[arXiv:2609.33114](https://arxiv.org/abs/2609.33114)

作者：Kai Ye, Shijin Gong, Hongyi Zhou, Valentina Zangirolami, Chengchun Shi。

目前只有标题页和大纲，尚未撰写正文。

[直接打开 talk](https://noncollapse.github.io/LLM_short_course/tabular_foundation_inference/)

## 大纲

1. 研究动机：为什么考虑跨数据集摊销统计推断的成本？
2. 统计目标：回归函数的置信区间，以及它与预测区间的区别。
3. 背景：表格基础模型、现有区间构造方法及其计算成本。
4. TabCon：估计误差分布、专家模型与稀疏路由。
5. 训练流程：预训练、监督微调与强化学习后训练。
6. 实验安排：覆盖率、区间长度、推断时间与消融。
7. 讨论：适用范围、局限与后续方向。

## 本地预览

在仓库根目录运行：

```bash
npm run dev -- tabular_foundation_inference
```

仅构建这个 talk：

```bash
npm run build -- tabular_foundation_inference
```

后续图片放在 `public/figs/`，在 slides 中使用 `/figs/<filename>` 引用。
