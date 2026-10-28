<script setup>
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'
const { $clicks } = useSlideContext()
const showPI = computed(() => $clicks.value >= 1)
const showCI = computed(() => $clicks.value >= 2)
const x = v => 110 + (v - 220) / 560 * 656
const baseline = 174
const piRow = 239
const ciRow = 300
const y = v => baseline - 140 * Math.exp(-.5 * ((v - 500) / 80) ** 2)
const curve = Array.from({length:141}, (_,i) => `${i ? 'L' : 'M'}${x(220+i*4)},${y(220+i*4)}`).join(' ')
const area = `M${x(343.2)},${baseline} ` + Array.from({length:81}, (_,i) => `L${x(343.2+i*313.6/80)},${y(343.2+i*313.6/80)}`).join(' ') + ` L${x(656.8)},${baseline} Z`
</script>
<template>
  <svg viewBox="0 0 876 335" class="density" role="img" aria-label="Predictive distribution of house price, with a wide 95 percent prediction interval from 343 to 657 thousand pounds and a narrow illustrative confidence interval for the mean from 480 to 520 thousand pounds, shown on the same scale.">
    <path :d="area" fill="#4263eb20" class="density-reveal" :style="{ opacity: showPI ? 1 : 0 }" />
    <path :d="curve" fill="none" stroke="#4263eb" stroke-width="3" />
    <line :x1="x(500)" :x2="x(500)" y1="34" y2="315" stroke="#aebbd1" stroke-width="1" stroke-dasharray="4 5" />
    <line :x1="x(220)" :y1="baseline" :x2="x(780)" :y2="baseline" stroke="#b3bfd2" />
    <g v-for="v in [300,400,500,600,700]" :key="v"><text :x="x(v)" y="199" text-anchor="middle" fill="#64748b" style="font-size: 14px">{{v}}</text></g>
    <text x="864" y="199" text-anchor="end" fill="#8490a4" style="font-size: 13px">Price (£k)</text>
    <g class="density-reveal pi-stage" :style="{ opacity: showPI ? 1 : 0 }">
    <line v-for="v in [343.2,656.8]" :key="v" :x1="x(v)" :x2="x(v)" :y1="baseline" :y2="y(v)" stroke="#4263eb" stroke-width="1.5" stroke-dasharray="4 4" />
    <text :x="x(500)" y="121" text-anchor="middle" fill="#4263eb" style="font-size: 22px" font-weight="700">95%</text>
    <text x="8" :y="piRow+6" fill="#4263eb" style="font-size: 16px" font-weight="600">95% PI · response</text>
    <line :x1="x(343.2)" :x2="x(656.8)" :y1="piRow" :y2="piRow" stroke="#4263eb" stroke-width="4" stroke-linecap="round" />
    <line v-for="v in [343.2,656.8]" :key="`pi-${v}`" :x1="x(v)" :x2="x(v)" :y1="piRow-8" :y2="piRow+8" stroke="#4263eb" stroke-width="2" />
    <text x="864" :y="piRow+6" text-anchor="end" fill="#4263eb" style="font-size: 15px">£343k–£657k</text>
    </g>
    <g class="density-reveal ci-stage" :style="{ opacity: showCI ? 1 : 0 }">
    <text x="8" :y="ciRow+6" fill="#0b9687" style="font-size: 16px" font-weight="600">95% CI · mean</text>
    <line :x1="x(480)" :x2="x(520)" :y1="ciRow" :y2="ciRow" stroke="#0b9687" stroke-width="4" stroke-linecap="round" />
    <line v-for="v in [480,520]" :key="`ci-${v}`" :x1="x(v)" :x2="x(v)" :y1="ciRow-8" :y2="ciRow+8" stroke="#0b9687" stroke-width="2" />
    <text x="864" :y="ciRow+6" text-anchor="end" fill="#0b9687" style="font-size: 15px">£480k–£520k</text>
    </g>
  </svg>
  <div class="callout density-reveal" :style="{ opacity: showCI ? 1 : 0 }"><b>PIs for the response</b> can be much wider than <b>CIs for its mean</b>!</div>
</template>
<style scoped>.density{display:block;width:100%;height:335px}.density-reveal{transition:opacity .55s ease}</style>
