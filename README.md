# Talks

Research talks and short courses by [Kai Ye](https://noncollapse.github.io/).
Each talk has its own Slidev source, figures and optional Vue components. Node
dependencies and development, build and export commands are shared at the root.

## Talks

- [Large Language Models: Principles and Training Methods](talks/llm_short_course/)

Run `npm run list` to see all talks available in your checkout, including local drafts.

## Getting started

Use Node.js 20 or newer, then install the locked dependencies:

```bash
npm ci
npm run list
npm run dev -- llm_short_course
```

Open the address printed by Slidev (normally `http://localhost:3030`). `npm run dev`
without a name opens the LLM course. Additional Slidev options are forwarded:

```bash
npm run dev -- llm_short_course --port 3031 --open
npm run export -- llm_short_course
```

Export uses Slidev's defaults and writes into the talk's directory. PDF export
requires Slidev's optional Playwright browser support.

## Repository structure

```text
talks/
  llm_short_course/
    slides.md
    talk.json
    README.md
    components/
    public/figs/
    global-bottom.vue
scripts/
  talks.mjs               # Discover, preview, build and export talks
  index.html              # Shared archive page template
package.json
package-lock.json
.github/workflows/deploy.yml
```

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
5. When ready to publish, set `draft` to `false`, commit the talk, and add it to the
   list in this README.

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
BASE_PATH=/LLM_short_course/ npm run build

# Serve the built site locally (use the default BASE_PATH=/ for this)
python3 -m http.server 8080 --directory dist
```

Each build replaces `dist/`, including any previously built drafts. The archive
is at `dist/index.html`; each deck is at `dist/<name>/index.html`.

GitHub Pages deploys on pushes to `main` or manual workflow runs. Set the repository's
Pages source to **GitHub Actions**. The workflow obtains the URL prefix from Pages
configuration, so the build is not tied to the current repository name.

Existing links of the form `/#/slide` at the old course URL redirect to
`llm_short_course/#/slide`. The site root now displays the talk archive.

## Technology

[Slidev](https://sli.dev/) provides Markdown slides, Vue components, KaTeX equations
and interactive presentation controls. This repository is for educational purposes.
