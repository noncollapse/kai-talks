# Kai’s talks

Research talks and short courses by [Kai Ye](https://kaiye.noncollapse.com/).

[Browse all talks](https://kaiye.noncollapse.com/kai-talks/)

- **Large Language Models: Principles and Training Methods** — [Open talk slides](https://kaiye.noncollapse.com/kai-talks/llm_short_course/) · [Abstract & contents](talks/llm_short_course/)
- **Can Tabular Foundation Models Amortize Statistical Inference? (TabCon)** — [Open talk slides](https://kaiye.noncollapse.com/kai-talks/TabCon/) · [Abstract & contents](talks/TabCon/) · [Paper](https://arxiv.org/abs/2609.33114)
- **BASIS: Batchwise Advantage Estimation from Single-Rollout Information Sharing for LLM Reasoning** — [Open talk slides](https://kaiye.noncollapse.com/kai-talks/basis/) · [Abstract & contents](talks/basis/) · [Paper](https://arxiv.org/abs/2605.27293)
- **VRPO: Robust Reinforcement Learning from Human Feedback for Large Language Models Fine-Tuning** — [Open talk slides](https://kaiye.noncollapse.com/kai-talks/vrpo/) · [Abstract & contents](talks/vrpo/) · [Paper](https://arxiv.org/abs/2504.03784)

## Hosting and updates

GitHub stores the source. Cloudflare Workers Static Assets publishes the archive at
`https://kaiye.noncollapse.com/kai-talks/`; GitHub Pages is disabled for this repository.
The root GitHub Pages redirect repository retains the old URL redirects.

After editing and pushing the source, deploy with a Cloudflare-authenticated account:

```sh
npm ci
npm run deploy:cloudflare
```

`wrangler.jsonc` routes only `/kai-talks` and `/kai-talks/*`, leaving the academic
homepage on its existing Cloudflare Pages deployment. The generated `.cloudflare-assets/`
directory preserves the `/kai-talks/` base path used by the original slide decks.
