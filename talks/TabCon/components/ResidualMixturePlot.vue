<script setup>
// Schematic mixture only; this is not an experimental output.
const count = 17
const normal = sigma => {
  const values = Array.from({ length: count }, (_, i) => Math.exp(-0.5 * ((i - 8) * 0.5 / sigma) ** 2))
  const total = values.reduce((a, b) => a + b, 0)
  return values.map(v => v / total)
}
const global = normal(1.0)
const expansion = normal(1.7)
const bars = global.map((p, i) => ({ global: 0.35 * p, expansion: 0.65 * expansion[i] }))
const left = 18, step = 17.4, baseline = 128, scale = 660
function quantileX(q) {
  let cumulative = 0
  for (let i = 0; i < bars.length; i++) {
    const mass = bars[i].global + bars[i].expansion
    if (cumulative + mass >= q) return left + step * (i + (q - cumulative) / mass)
    cumulative += mass
  }
  return left + count * step
}
const lower = quantileX(0.025)
const upper = quantileX(0.975)
</script>
<template>
  <svg class="residual-mixture-plot" viewBox="0 0 332 194" role="img" aria-label="Illustrative residual mixture with 0.35 Global and 0.65 Expansion weights. Dashed lines mark the 2.5th and 97.5th percentiles.">
    <g v-for="(bar, i) in bars" :key="i">
      <rect :x="left + i * step + 2" :y="baseline - bar.global * scale" width="13.4" :height="bar.global * scale" rx="1.5" fill="#ce7b26" />
      <rect :x="left + i * step + 2" :y="baseline - (bar.global + bar.expansion) * scale" width="13.4" :height="bar.expansion * scale" rx="1.5" fill="#a17adb" />
    </g>
    <line x1="18" x2="315" :y1="baseline" :y2="baseline" stroke="#bdc9dd" />
    <g stroke="#0b9687" stroke-width="1.5" stroke-dasharray="3 4"><line :x1="lower" :x2="lower" y1="14" y2="136" /><line :x1="upper" :x2="upper" y1="14" y2="136" /></g>
    <text :x="lower" y="153" text-anchor="middle" fill="#0b9687">2.5%</text>
    <text :x="upper" y="153" text-anchor="middle" fill="#0b9687">97.5%</text>
    <g class="mixture-legend"><rect x="61" y="174" width="8" height="8" rx="2" fill="#ce7b26" /><text x="76" y="182">0.35 Global</text><rect x="181" y="174" width="8" height="8" rx="2" fill="#a17adb" /><text x="196" y="182">0.65 Expansion</text></g>
  </svg>
</template>
<style scoped>
.residual-mixture-plot{display:block;width:100%;height:auto;overflow:visible}
.residual-mixture-plot text{font-family:'DM Sans',sans-serif;font-size:12px}
.mixture-legend{fill:#64748b}
</style>
