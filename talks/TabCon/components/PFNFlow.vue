<script setup>
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'
import MathTex from './MathTex.vue'
const props = defineProps({ mode: { default: 'train' } })
const { $clicks } = useSlideContext()
const step = computed(() => $clicks.value)
const tasks = [
  { name: 'A smooth relationship', color: '#4263eb', values: [8, 11, 16, 20, 27, 35, 43] },
  { name: 'A curved relationship', color: '#7c4dce', values: [37, 23, 14, 10, 14, 23, 37] },
  { name: 'Different noise levels', color: '#0b9687', values: [12, 28, 17, 38, 24, 44, 31] },
]
const rows = [[65, 2, 370], [80, 2, 405], [105, 3, 490], [120, 3, 565]]
</script>
<template>
  <div v-if="mode === 'train'" class="train-flow">
    <div class="tasks">
      <div v-for="task in tasks" :key="task.name" class="task">
        <svg viewBox="0 0 150 65" role="img" :aria-label="task.name">
          <line x1="10" y1="58" x2="140" y2="58" stroke="#d7dfec" />
          <circle v-for="(v,i) in task.values" :key="i" :cx="20+i*18" :cy="58-v" r="3.5" :fill="task.color" />
          <circle cx="128" cy="20" r="10" fill="#eef2ff" :style="{opacity:step>=1?1:0}" />
          <text x="128" y="24" text-anchor="middle" fill="#4263eb" style="font-size: 13px" font-weight="bold" :style="{opacity:step>=1?1:0}">?</text>
        </svg>
      </div>
      <div class="label">Many simulated datasets</div>
    </div>
    <div class="connector" :class="{on:step>=1}">→</div>
    <div class="transformer-model training-model" :class="{learning:step>=2}">
      <div class="transformer-stack" aria-label="Simplified stack of Transformer blocks">
        <i class="transformer-layer back-layer"></i>
        <i class="transformer-layer middle-layer"></i>
        <div class="transformer-layer front-layer">Transformer<br><small>blocks</small></div>
      </div>
      <div class="weights"><i v-for="n in 18" :key="n" :style="{'--d': `${n*70}ms`}" /></div>
    </div>
    <div class="connector" :class="{on:step>=2}">→</div>
    <div class="objective reveal" :class="{waiting:step<2}">
      <div class="target">Minimize negative log-likelihood</div>
      <div class="loss"><MathTex tex="\mathcal{L}(\theta)=\mathbb{E}_{D,(x,y)}\!\left[-\log q_\theta(y\mid x,D)\right]" display /></div>
      <div class="loss-key"><MathTex tex="D" />: datasets; <MathTex tex="(x,y)" />: predictor-label pair</div>
    </div>
  </div>
  <div v-else class="inference-flow">
    <div class="context-table">
      <table><thead><tr><th>Area</th><th>Beds</th><th>Price</th></tr></thead><tbody><tr v-for="r in rows" :key="r[0]"><td v-for="(v,j) in r" :key="j">{{v}}</td></tr><tr class="query"><td>100</td><td>3</td><td>?</td></tr></tbody></table>
    </div>
    <div class="connector" :class="{on:step>=1}">→</div>
    <div class="transformer-model" :class="{reading:step>=1}">
      <div class="transformer-stack" aria-label="Simplified stack of Transformer blocks">
        <i class="transformer-layer back-layer"></i>
        <i class="transformer-layer middle-layer"></i>
        <div class="transformer-layer front-layer">Transformer<br><small>blocks</small></div>
      </div>
    </div>
    <div class="connector" :class="{on:step>=2}">→</div>
    <div class="distribution reveal" :class="{waiting:step<2}">
      <svg viewBox="0 0 190 140" role="img" aria-label="Predictive distribution for the unknown sale price">
        <path d="M5 116 C40 116 46 108 62 65 C76 6 108 6 123 65 C139 108 149 116 184 116 L184 118 L5 118Z" fill="#4263eb20" stroke="#4263eb" stroke-width="3" />
        <line x1="5" x2="184" y1="119" y2="119" stroke="#a3b0c6" />
      </svg>
      <b>A predictive distribution of price</b>
    </div>
  </div>
  <div class="step-row"><span :class="{active:step===0}">{{mode==='train'?'1. Simulate datasets':'1. Input the data'}}</span><span :class="{active:step===1}">{{mode==='train'?'2. Mask some outcomes':'2. Read the data'}}</span><span :class="{active:step>=2}">{{mode==='train'?'3. Learn across data generating processes':'3. Predict in one pass'}}</span></div>
