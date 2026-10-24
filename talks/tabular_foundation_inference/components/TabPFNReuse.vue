<script setup>
import { useSlideContext } from '@slidev/client'
import MathTex from './MathTex.vue'
const { $clicks } = useSlideContext()
const bars = [8, 17, 30, 43, 33, 18, 9]
</script>

<template>
  <div class="reuse-map">
    <div class="frozen-region"><span>Reused TabPFN layers · frozen</span></div>
    <svg class="reuse-links" viewBox="0 0 876 330" aria-hidden="true">
      <defs><marker id="reuse-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7" fill="#a1afc7" /></marker></defs>
      <g fill="none" stroke="#a1afc7" stroke-width="1.6" marker-end="url(#reuse-arrow)">
        <path d="M84 162H110" /><path d="M237 162H265" /><path d="M412 162H470" marker-end="none" />
        <path d="M470 162H498V93H525" /><path d="M712 93H742" />
      </g>
      <g class="reveal" :class="{waiting:$clicks<1}" fill="none" stroke="#9d84c7" stroke-width="1.7" marker-end="url(#reuse-arrow)">
        <path d="M470 162H498V251H525" /><path d="M712 251H742" />
      </g>
      <circle cx="470" cy="162" r="4" fill="#7c8ba4" />
    </svg>
    <div class="data-node">
      <div class="data-table" aria-hidden="true"><i v-for="i in 12" :key="i" /></div>
      <b>Data + query</b><MathTex tex="D,\;x" />
    </div>
    <section class="feature-node"><span class="layer-icon">▥</span><h3>Feature<br>encoding</h3><p>Read the table</p></section>
    <section class="transformer-node"><span class="layer-icon">≋</span><h3>In-context<br>Transformer</h3><p>Learn from its context</p></section>
    <div class="representation">Query<br>embedding</div>

    <section class="original-head"><span class="status">Keep · frozen</span><h3>Original head</h3><p>Linear → GELU → Linear</p></section>
    <div class="outcome-output"><div class="distribution-bars gray-bars" aria-hidden="true"><i v-for="(h,i) in bars" :key="i" :style="{height:`${h}px`}" /></div><b>Predict outcomes</b><MathTex tex="Y=f(x)+\epsilon(x)" /><small>Also gives the fixed <MathTex tex="\widehat f(x)" /></small></div>

    <section class="residual-head reveal" :class="{waiting:$clicks<1}"><span class="status">Train · residual target</span><h3>Residual heads</h3><p>Linear → GELU → Linear</p><div class="head-tags"><b>Global</b><b>Expansion</b><b>Shrinkage</b></div></section>
    <div class="residual-output reveal" :class="{waiting:$clicks<1}"><div class="distribution-bars purple-bars" aria-hidden="true"><i v-for="(h,i) in bars" :key="i" :style="{height:`${h*.82}px`}" /></div><b>Predict estimation errors</b><MathTex tex="r(x)=\widehat f(x)-f(x)" /></div>
  </div>
  <div class="reuse-message reveal" :class="{waiting:$clicks<2}"><b>Same head design, new target.</b> Shared representations feed separately trained residual heads.</div>
</template>

<style scoped>
.reuse-map{position:relative;width:876px;height:330px;margin-top:13px}
.reuse-links{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.frozen-region{position:absolute;left:98px;top:60px;width:330px;height:195px;border:1px dashed #bdc8da;border-radius:16px;background:#f0f3f8}
.frozen-region>span{position:absolute;top:16px;left:18px;font-size:12px;color:#6c7d99;font-weight:700}
.reuse-map section{position:absolute;box-sizing:border-box;border:1px solid #d9e1ef;border-radius:12px;background:#fff;text-align:center;padding:15px 10px}
.reuse-map h3{font-size:19px;line-height:1.3;font-weight:800;margin:0}
.reuse-map p{font-size:11px;color:#78869f;margin:9px 0 0}
.data-node{position:absolute;left:0;top:114px;width:84px;text-align:center}
.data-table{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;width:54px;margin:0 auto 10px}
.data-table i{height:8px;background:#c9d3e8;border-radius:2px}
.data-table i:nth-child(3n){background:#9caee4}
.data-node b{display:block;font-size:11px;margin-bottom:8px}.data-node>.math-tex-inline{font-size:18px}
.feature-node{left:113px;top:98px;width:124px;height:129px}
.transformer-node{left:268px;top:98px;width:144px;height:129px}
.layer-icon{display:block;color:#8b9bb5;font-size:24px;margin-bottom:7px;line-height:1}
.representation{position:absolute;left:427px;top:182px;width:67px;text-align:center;font-size:10px;line-height:1.5;color:#7b89a1}
.original-head{left:528px;top:42px;width:184px;height:102px;background:#f2f4f8!important}
.status{display:block;font-size:9px;letter-spacing:.07em;text-transform:uppercase;color:#7c8ba2;margin-bottom:10px;font-weight:800}
.original-head h3{font-size:19px}
.residual-head{left:528px;top:189px;width:184px;height:124px;border-top:3px solid #7c4dce!important;background:#fcfaff!important}
.residual-head .status,.residual-head h3{color:#7c4dce}
.residual-head p{margin-top:7px}
.head-tags{display:flex;justify-content:center;gap:5px;margin-top:12px}.head-tags b{font-size:8px;padding:4px;background:#f0eafa;color:#7c4dce;border-radius:4px}
.outcome-output,.residual-output{position:absolute;left:744px;width:132px;text-align:center;font-size:13px}
.outcome-output{top:32px}.residual-output{top:192px;color:#7c4dce}
.distribution-bars{height:49px;display:flex;align-items:flex-end;justify-content:center;gap:4px;margin-bottom:10px}.distribution-bars i{width:9px;border-radius:3px 3px 0 0}
.gray-bars i{background:#9dabc4}.purple-bars i{background:#9d7ddd}
.outcome-output b,.residual-output b{display:block;font-size:11px;margin-bottom:7px}
.outcome-output small{display:block;font-size:9px;color:#7b89a1;margin-top:9px}
.reuse-message{font-size:15px;background:#edf2fc;border-left:3px solid #4263eb;border-radius:0 10px 10px 0;padding:12px 16px;margin-top:5px;color:#64748b}.reuse-message b{color:#4263eb}
</style>
