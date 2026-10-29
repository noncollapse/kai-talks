<script setup>
import MathTex from './MathTex.vue'
import HeadDistribution from './HeadDistribution.vue'
import ResidualHeadBlock from './ResidualHeadBlock.vue'
</script>
<template>
  <div class="branched-training">
    <svg class="branched-links" viewBox="0 0 876 355" aria-hidden="true">
      <g stroke="#4263eb" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <path d="M155 190H221 M215 184L221 190L215 196"/>
        <path d="M225 190V92H275M268 86L275 92L268 98"/>
        <path d="M225 190V297H275M268 291L275 297L268 303"/>
        <path d="M445 92H625M618 86L625 92L618 98"/>
      </g>
      <path d="M445 297H625M618 291L625 297L618 303" stroke="#cf4b53" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M745 153V188H360V201M354 194L360 201L366 194" stroke="#cf4b53" stroke-width="1.7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="225" cy="190" r="4" fill="#4263eb"/>
      <circle class="branch-flow regression-flow" r="3.5" fill="#4263eb"/>
      <circle class="branch-flow residual-feature-flow" r="3.5" fill="#4263eb"/>
      <circle class="branch-flow residual-supervision-flow" r="3.5" fill="#cf4b53"/>
    </svg>
    <div class="branch-data">
      <h3>Simulated dataset</h3>
      <svg viewBox="0 0 155 110" aria-label="A simulated dataset">
        <rect x="10" y="8" width="135" height="94" rx="10" fill="white" stroke="#7890bb" stroke-width="2"/>
        <rect x="19" y="17" width="117" height="16" rx="3" fill="#4263eb" fill-opacity=".65"/>
        <g v-for="r in [0,1,2,3]" :key="r"><rect v-for="c in [0,1,2,3]" :key="c" :x="21+c*29" :y="43+r*13" width="21" height="6" rx="2" fill="#4263eb" :style="{opacity:.4+((r+c)%3)*.2}"/></g>
      </svg>
      <p>Known ground truth <MathTex tex="f(x)" /></p>
    </div>
    <ResidualHeadBlock class="branch-regression"/>
    <ResidualHeadBlock class="branch-residual" residual/>
    <HeadDistribution class="branch-outcomes"/>
    <HeadDistribution class="branch-residuals" residual/>
    <div class="branch-compute"><b>Compute residual</b><MathTex tex="r(x)=\widehat{f}(x)-f(x)" /></div>
  </div>
</template>
<style scoped>
.branched-training{position:relative;width:876px;height:355px;margin-top:16px}
.branched-links{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.branch-data{position:absolute;left:0;top:123px;width:155px;text-align:center}.branch-data h3{font-size:16px;font-weight:800;margin:0 0 10px}.branch-data svg{display:block;width:150px;height:106px}.branch-data p{font-size:11px;color:#8490a4;margin-top:10px;white-space:nowrap}
.branch-regression{position:absolute;left:285px;top:0}.branch-residual{position:absolute;left:285px;top:205px}
.branch-outcomes{position:absolute;left:640px;top:5px;width:210px}.branch-residuals{position:absolute;left:640px;top:214px;width:210px}
.branch-compute{position:absolute;left:430px;top:136px;width:250px;text-align:center;color:#cf4b53;font-size:18px;display:flex;flex-direction:column;gap:6px}.branch-compute b{font-size:12px;color:#17233e}
.branch-flow{offset-distance:0%;opacity:0;animation:branchMove 7s linear infinite}.regression-flow{offset-path:path('M155 190H225V92H272')}.residual-feature-flow{offset-path:path('M155 190H225V297H272')}.residual-supervision-flow{offset-path:path('M745 153V188H360V197');animation-delay:2.5s}
@keyframes branchMove{0%{opacity:0;offset-distance:0%}5%{opacity:1}30%{opacity:1;offset-distance:100%}35%,100%{opacity:0;offset-distance:100%}}
@media(prefers-reduced-motion:reduce){.branch-flow{display:none}}
</style>