</template>
<style scoped>
.train-flow,.inference-flow { display:grid;align-items:center;height:340px;gap:14px; }
.train-flow { grid-template-columns:210px 34px 206px 34px minmax(0,1fr); }
.inference-flow { grid-template-columns:270px 34px 206px 34px minmax(0,1fr); }
.tasks { min-width:0; }.task { display:flex;align-items:center;background:white;border:1px solid #e0e6f0;border-radius:11px;margin:8px 0;padding:9px 13px; }.task svg { display:block;width:100%;height:72px; }.task span { font-size:12px;color:#64748b;padding-left:7px; }
.label { font-size:15px;font-weight:700;color:#64748b;margin:11px 0 0; }.connector { font-size:42px;line-height:1;text-align:center;color:#d7dfed;transition:color .5s; }.connector.on { color:#4263eb; }
.pfn { width:185px;min-height:190px;border:1px solid #c6d1fc;border-radius:22px;background:#eef2ff;display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;transition:box-shadow .5s; }.pfn strong { font-family:Manrope;font-size:44px;color:#4263eb; }.pfn span { text-align:center;font-size:15px;line-height:1.5; }.chip { font-size:10px;letter-spacing:.05em;color:#6577ac;position:absolute;top:15px; }
.objective { min-width:0;text-align:center; }.target { font-size:18px;line-height:1.4;color:#7c4dce;font-weight:700; }.loss { padding:24px 12px;margin-top:18px;background:#f3edfc;border-radius:12px;color:#7c4dce;font-size:20px; }.loss :deep(.katex) { font-size:1.05em; }.loss-key { font-size:13px;line-height:1.65;color:#7a879e;margin-top:15px; }.objective p { font-size:13px;color:#64748b;margin:12px 0 0; }
.weights { display:grid;grid-template-columns:repeat(9,10px);gap:5px;margin-top:21px; }.weights i { width:10px;height:10px;background:#c5d1fa;border-radius:2px; }.learning .weights i { animation:learn 1.8s var(--d) infinite alternate; }.lit { box-shadow:0 0 0 8px #4263eb0c; }@keyframes learn { to { background:#4263eb; } }
.context-table { min-width:0; }.context-table table { width:100%;font-size:18px;background:white;border-collapse:collapse;margin:8px 0; }.context-table td,.context-table th { padding:11px;border-bottom:1px solid #e7ebf3;text-align:center; }.context-table th { color:#8792a7;font-size:14px; }.query { color:#4263eb;background:#eef2ff;font-weight:700; }.context-table .small { font-size:12px; }
.distribution { min-width:0;text-align:center; }.distribution svg { display:block;width:250px;max-width:100%;margin:0 auto 4px; }.distribution b { display:block;font-size:18px;line-height:1.4;color:#4263eb; }.distribution p { font-size:13px;color:#64748b; }
.transformer-stack { position:relative; width:202px; height:146px; margin:0; }
.transformer-layer { position:absolute; width:174px; height:114px; border:1.5px solid #aebff3; border-radius:12px; box-sizing:border-box; }
.back-layer { left:28px; top:0; background:#d6e0fc; }
.middle-layer { left:14px; top:14px; background:#e4ebff; }
.front-layer { left:0; top:28px; display:flex; flex-direction:column; justify-content:center; align-items:center; background:white; color:#4263eb; font-size:22px; font-weight:700; line-height:1.2; box-shadow:0 4px 9px #4263eb0b; }
.front-layer small { font-size:16px; font-weight:500; margin-top:7px; color:#7f90bc; }
.transformer-model { min-width:0;min-height:220px;display:flex;align-items:center;justify-content:center; }
.training-model { flex-direction:column; }
.transformer-model .front-layer{transition:box-shadow .5s,border-color .5s}.reading .front-layer{border-color:#4263eb;box-shadow:0 0 0 7px #4263eb0d}
.step-row { margin-top:12px;gap:14px; }
.step-row span { font-size:14px;padding:7px 14px; }
</style>
