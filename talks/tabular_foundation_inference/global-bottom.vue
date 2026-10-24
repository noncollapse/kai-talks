<script setup lang="ts">
import { useSlideContext } from '@slidev/client'

const { $nav } = useSlideContext()
</script>

<template>
  <div class="slide-page-number">
    {{ $nav.currentSlideNo }}/{{ $nav.total }}
  </div>
</template>

<style scoped>
.slide-page-number {
  position: absolute;
  right: 1.1rem;
  bottom: 0.65rem;
  z-index: 40;
  color: rgb(100 116 139 / 78%);
  font-family: 'Inter', 'Noto Sans SC', sans-serif;
  font-size: 0.62rem;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  line-height: 1;
  letter-spacing: 0.04em;
  pointer-events: none;
  user-select: none;
}
</style>
