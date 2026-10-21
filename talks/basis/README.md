# BASIS

**Batchwise Advantage Estimation from Single-Rollout Information Sharing for LLM Reasoning**

Kai Ye · Department of Statistics, LSE & Stats-Powered AI Lab

- [Open the web talk](https://noncollapse.github.io/kai-talks/basis/)
- [Original PowerPoint](source/bas.pptx)

The web version preserves all 25 slides and their original order, figures,
equations and layout. PowerPoint's native PDF export provides the page artwork,
which is converted into scalable SVGs and presented with Slidev. Use the arrow
keys to move between slides, or Slidev's controls for fullscreen and slide overview.
PowerPoint animations are shown in their exported static state.

## Editing and preview

```bash
# From the repository root
npm run dev -- basis
npm run build -- basis
```

Edit `source/bas.pptx` in PowerPoint to change the original content. The slide
images are generated assets; the text in `slides.md` supplies accessible slide
content and does not change the visible artwork.

To regenerate after editing:

1. Export all slides from PowerPoint to PDF using **Best for printing**. This
   preserves the source fonts and mathematical notation.
2. Update `slide-titles.json` if the slide titles or order change.
3. With Python 3 and Poppler installed, run:

   ```bash
   python3 talks/basis/convert.py /path/to/exported.pdf
   ```

   Use `--pdftocairo /path/to/pdftocairo --pdfinfo /path/to/pdfinfo` when those
   programs are not on `PATH`.
4. Preview the result, then commit the source PPTX, `slides.md` and
   `public/slides/` together. Normal site builds use the committed SVG files and
   do not require PowerPoint or Poppler.
