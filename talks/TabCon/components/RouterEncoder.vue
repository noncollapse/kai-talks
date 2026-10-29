<script setup>
import { useSlideContext } from '@slidev/client'
import MathTex from './MathTex.vue'
const { $clicks } = useSlideContext()
const attention = [[.10,.15,.40,.25,.10],[.35,.30,.10,.15,.10],[.10,.10,.15,.25,.40],[.15,.35,.25,.15,.10]]
</script>
<template>
  <div class="attention-map">
    <svg class="attention-links" viewBox="0 0 876 400" aria-hidden="true">
      <defs><marker id="attention-arrow" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#a5b1c9"/></marker></defs>
      <g fill="none" stroke="#a5b1c9" stroke-width="1.8" marker-end="url(#attention-arrow)">
        <path class="reveal" :class="{waiting:$clicks<1}" d="M185 207H200V155H215"/>
        <path class="reveal" :class="{waiting:$clicks<2}" d="M200 207V332H215"/>
        <path class="reveal" :class="{waiting:$clicks<2}" d="M565 155H573V83H590"/>
        <path class="reveal" :class="{waiting:$clicks<2}" d="M565 332H582V111H590"/>
        <path class="reveal" :class="{waiting:$clicks<3}" d="M733 142V190"/>
      </g>
      <circle class="reveal" :class="{waiting:$clicks<2}" cx="200" cy="207" r="3" fill="#a5b1c9"/>
    </svg>
    <div class="query-set">
      <h3>Query embeddings<br>from Frozen TabPFN</h3>
      <div class="embedding-rows"><div v-for="row in 5" :key="row"><MathTex :tex="`\\boldsymbol{h}_{${row}}`"/><i v-for="cell in 6" :key="cell" :style="{opacity:.25+((row*3+cell)%7)/10}"/></div></div>
    </div>
    <div class="attention-pool pooling-group reveal" :class="{waiting:$clicks<1}">
      <h3 class="outside-heading">Attention pooling</h3>
      <section class="router-panel attention-panel">
        <div class="attention-grid">
          <div class="grid-label">Learned<br>query</div><MathTex v-for="q in 5" :key="q" :tex="`\\boldsymbol{h}_{${q}}`"/><div class="grid-label">Weighted<br>summary</div>
          <template v-for="(weights,j) in attention" :key="j"><MathTex :tex="`\\boldsymbol{a}_{${j+1}}`"/><span v-for="(weight,q) in weights" :key="q" class="attention-weight" :style="{background:`rgba(207,100,154,${.07+weight*1.5})`}">{{weight.toFixed(2)}}</span><MathTex :tex="`\\boldsymbol{u}_{${j+1}}`"/></template>
        </div>
        <div class="pooling-formulas">
        <div class="pooling-formula"><MathTex tex="\boldsymbol{\alpha}_{ji}=\operatorname{softmax}_{i}\!\left(\frac{\boldsymbol{a}_j^{\top}\boldsymbol{h}_i}{\sqrt{d}}\right)"/></div>
        <div class="pooling-formula"><MathTex tex="\boldsymbol{u}_j=\sum_i\boldsymbol{\alpha}_{ji}\boldsymbol{h}_i"/></div>
        </div>
      </section>
    </div>
    <div class="query-statistics pooling-group reveal" :class="{waiting:$clicks<2}">
      <section class="router-panel statistics-panel"><MathTex tex="\mathbf{Mean}(\boldsymbol{h})"/><MathTex tex="\mathbf{Std}(\boldsymbol{h})"/></section>
      <h3 class="below-heading">Mean and std pooling</h3>
    </div>
    <div class="task-summary pooling-group reveal" :class="{waiting:$clicks<2}">
      <h3 class="outside-heading">Query-set summary</h3>
      <section class="router-panel summary-panel"><MathTex tex="\bigl[\boldsymbol{u}_1,\boldsymbol{u}_2,\boldsymbol{u}_3,\boldsymbol{u}_4,\mathbf{Mean}(\boldsymbol{h}),\mathbf{Std}(\boldsymbol{h})\bigr]"/></section>
    </div>
    <span class="routing-mlp-label reveal" :class="{waiting:$clicks<3}"><span>Feedforward</span><span>neural net</span></span>
    <section class="expert-scores router-panel reveal" :class="{waiting:$clicks<3}">
      <h3>{{ $clicks >= 4 ? 'Top-2 weights' : 'Expert weights' }}</h3>
      <div class="weight-columns">
        <div v-for="(name,i) in ['G','E','S']" :key="name" class="weight-column">
          <span>{{ ($clicks >= 4 ? [0.35,0.65,0] : [0.28,0.52,0.20])[i].toFixed(2) }}</span>
          <div class="weight-track"><i :style="{height:`${($clicks >= 4 ? [0.35,0.65,0] : [0.28,0.52,0.20])[i]*64}px`,background:['#ce7b26','#7c4dce','#0b9687'][i]}"/></div>
          <b>{{name}}</b>
        </div>
      </div>
    </section>
  </div>
