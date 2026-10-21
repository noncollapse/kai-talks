# Large Language Models: Principles and Training Methods

Course by Chengchun Shi, Kai Ye and Shijin Gong.

## Contents

- Introduction to large language models
- Transformer foundations
- Pre-training and supervised fine-tuning
- Preference optimization and reinforcement learning from human feedback
- Reasoning and reinforcement learning with verifiable rewards

## Editing and preview

From the repository root:

```bash
npm run dev -- llm_short_course
npm run build -- llm_short_course
npm run export -- llm_short_course
```

Edit `slides.md`. The course's Vue components live in `components/`; images live in
`public/figs/` and are referenced as `/figs/<filename>` inside the slides.

The repository-wide build publishes this course at `llm_short_course/` beneath the
site's base URL. Old root URLs containing a Slidev hash route redirect here while
preserving the selected slide.
