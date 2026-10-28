<script setup>
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'
const { $clicks } = useSlideContext()
const count = computed(() => $clicks.value >= 1 ? 20 : 1)
const offsets=[-.3,.8,-1.1,.4,1.3,-.6,0,1.6,-.9,.5,-1.5,2.4,.2,-.7,1.1,-.4,.6,-1.2,.9,-.1]
const sx=x=>300+x*55
</script>
<template>
  <div class="coverage">
    <svg viewBox="0 0 580 326" role="img" aria-label="Twenty illustrative confidence intervals from repeated datasets. Nineteen cover the fixed true average and one misses it.">
      <line :x1="sx(0)" :x2="sx(0)" y1="20" y2="310" stroke="#17233e" stroke-dasharray="5 4" stroke-width="2"/>
      <text :x="sx(0)" y="12" text-anchor="middle" fill="#17233e" style="font-size: 12px" font-weight="700">True average (fixed)</text>
      <g v-for="(o,i) in offsets" :key="i" class="coverage-trial" :style="{ opacity: i < count ? 1 : 0, transition: `opacity .35s ${i < count ? i * 35 : 0}ms` }">
        <text x="58" :y="32+i*14+4" fill="#8b97aa" style="font-size: 10px">Dataset {{i+1}}</text>
        <line :x1="sx(o-1.96)" :x2="sx(o+1.96)" :y1="32+i*14" :y2="32+i*14" :stroke="Math.abs(o)<1.96?'#0b9687':'#e06c67'" stroke-width="3" stroke-linecap="round"/>
        <circle :cx="sx(o)" :cy="32+i*14" r="3" fill="#17233e"/>
      </g>
    </svg>
    <aside><div class="eyebrow">Repeat the whole experiment</div><h3>New data.<br>New estimate.<br>New interval.</h3><p>Use <MathTex tex="1-\alpha=95\%" /> as an example.</p><span class="pill coverage-count" :style="{ opacity: $clicks >= 1 ? 1 : 0 }">On average, 19 of 20 CIs cover</span></aside>
  </div>
</template>
<style scoped>.coverage{display:grid;grid-template-columns:565px 1fr;align-items:center;gap:22px}.coverage svg{width:565px;height:330px}.coverage aside h3{font-size:27px;line-height:1.35;font-weight:800;margin:14px 0}.coverage aside p{font-size:17px;color:#64748b}.coverage .eyebrow{font-size:18px}.coverage .pill{font-size:13px;white-space:nowrap;line-height:1.5}.coverage-count{transition:opacity .4s .65s}</style>