</template>


<style scoped>
.attention-map{position:relative;width:876px;height:400px;margin-top:20px;font-family:inherit;font-size:14px;font-weight:400;color:#17233e}
.attention-links{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
/* Match slide 22's "Extract its quantiles" heading exactly. */
.attention-map h3{font-family:Manrope,sans-serif;font-size:18px;font-weight:800;line-height:1.3;letter-spacing:normal;margin:0;color:#17233e}
.attention-map :deep(.katex){font-size:1em!important;color:#17233e}
.router-panel{border:1px solid #dce3f1;border-left:3px solid #cf649a;border-radius:10px;background:white;text-align:center;box-sizing:border-box}
.query-set{position:absolute;left:0;top:52px;width:185px;text-align:center}
.embedding-rows{height:184px;box-sizing:border-box;margin-top:16px;border:1px solid #dce3f1;border-radius:10px;background:white;padding:12px 6px}
.embedding-rows>div{display:flex;gap:4px;align-items:center;justify-content:center;height:26px;margin:4px 0}
.embedding-rows .math-tex-inline{width:27px;font-size:18px}.embedding-rows i{height:15px;width:16px;border-radius:3px;background:#6d88c9}
.pooling-group{position:absolute;text-align:center}.outside-heading{margin-bottom:12px!important}
.attention-pool{left:215px;top:0;width:350px}.attention-panel{padding:12px 8px;height:246px}
.attention-grid{display:grid;grid-template-columns:44px repeat(5,34px) 50px;justify-content:center;gap:6px;align-items:center}
.attention-grid .math-tex-inline{font-size:18px}.grid-label{font-size:11px;color:#64748b;line-height:1.3;font-weight:400}
.attention-weight{height:24px;display:flex;align-items:center;justify-content:center;border-radius:3px;font-size:10px;font-weight:800;color:#111;font-variant-numeric:tabular-nums}
.pooling-formulas{display:flex;justify-content:center;align-items:center;gap:14px;margin-top:12px;white-space:nowrap}
.pooling-formula{font-size:17px;color:#17233e}
.query-statistics{left:215px;top:307px;width:350px}.statistics-panel{height:50px;display:flex;align-items:center;justify-content:center;gap:30px;font-size:20px}
.below-heading{margin-top:12px!important}
.task-summary{left:590px;top:24px;width:286px}.summary-panel{height:78px;display:flex;align-items:center;justify-content:center;font-size:18px;padding:8px 4px;white-space:nowrap}
.routing-mlp-label{position:absolute;left:623px;top:157px;width:220px;display:grid;grid-template-columns:100px 100px;gap:20px;font-family:inherit;font-size:14px;line-height:1.5;font-weight:400;color:#64748b;background:transparent;pointer-events:none}
.routing-mlp-label>span:first-child{text-align:right}.routing-mlp-label>span:last-child{text-align:left}
.expert-scores{position:absolute;left:616px;top:190px;width:234px;height:154px;padding:12px}
.expert-scores .weight-columns{display:flex;justify-content:center;align-items:flex-end;gap:28px;margin-top:10px}
.weight-column{display:flex;flex-direction:column;align-items:center;gap:5px}
.weight-column>span{font-size:14px;font-weight:600;font-variant-numeric:tabular-nums}
.expert-scores b{font-size:12px;font-weight:600;color:#17233e;line-height:1.1}
.weight-track{height:44px;display:flex;align-items:flex-end;border-bottom:1px solid #dce3f1;min-width:27px}
.weight-track i{display:block;width:25px;border-radius:3px 3px 0 0;transition:height .65s ease}
.attention-map .reveal.waiting{transform:none}
</style>
