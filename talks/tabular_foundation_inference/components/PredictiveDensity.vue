<script setup>
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'
const { $clicks } = useSlideContext()
const x = v => 60+(v-220)/560*690
const y = v => 226-180*Math.exp(-.5*((v-500)/80)**2)
const curve = computed(()=>Array.from({length:141},(_,i)=>`${i?'L':'M'}${x(220+i*4)},${y(220+i*4)}`).join(' '))
const area = computed(()=>`M${x(343.2)},226 `+Array.from({length:81},(_,i)=>`L${x(343.2+i*313.6/80)},${y(343.2+i*313.6/80)}`).join(' ')+` L${x(656.8)},226 Z`)
</script>
<template>
  <svg viewBox="0 0 860 305" class="density" role="img" aria-label="A predictive distribution. Its central 95 percent spans 343 to 657 thousand pounds in this illustrative example.">
    <text x="60" y="21" fill="#64748b" style="font-size: 12px">Predictive density</text>
    <path :d="area" fill="#4263eb25" class="fade" :style="{opacity:$clicks>=1?1:0}" />
    <path :d="curve" fill="none" stroke="#4263eb" stroke-width="4" />
    <line x1="60" y1="226" x2="750" y2="226" stroke="#b3bfd2" />
    <g v-for="v in [300,400,500,600,700]" :key="v"><text :x="x(v)" y="249" text-anchor="middle" fill="#64748b" style="font-size: 13px">{{v}}</text></g>
    <g class="fade" :style="{opacity:$clicks>=1?1:0}">
      <line v-for="v in [343.2,656.8]" :key="v" :x1="x(v)" :x2="x(v)" y1="226" :y2="y(v)" stroke="#7c4dce" stroke-width="2" stroke-dasharray="4 4" />
      <text :x="x(500)" y="157" text-anchor="middle" fill="#4263eb" style="font-size: 27px" font-weight="800">95%</text>
      <text :x="x(343.2)" y="282" text-anchor="middle" fill="#7c4dce" style="font-size: 12px">2.5th percentile</text>
      <text :x="x(656.8)" y="282" text-anchor="middle" fill="#7c4dce" style="font-size: 12px">97.5th percentile</text>
    </g>
    <text x="755" y="249" text-anchor="end" fill="#8792a7" style="font-size: 11px">Price (£k)</text>
  </svg>
  <div class="callout reveal" :class="{waiting:$clicks<2}">A prediction interval for <strong>one future sale</strong>: £343k–£657k</div>
</template>
<style scoped>.density{width:100%;height:290px}.fade{transition:opacity .6s}</style>
