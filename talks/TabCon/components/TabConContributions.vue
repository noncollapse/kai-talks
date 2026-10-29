<script setup>
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'
const props = defineProps({ active: { type:Number, default:0 } })
const { $clicks } = useSlideContext()
const selected = computed(() => props.active || ($clicks.value >= 1 ? 1 : 0))
</script>

<template>
  <div class="tabcon-roadmap contributions-roadmap" :class="{'contribution-focused':selected > 0}">
    <section :class="{chosen:selected === 1}"><span>1</span><div><h2>Amortized CI construction</h2><p>A new methodology based on residual distributions</p></div></section>
    <section :class="{chosen:selected === 2}"><span>2</span><div><h2>A new model architecture</h2><p>A sparse mixture of experts for tabular foundation models</p></div></section>
    <section :class="{chosen:selected === 3}"><span>3</span><div><h2>A new training paradigm</h2><p>Pretraining followed by post-training</p></div></section>
    <section :class="{chosen:selected === 4}"><span>4</span><div><h2>Strong empirical performance</h2><p>Near-nominal coverage, short intervals, fast inference</p></div></section>
  </div>
</template>
<style scoped>
.contributions-roadmap{margin-top:35px;row-gap:22px;column-gap:42px}
.contributions-roadmap h2{font-size:25px;line-height:1.3}
.contributions-roadmap section{gap:18px}
.contributions-roadmap h2,.contributions-roadmap p,.contributions-roadmap section>span{transition:color .35s ease}
.contribution-focused section:not(.chosen) h2{color:#a1adbf}
.contribution-focused section:not(.chosen)>span{color:#c5cedd}
.contribution-focused section:not(.chosen) p{color:#b0b9c8}
.contribution-focused section.chosen>span{color:#4263eb}
.contribution-focused section.chosen p{color:#53637c}
</style>
