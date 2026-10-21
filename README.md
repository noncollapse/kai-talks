# Kai’s talks

- **Large Language Models: Principles and Training Methods** — [Open talk](https://noncollapse.github.io/kai-talks/llm_short_course/) · [Source](talks/llm_short_course/)
- **Can Tabular Foundation Models Amortize Statistical Inference? (TabCon)** — [Open talk](https://noncollapse.github.io/kai-talks/tabular_foundation_inference/) · [Source](talks/tabular_foundation_inference/) · Title and outline
- **BASIS: Batchwise Advantage Estimation from Single-Rollout Information Sharing for LLM Reasoning** — [Open talk](https://noncollapse.github.io/kai-talks/basis/) · [Source](talks/basis/) · 25 slides converted from PowerPoint

[Browse all talks](https://noncollapse.github.io/kai-talks/)

## Description

Research talks and short courses by [Kai Ye](https://noncollapse.github.io/).
Each talk has its own Slidev source, figures and optional Vue components. Node
dependencies and development, build and export commands are shared at the root.

## Adding a talk

1. Create `talks/<name>/slides.md`, using a lowercase directory name with underscores
   or hyphens. Include the usual Slidev frontmatter, including `theme: default`.
2. Add a `talk.json` with the title and description for the archive page:

   ```json
   {
     "title": "Your talk title",
     "description": "A short description.",
     "draft": true
   }
   ```

3. Put figures in `talks/<name>/public/figs/` and any custom components in
   `talks/<name>/components/`. Reference figures as `/figs/<filename>` in Slidev.
4. Preview with `npm run dev -- <name>`. No root configuration change is needed.
5. When ready to publish, set `draft` to `false`, commit the talk, and add its source
   and live slide links to the list in this README.

`draft: true` excludes a talk from the default site build. It does **not** hide
committed source files on GitHub. Keep private work untracked until it is ready
to share; stage specific paths when committing other changes.

## Building and deployment

```bash
# Build all non-draft talks and the archive page
npm run build

# Build just one talk and an index pointing to it
npm run build -- llm_short_course

# Include drafts in a local preview build
npm run build -- --include-drafts

# Build for a site hosted below a URL prefix
BASE_PATH=/kai-talks/ npm run build

# Serve the built site locally (use the default BASE_PATH=/ for this)
python3 -m http.server 8080 --directory dist
```

Each build replaces `dist/`, including any previously built drafts. The archive
is at `dist/index.html`; each deck is at `dist/<name>/index.html`.

GitHub Pages deploys on pushes to `main` or manual workflow runs. Set the repository's
Pages source to **GitHub Actions**. The workflow obtains the URL prefix from Pages
configuration, so the build is not tied to the current repository name.

Links of the form `/#/slide` at the site root redirect to `llm_short_course/#/slide`.
The site root displays the talk archive. After the repository rename, published
talks use the `/kai-talks/` URL prefix; GitHub Pages does not redirect the former
`/LLM_short_course/` URLs.
