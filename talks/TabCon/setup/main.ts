import { defineAppSetup } from '@slidev/types'
import { slides } from '#slidev/slides'
import { isFlatMode } from '../utils/flat-mode'

export default defineAppSetup(({ router }) => {
  // Keep public URLs consistently numbered, while preserving old named links,
  // presenter links, and reveal queries such as ?clicks=2.
  router.beforeEach((to) => {
    if (to.name !== 'play' && to.name !== 'presenter') return
    const slide = slides.value.find(s => s.meta.slide.frontmatter.routeAlias === to.params.no)
    if (!slide || String(slide.no) === to.params.no) return
    const prefix = to.name === 'presenter' ? '/presenter/' : '/'
    return { path: `${prefix}${slide.no}`, query: to.query, hash: to.hash, replace: true }
  })

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
