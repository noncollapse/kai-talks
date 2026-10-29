<script setup>
import MathTex from './MathTex.vue'
const props = defineProps({ residual: { type:Boolean, default:false } })
const bars = Array.from({length:17},(_,i) => {
  const t = (i-8)*8
  const sigma = props.residual ? 11 : 29
  const amplitude = props.residual ? 53 : 34
  const height = amplitude * Math.exp(-0.5 * Math.pow(t / sigma, 2))
  return { x: 12 + i * 8, height }
})
</script>
<template>
  <div class="head-distribution" :class="{residual}">
    <svg viewBox="0 0 160 80" role="img" :aria-label="residual ? 'A sharp residual distribution centered at zero' : 'A broad outcome distribution'">
      <line x1="8" x2="152" y1="61" y2="61" stroke="currentColor" stroke-opacity=".25" />
      <rect v-for="(bar,i) in bars" :key="i" :x="bar.x" :y="60-bar.height" width="6" :height="Math.max(.4,bar.height)" rx="1.5" fill="currentColor" :style="{opacity:residual ? .8 : .65}" />
      <line x1="79" x2="79" y1="64" y2="68" stroke="currentColor" stroke-width="1" />
    </svg>
    <b>{{ residual ? 'Predict residuals' : 'Predict outcomes' }}</b>
    <div class="distribution-formula"><MathTex :tex="residual ? 'r(x)=\\widehat{f}(x)-f(x)' : 'Y=f(x)+\\epsilon'" /></div>
    <small v-if="!residual">This gives <MathTex tex="\widehat{f}(x)" /></small>
  </div>
</template>
<style scoped>
.head-distribution{color:#4263eb;text-align:center;margin-top:0}.head-distribution.residual{color:#cf4b53}
.head-distribution svg{display:block;width:150px;height:75px;margin:0 auto}
.head-distribution b{display:block;font-size:12px;font-weight:700;margin:3px 0 6px}
.distribution-formula{font-size:15px;white-space:nowrap}
.head-distribution small{display:block;font-size:10px;color:#64748b;margin-top:9px;white-space:nowrap}
</style>
