<script setup lang="ts">
import { computed } from 'vue'
import { renderToString } from 'katex'

const props = withDefaults(defineProps<{
  tex: string
  display?: boolean
}>(), {
  display: false,
})

const html = computed(() =>
  renderToString(props.tex, {
    throwOnError: false,
    displayMode: props.display,
  }),
)
</script>

<template>
  <div v-if="display" class="math-tex-block" v-html="html" />
  <span v-else class="math-tex-inline" v-html="html" />
</template>

<style scoped>
.math-tex-inline :deep(.katex) {
  font-size: 1em;
}

.math-tex-block :deep(.katex-display) {
  margin: 0.15rem 0;
}
</style>
