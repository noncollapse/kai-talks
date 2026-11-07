import { defineAppSetup } from '@slidev/types'
import { slides } from '#slidev/slides'
import { isFlatMode } from '../utils/flat-mode'

export default defineAppSetup(() => {
  if (!isFlatMode) return

  // Preserve the authored final state for diagrams, while removing all hidden
  // keyboard steps. Interactive diagrams use their own local button state.
  for (const slide of slides.value) {
    const frontmatter = slide.meta.slide.frontmatter
    frontmatter.flatFinalClicks = Number(frontmatter.clicks ?? 0)
    frontmatter.clicks = 0
    frontmatter.clicksStart = 0
  }

  // Slidev pauses remote/arrow navigation while a button has focus. Release
  // pointer focus after selecting a diagram state; retain keyboard focus for
  // people navigating the buttons with Tab and Enter.
  document.addEventListener('click', (event) => {
    if (event.detail > 0 && event.target instanceof Element)
      event.target.closest<HTMLButtonElement>('.slidev-page button')?.blur()
  }, true)
})
