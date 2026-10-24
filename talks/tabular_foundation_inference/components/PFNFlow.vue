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
        <span>{{ task.name }}</span>
      </div>
      <div class="label">Many simulated datasets</div>
    </div>
    <div class="connector" :class="{on:step>=1}">→</div>
    <div class="pfn" :class="{learning:step>=2}">
      <div class="chip">Shared parameters</div><strong>PFN</strong><span>Learn to predict<br>held-out outcomes</span>
      <div class="weights"><i v-for="n in 18" :key="n" :style="{'--d': `${n*70}ms`}" /></div>
    </div>
    <div class="connector" :class="{on:step>=2}">→</div>
    <div class="objective reveal" :class="{waiting:step<2}">
      <div class="target">Prior-data negative log-likelihood</div>
      <div class="loss"><MathTex tex="\begin{gathered}\mathcal{L}(\theta)=\\[3pt]\mathbb{E}_{D,(x,y)}\!\left[-\log q_\theta(y\mid x,D)\right]\end{gathered}" display /></div>
      <div class="loss-key"><MathTex tex="D" />: context rows<br><MathTex tex="(x,y)" />: a held-out row from the same task</div>
      <p>Minimize across simulated tasks.<br>Update the shared parameters θ.</p>
    </div>
  </div>
  <div v-else class="inference-flow">
    <div class="context-table">
      <div class="label">A new dataset</div>
      <table><thead><tr><th>Area</th><th>Beds</th><th>Price</th></tr></thead><tbody><tr v-for="r in rows" :key="r[0]"><td v-for="(v,j) in r" :key="j">{{v}}</td></tr><tr class="query"><td>100</td><td>3</td><td>?</td></tr></tbody></table>
      <span class="small">Observed rows are the context.</span>
    </div>
    <div class="connector" :class="{on:step>=1}">→</div>
    <div class="pfn" :class="{lit:step>=1}"><div class="chip">Weights fixed</div><strong>PFN</strong><span>Read the table<br>and the query</span></div>
    <div class="connector" :class="{on:step>=2}">→</div>
    <div class="distribution reveal" :class="{waiting:step<2}">
      <svg viewBox="0 0 190 140" role="img" aria-label="Predictive distribution for the unknown sale price">
        <path d="M5 116 C40 116 46 108 62 65 C76 6 108 6 123 65 C139 108 149 116 184 116 L184 118 L5 118Z" fill="#4263eb20" stroke="#4263eb" stroke-width="3" />
        <line x1="5" x2="184" y1="119" y2="119" stroke="#a3b0c6" />
        <text x="95" y="138" text-anchor="middle" fill="#64748b" style="font-size: 11px">Possible sale prices</text>
      </svg>
      <b>A predictive distribution</b><p>Several prices remain plausible.</p>
    </div>
  </div>
  <div class="step-row"><span :class="{active:step===0}">{{mode==='train'?'1. Simulate tasks':'1. Supply context'}}</span><span :class="{active:step===1}">{{mode==='train'?'2. Hide some outcomes':'2. Read the query'}}</span><span :class="{active:step>=2}">{{mode==='train'?'3. Learn across tasks':'3. Predict in one pass'}}</span></div>
</template>
<style scoped>
.train-flow,.inference-flow { display:flex;align-items:center;justify-content:space-between;height:300px;gap:14px; }
.tasks { width:210px; }.task { display:flex;align-items:center;background:white;border:1px solid #e0e6f0;border-radius:11px;margin:8px 0;padding:8px; }.task svg { width:95px;flex-shrink:0; }.task span { font-size:12px;color:#64748b;padding-left:7px; }
.label { font-size:13px;font-weight:700;color:#64748b;margin:10px 0; }.connector { font-size:35px;color:#d7dfed;transition:color .5s; }.connector.on { color:#4263eb; }
.pfn { width:185px;min-height:190px;border:1px solid #c6d1fc;border-radius:22px;background:#eef2ff;display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;transition:box-shadow .5s; }.pfn strong { font-family:Manrope;font-size:44px;color:#4263eb; }.pfn span { text-align:center;font-size:15px;line-height:1.5; }.chip { font-size:10px;letter-spacing:.05em;color:#6577ac;position:absolute;top:15px; }
.objective { width:290px;flex-shrink:0;text-align:center; }.target { font-size:14px;color:#7c4dce;font-weight:700; }.loss { padding:17px 10px;margin-top:13px;background:#f3edfc;border-radius:12px;color:#7c4dce;font-size:18px; }.loss :deep(.katex) { font-size:1.05em; }.loss-key { font-size:11px;line-height:1.7;color:#8591a7;margin-top:12px; }.objective p { font-size:13px;color:#64748b;margin:12px 0 0; }
.weights { display:grid;grid-template-columns:repeat(9,7px);gap:4px;margin-top:14px; }.weights i { width:7px;height:7px;background:#c5d1fa;border-radius:2px; }.learning .weights i { animation:learn 1.8s var(--d) infinite alternate; }.lit { box-shadow:0 0 0 8px #4263eb0c; }@keyframes learn { to { background:#4263eb; } }
.context-table { width:255px; }.context-table table { width:100%;font-size:15px;background:white;border-collapse:collapse;margin:8px 0; }.context-table td,.context-table th { padding:9px;border-bottom:1px solid #e7ebf3;text-align:center; }.context-table th { color:#8792a7;font-size:12px; }.query { color:#4263eb;background:#eef2ff;font-weight:700; }.context-table .small { font-size:12px; }
.distribution { width:205px;text-align:center; }.distribution svg { width:190px; }.distribution b { font-size:15px;color:#4263eb; }.distribution p { font-size:13px;color:#64748b; }
</style>
