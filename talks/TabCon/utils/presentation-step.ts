import { computed, ref } from 'vue'
import { useSlideContext } from '@slidev/client'
import { isFlatMode } from './flat-mode'

export function usePresentationStep({ interactive = false } = {}) {
  const { $clicks, $frontmatter } = useSlideContext()
  const selection = ref(0)
  const step = computed(() => {
    if (!isFlatMode) return $clicks.value
    if (interactive) return selection.value
    return Number($frontmatter.flatFinalClicks ?? 0)
  })

  function selectStep(value: number) {
    if (isFlatMode && interactive) selection.value = value
  }

  return { step, selectStep, isFlatMode }
}
