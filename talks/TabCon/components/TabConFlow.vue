<script setup>
import { useSlideContext } from '@slidev/client'
import MathTex from './MathTex.vue'
import ModelSymbol from './ModelSymbol.vue'
import ResidualMixturePlot from './ResidualMixturePlot.vue'

const { $clicks } = useSlideContext()
const expertHeight = 86
const heads = [
  { name: 'Global', detail: 'Broad training tasks', key: 'G', color: '#ce7b26', weight: '0.35', y: 35, bars: [5, 12, 23, 33, 23, 12, 5] },
  { name: 'Expansion', detail: 'Undercoverage tasks', key: 'E', color: '#7c4dce', weight: '0.65', y: 139, bars: [10, 16, 21, 23, 21, 16, 10] },
  { name: 'Shrinkage', detail: 'Overcoverage tasks', key: 'S', color: '#0b9687', weight: '0', y: 243, bars: [2, 8, 28, 35, 28, 8, 2] },
]
const centerY = head => head.y + expertHeight / 2
const expertOutputPath = (head, index) => {
  const fromY = centerY(head)
  const toY = 65 + index * 20
  return `M455 ${fromY}H522C544 ${fromY} 544 ${toY} 566 ${toY}H664`
}
</script>

<template>
  <div class="moe-map">
    <svg class="moe-links" viewBox="0 0 876 414" aria-hidden="true">
      <defs>
        <marker id="moe-arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#a4b2cb" /></marker>
        <marker id="moe-gate-arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#cf649a" /></marker>
        <marker v-for="head in heads" :key="`marker-${head.key}`" :id="`moe-expert-arrow-${head.key}`" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0 0L8 4L0 8" :fill="head.color" /></marker>
      </defs>
      <g class="reveal" :class="{ waiting: $clicks < 1 }" fill="none" stroke="#a4b2cb" stroke-width="1.7">
        <path :d="`M178 ${centerY(heads[1])}H215`" />
        <path :d="`M215 ${centerY(heads[0])}V${centerY(heads[2])}`" />
        <path v-for="head in heads" :key="`input-${head.key}`" :d="`M215 ${centerY(head)}H232`" marker-end="url(#moe-arrow)" />
      </g>
      <path class="reveal" :class="{ waiting: $clicks < 2 }" d="M89 249V282" fill="none" stroke="#a4b2cb" stroke-width="1.7" marker-end="url(#moe-arrow)" />
      <path class="reveal gate-link" :class="{ waiting: $clicks < 2 }" :d="`M190 333H202V362H480V${centerY(heads[0])}`" fill="none" stroke="#cf649a" stroke-width="1.7" stroke-dasharray="5 4" />
      <g class="reveal" :class="{ waiting: $clicks < 3 }" fill="none" stroke-width="2" marker-end="url(#moe-arrow)">
        <path v-for="(head, i) in heads" :key="`output-${head.key}`" :d="expertOutputPath(head, i)" :stroke="head.color" :marker-end="`url(#moe-expert-arrow-${head.key})`" :stroke-dasharray="i === 2 ? '4 4' : undefined" :style="{ opacity: i === 2 ? 0.3 : 1 }" />
        <path d="M723 184V197" stroke="#a4b2cb" />
      </g>
    </svg>

    <section class="backbone">
      <h3>❄ Frozen TabPFN-v3</h3>
      <div class="backbone-symbol"><ModelSymbol /></div>
    </section>
    <span class="embedding-label reveal" :class="{ waiting: $clicks < 2 }">Query<br>embeddings</span>

    <div class="expert-label reveal" :class="{ waiting: $clicks < 1 }">Three residual experts</div>
    <section v-for="(head, i) in heads" :key="head.key" class="expert reveal"
      :class="{ waiting: $clicks < 1, inactive: $clicks >= 3 && i === 2 }"
      :style="{ top: `${head.y}px`, height: `${expertHeight}px`, '--expert': head.color }">
      <div><h3>{{ head.name }}</h3><p>{{ head.detail }}</p></div>
      <div class="expert-distribution">
        <div class="expert-bars" aria-hidden="true"><i v-for="(height, bin) in head.bars" :key="bin" :style="{ height: `${height}px` }" /></div>
        <MathTex :tex="`p_${head.key}(r)`" />
      </div>
    </section>

    <section class="router reveal" :class="{ waiting: $clicks < 2 }">
      <h3>Router</h3>
      <p>Score experts<br>→ Choose <span class="no-wrap">top-2 scores</span></p>
    </section>
    <span class="routing-label reveal" :class="{ waiting: $clicks < 2 }">Routing weights</span>
    <div v-for="(head, i) in heads" :key="`weight-${head.key}`" class="gate reveal"
      :class="{ waiting: $clicks < 2, inactive: $clicks >= 3 && i === 2 }"
      :style="{ top: `${centerY(head) - 14}px`, '--expert': head.color }">
      <b v-if="$clicks >= 3">{{ head.weight }}</b>
      <MathTex v-else :tex="`w_${head.key}`" />
    </div>

    <section class="mixture reveal" :class="{ waiting: $clicks < 3 }">
      <h3>🔥 Residual head</h3>
      <div class="mixture-symbol"><ModelSymbol color="#cf4b53" /></div>
      <div class="mixture-math"><MathTex tex="p_{\mathrm{mix}}(r)=\sum_{e\,\in\,\mathrm{Top2}}w_e\,p_e(r)" /></div>
      <p><b style="color:#ce7b26">0.35 Global</b> + <b class="violet">0.65 Expansion</b></p>
    </section>

    <div class="quantile-output reveal" :class="{ waiting: $clicks < 3 }"><h3>Extract its quantiles</h3><div class="quantile-math"><MathTex tex="Q_{1-\alpha/2}(x)" /> and <MathTex tex="Q_{\alpha/2}(x)" /></div><ResidualMixturePlot /></div>
  </div>
