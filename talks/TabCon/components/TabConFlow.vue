<script setup>
import { useSlideContext } from '@slidev/client'
import MathTex from './MathTex.vue'

const { $clicks } = useSlideContext()
const expertHeight = 78
const heads = [
  { name: 'Global', detail: 'Broad training tasks', key: 'G', color: '#4263eb', weight: '0.35', y: 21, bars: [5, 12, 23, 33, 23, 12, 5] },
  { name: 'Expansion', detail: 'Undercoverage tasks', key: 'E', color: '#7c4dce', weight: '0.65', y: 109, bars: [10, 16, 21, 23, 21, 16, 10] },
  { name: 'Shrinkage', detail: 'Overcoverage tasks', key: 'S', color: '#0b9687', weight: '0', y: 197, bars: [2, 8, 28, 35, 28, 8, 2] },
]
const centerY = head => head.y + expertHeight / 2
const expertOutputPath = (head, index) => {
  const fromY = centerY(head)
  const toY = 104 + index * 44
  return `M458 ${fromY}H530C554 ${fromY} 554 ${toY} 578 ${toY}H596`
}
</script>

<template>
  <div class="moe-map">
    <svg class="moe-links" viewBox="0 0 876 350" aria-hidden="true">
      <defs>
        <marker id="moe-arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#a4b2cb" /></marker>
        <marker id="moe-gate-arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="#9d80c7" /></marker>
        <marker v-for="head in heads" :key="`marker-${head.key}`" :id="`moe-expert-arrow-${head.key}`" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0 0L8 4L0 8" :fill="head.color" /></marker>
      </defs>
      <g class="reveal" :class="{ waiting: $clicks < 1 }" fill="none" stroke="#a4b2cb" stroke-width="1.7">
        <path :d="`M178 ${centerY(heads[1])}H218`" />
        <path :d="`M218 ${centerY(heads[0])}V${centerY(heads[2])}`" />
        <path v-for="head in heads" :key="`input-${head.key}`" :d="`M218 ${centerY(head)}H245`" marker-end="url(#moe-arrow)" />
      </g>
      <path class="reveal" :class="{ waiting: $clicks < 2 }" d="M89 218V262" fill="none" stroke="#a4b2cb" stroke-width="1.7" marker-end="url(#moe-arrow)" />
      <path class="reveal gate-link" :class="{ waiting: $clicks < 2 }" :d="`M235 308H491V${centerY(heads[0])}`" fill="none" stroke="#9d80c7" stroke-width="1.7" stroke-dasharray="5 4" />
      <g class="reveal" :class="{ waiting: $clicks < 3 }" fill="none" stroke-width="2" marker-end="url(#moe-arrow)">
        <path v-for="(head, i) in heads" :key="`output-${head.key}`" :d="expertOutputPath(head, i)" :stroke="head.color" :marker-end="`url(#moe-expert-arrow-${head.key})`" :stroke-dasharray="i === 2 ? '4 4' : undefined" :style="{ opacity: i === 2 ? 0.3 : 1 }" />
        <path d="M737 232V262" stroke="#0b9687" />
      </g>
    </svg>

    <section class="backbone">
      <span class="micro">Observed data + queries</span>
      <div class="context-math"><MathTex tex="D,\;x" /></div>
      <h3>Frozen TabPFN-v3</h3>
      <p>Shared query embeddings</p>
    </section>
    <span class="embedding-label reveal" :class="{ waiting: $clicks < 2 }">Same embeddings</span>

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
      <div><h3>Top-2 router</h3><span class="sparse-badge">Sparse MoE</span></div>
      <p>Learned attention pooling</p>
      <small>Score experts → keep 2 → renormalize</small>
    </section>
    <span class="routing-label reveal" :class="{ waiting: $clicks < 2 }">Task-level routing weights</span>
    <div v-for="(head, i) in heads" :key="`weight-${head.key}`" class="gate reveal"
      :class="{ waiting: $clicks < 2, inactive: $clicks >= 3 && i === 2 }"
      :style="{ top: `${centerY(head) - 14}px`, '--expert': head.color }">
      <b v-if="$clicks >= 3">{{ head.weight }}</b>
      <MathTex v-else :tex="`w_${head.key}`" />
    </div>

    <section class="mixture reveal" :class="{ waiting: $clicks < 3 }">
      <span class="micro">Mix the selected distributions</span>
      <h3>Residual mixture</h3>
      <div class="mixture-math"><MathTex tex="p_{\mathrm{mix}}(r)=\sum_{e\,\in\,\mathrm{Top2}}w_e\,p_e(r)" /></div>
      <p><b class="blue">0.35 Global</b> + <b class="violet">0.65 Expansion</b></p>
      <small>Illustrative distributions and routing weights</small>
    </section>

    <section class="interval reveal" :class="{ waiting: $clicks < 3 }">
      <h3>Confidence interval for <MathTex tex="f(x)" /></h3>
      <p>Residual quantiles + fixed TabPFN estimate <MathTex tex="\widehat f(x)" /></p>
    </section>
  </div>
