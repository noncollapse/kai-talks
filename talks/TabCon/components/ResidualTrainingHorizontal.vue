<script setup>
import MathTex from './MathTex.vue'
import HeadDistribution from './HeadDistribution.vue'
</script>

<template>
  <div class="residual-training-flow">
    <section class="simulation-stage">
      <h3>Simulated dataset</h3>
      <svg viewBox="0 0 155 130" class="synthetic-table" aria-label="A simulated dataset with predictors and labels">
        <rect x="10" y="18" width="135" height="94" rx="10" fill="white" stroke="#7890bb" stroke-width="2" />
        <rect x="19" y="27" width="117" height="16" rx="3" fill="#4263eb" fill-opacity=".65" />
        <g v-for="r in [0,1,2,3]" :key="r"><rect v-for="c in [0,1,2,3]" :key="c" :x="21+c*29" :y="53+r*13" width="21" height="6" rx="2" fill="#4263eb" :style="{opacity:.4+((r+c)%3)*.2}" /></g>
      </svg>
      <p>Known ground truth</p>
      <div class="truth-formula"><MathTex tex="f(x)" /></div>
    </section>
    <div class="training-connector first-connector" aria-hidden="true"><svg viewBox="0 0 26 30" aria-hidden="true"><path d="M1 15H24M18 9L24 15L18 21" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><i /></div>
    <section class="head-stage regression-stage">
      <h3>Regression head</h3>
      <div class="training-badge frozen"><span aria-hidden="true">❄</span> Frozen</div>
      <div class="idea-model-stack"><i></i><i></i><div><svg class="head-network" viewBox="0 0 110 76" aria-hidden="true"><g stroke="currentColor" stroke-width="2" stroke-opacity=".45" fill="none"><path d="M15 13L55 21L95 13M15 13L55 55L95 13M15 63L55 21L95 63M15 63L55 55L95 63"/></g><g fill="currentColor"><circle cx="15" cy="13" r="5"/><circle cx="15" cy="63" r="5"/><circle cx="55" cy="21" r="5"/><circle cx="55" cy="55" r="5"/><circle cx="95" cy="13" r="5"/><circle cx="95" cy="63" r="5"/></g></svg></div></div>
      <HeadDistribution />
    </section>
    <div class="training-connector second-connector" aria-hidden="true"><svg viewBox="0 0 26 30" aria-hidden="true"><path d="M1 15H24M18 9L24 15L18 21" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><i /></div>
    <section class="residual-stage">
      <h3>Compute residual</h3>
      <div class="residual-equation"><MathTex tex="r(x)=\widehat{f}(x)-f(x)" /></div>
      <p>Estimate − ground truth</p>
    </section>
    <div class="training-connector third-connector" aria-hidden="true"><svg viewBox="0 0 26 30" aria-hidden="true"><path d="M1 15H24M18 9L24 15L18 21" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><i /></div>
    <section class="head-stage residual-head-stage">
      <h3>Residual head</h3>
      <div class="training-badge trainable"><span aria-hidden="true">🔥</span> Trainable</div>
      <div class="idea-model-stack residual-stack"><i></i><i></i><div><svg class="head-network" viewBox="0 0 110 76" aria-hidden="true"><g stroke="currentColor" stroke-width="2" stroke-opacity=".45" fill="none"><path d="M15 13L55 21L95 13M15 13L55 55L95 13M15 63L55 21L95 63M15 63L55 55L95 63"/></g><g fill="currentColor"><circle cx="15" cy="13" r="5"/><circle cx="15" cy="63" r="5"/><circle cx="55" cy="21" r="5"/><circle cx="55" cy="55" r="5"/><circle cx="95" cy="13" r="5"/><circle cx="95" cy="63" r="5"/></g></svg></div></div>
      <HeadDistribution residual />
    </section>
  </div>
</template>

<style scoped>
.residual-training-flow{display:grid;grid-template-columns:155px 26px 170px 26px 200px 26px 190px;gap:12px;align-items:start;margin-top:28px}
.residual-training-flow section{text-align:center;min-width:0}
.residual-training-flow h3{font-size:17px;font-weight:800;line-height:1.3;color:#17233e;margin:0 0 14px}
.synthetic-table{width:145px;height:130px;margin-top:27px}
.residual-training-flow p{font-size:12px;color:#8490a4;line-height:1.4;margin:9px 0}
.truth-formula,.estimate-formula{font-size:23px;color:#4263eb}
.training-badge{display:flex;gap:7px;align-items:center;justify-content:center;font-size:12px;font-weight:700;margin-bottom:22px}.frozen{color:#4263eb}.trainable{color:#cf4b53}.training-badge span{font-size:22px;line-height:1}
.idea-model-stack{position:relative;width:145px;height:100px;margin:0 auto 6px;--head-color:#4263eb;--head-border:#a4b6ee;--head-fill:#eef2ff}
.idea-model-stack>i,.idea-model-stack>div{position:absolute;width:129px;height:82px;border-radius:11px;border:1.5px solid var(--head-border);box-sizing:border-box;background:var(--head-fill)}
.idea-model-stack>i:first-child{left:16px;top:0}.idea-model-stack>i:nth-child(2){left:8px;top:8px}
.idea-model-stack>div{left:0;top:16px;background:white;display:flex;align-items:center;justify-content:center;text-align:center;font-size:14px;line-height:1.4;font-weight:700;color:var(--head-color)}
.residual-stack{--head-color:#cf4b53;--head-border:#e7acb0;--head-fill:#fff0f1}
.residual-equation{font-size:20px;padding:19px 0;border-top:1px solid #e1e6ef;border-bottom:1px solid #e1e6ef;margin-top:76px;color:#17233e}
.learned-residual{display:block;width:145px;height:58px;margin:0 auto}
.training-connector{position:relative;font-size:30px;color:#4263eb;margin-top:123px;line-height:1;text-align:center}
.training-connector small{position:absolute;font-size:9px;left:50%;transform:translateX(-50%);top:-20px;color:#cf4b53}
.training-connector i{position:absolute;width:5px;height:5px;border-radius:50%;background:#4263eb;top:15px;left:0;transform:translate(-50%,-50%);opacity:0;animation:residualDataFlow 7s linear infinite}
.second-connector i{animation-delay:1.5s}.third-connector{color:#cf4b53}.third-connector i{background:#cf4b53;animation-delay:3s}
.shared-representations{margin:3px 0 0 200px;width:650px;border-bottom:1px dashed #a4b6ee;text-align:center;padding-bottom:8px;color:#7d90b8;font-size:10px}
.residual-idea-note{font-size:13px;color:#64748b;margin-top:17px;text-align:center}
.residual-stack{animation:residualHeadLearn 3s ease-in-out infinite}
@keyframes residualDataFlow{0%{left:0;opacity:0}5%{opacity:1}20%{left:21.5px;opacity:1}24%,100%{left:21.5px;opacity:0}}
@keyframes residualHeadLearn{0%,100%{filter:drop-shadow(0 0 0 #cf4b5300)}50%{filter:drop-shadow(0 0 7px #cf4b5325)}}
@media(prefers-reduced-motion:reduce){.training-connector i{display:none}.residual-stack{animation:none}}
.head-network{width:95px;height:66px}
.training-connector>svg{display:block;width:26px;height:30px}
</style>