</template>

<style scoped>
.moe-map{position:relative;width:876px;height:414px;margin-top:18px}
.moe-links{position:absolute;inset:0;width:100%;height:100%;overflow:visible;pointer-events:none}
.moe-map section{position:absolute;box-sizing:border-box}
.moe-map h3{font-size:19px;line-height:1.3;margin:0;color:#17233e}
.backbone{left:0;top:98px;width:178px;text-align:center}
.backbone h3{font-size:17px;color:#4263eb;white-space:nowrap}
.backbone-symbol{width:150px;height:118px;margin:13px auto 0}
.embedding-label{position:absolute;left:109px;top:250px;width:91px;font-size:12px;line-height:1.3;color:#71809a}
.expert-label{position:absolute;left:235px;top:5px;font-size:13px;line-height:1.4;color:#71809a}
.expert{left:235px;width:220px;border:1px solid #dce3ef;border-left:3px solid var(--expert);border-radius:10px;background:#fff;padding:12px;display:grid;grid-template-columns:1fr 60px;gap:6px;align-items:center}
.expert h3{font-size:19px;color:var(--expert)}
.expert p{font-size:12px;line-height:1.4;color:#71809a;margin:7px 0 0}
.expert-distribution{text-align:center;font-size:14px;color:var(--expert);line-height:1.3}
.expert-bars{display:flex;align-items:flex-end;justify-content:center;gap:2px;height:35px;margin-bottom:4px}
.expert-bars i{display:block;width:5px;background:var(--expert);opacity:.65;border-radius:2px 2px 0 0}
.expert.inactive,.gate.inactive{opacity:.35}
.router{left:0;top:289px;width:190px;height:90px;border:1px solid #dce3ef;border-left:3px solid #cf649a;border-radius:10px;background:#fff;padding:12px 14px}
.no-wrap{white-space:nowrap}
.router h3{font-size:20px;color:#bd4d86}.router p{font-size:13px;line-height:1.4;color:#64748b;margin:6px 0 0}
.routing-label{position:absolute;left:321px;top:371px;font-size:12px;color:#a56385;padding:0 4px;background:#fbfcff}
.gate{position:absolute;left:463px;width:36px;height:28px;display:flex;align-items:center;justify-content:center;border:1px solid color-mix(in srgb,var(--expert) 30%,white);border-radius:6px;background:#fff;color:var(--expert);font-size:14px}
.gate b{font-weight:600}
.mixture{left:566px;top:0;width:310px;text-align:center;padding:0}
.mixture-label{font-size:12px;color:#bd4d86;margin-bottom:6px}
.mixture h3{font-size:19px;white-space:nowrap;margin:0;color:#cf4b53}
.mixture-symbol{width:120px;height:94px;margin:8px auto 0}
.mixture p{font-size:12px;line-height:1.4;margin:3px 0 0;color:#64748b}
.mixture p b{font-weight:600}
.mixture-math{font-size:17px;color:#17233e;margin:4px 0 0}
.quantile-output{position:absolute;left:566px;top:204px;width:310px;text-align:center}
.quantile-output h3{font-size:18px;margin-bottom:6px}
.quantile-math{font-size:17px;line-height:1.4;color:#52627d;margin-bottom:0}
.quantile-output :deep(.residual-mixture-plot){width:244px;margin:0 auto}
</style>