</template>

<style scoped>
.moe-map{position:relative;width:876px;height:350px;margin-top:18px}
.moe-links{position:absolute;inset:0;width:100%;height:100%;overflow:visible;pointer-events:none}
.moe-map section{position:absolute;border:1px solid #dce3f1;border-radius:12px;background:#fff}
.moe-map h3{font-size:18px;font-weight:800;line-height:1.3;margin:0}
.micro{font-size:10px;color:#7887a0}
.backbone{left:0;top:78px;width:178px;height:140px;padding:15px 12px;text-align:center;background:#eef1f7!important;border-top:3px solid #929eb3!important}
.context-math{font-size:22px;margin:8px 0}
.backbone h3{font-size:16px}
.backbone p{font-size:11px;color:#64748b;margin:7px 0 0}
.embedding-label{position:absolute;left:100px;top:239px;font-size:10px;color:#8794ab}
.expert-label{position:absolute;left:248px;top:0;font-size:10px;text-transform:uppercase;letter-spacing:.1em;font-weight:700;color:#7d8ba3}
.expert{left:248px;width:210px;border-left:3px solid var(--expert)!important;padding:9px 12px;display:grid;grid-template-columns:1fr 62px;gap:8px;align-items:center}
.expert h3{color:var(--expert);font-size:17px}
.expert p{font-size:10px;color:#7c89a0;margin:5px 0 0}
.expert-distribution{text-align:center;font-size:12px;color:var(--expert);line-height:1.3}
.expert-bars{display:flex;align-items:flex-end;justify-content:center;gap:3px;height:35px;margin-bottom:3px}
.expert-bars i{display:block;width:6px;background:var(--expert);opacity:.65;border-radius:2px 2px 0 0}
.expert.inactive,.gate.inactive{opacity:.3}
.router{left:0;top:266px;width:235px;height:84px;padding:11px 13px;border-color:#d9c9ef!important;background:#f7f3fc!important}
.router>div{display:flex;align-items:center;justify-content:space-between}
.router h3{font-size:17px;color:#7c4dce}
.sparse-badge{font-size:9px;font-weight:800;color:#7c4dce;background:#ece2f8;border-radius:10px;padding:3px 6px}
.router p{font-size:11px;color:#78618f;margin:3px 0}
.router small{display:block;font-size:9px;line-height:1.3;color:#8c79a3}
.routing-label{position:absolute;left:283px;top:286px;font-size:11px;color:#8b70ad;background:#fbfcff;padding:0 6px}
.gate{position:absolute;left:466px;width:50px;height:28px;display:flex;align-items:center;justify-content:center;border:1px solid color-mix(in srgb,var(--expert) 32%,white);border-radius:7px;background:#fff;color:var(--expert);font-size:14px}
.mixture{left:598px;top:64px;width:278px;height:168px;padding:15px;text-align:center;background:#f3f6fd!important}
.mixture h3{margin-top:6px;font-size:20px}
.mixture-math{font-size:17px;margin:12px 0}
.mixture p{font-size:11px;margin:0}
.mixture small{display:block;font-size:9px;color:#8994a7;margin-top:5px}
.interval{left:598px;top:266px;width:278px;height:84px;padding:12px;text-align:center;border-color:#c7e7df!important;background:#edf9f5!important}
.interval h3{font-size:17px;color:#0b9687}
.interval p{font-size:11px;color:#65877e;margin:8px 0 0}
</style>
