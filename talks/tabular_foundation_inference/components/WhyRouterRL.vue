<script setup>
import { useSlideContext } from '@slidev/client'
import MathTex from './MathTex.vue'
const { $clicks } = useSlideContext()
const experts = [
  { name: 'Global', color: '#4263eb', dense: '.25', sparse: '.29' },
  { name: 'Expansion', color: '#9161d5', dense: '.60', sparse: '.71' },
  { name: 'Shrinkage', color: '#0b9687', dense: '.15', sparse: '0' },
]
</script>

<template>
  <div class="why-rl">
    <section class="motivation routing-motivation">
      <div class="motivation-label">01 · Routing</div>
      <h3>Do we need every expert?</h3>
      <div class="dense-example">
        <span class="example-label">Dense mixture · all weights active</span>
        <div class="expert-tiles"><div v-for="expert in experts" :key="expert.name" :style="{ '--expert': expert.color }"><span>{{ expert.name }}</span><b>{{ expert.dense }}</b></div></div>
      </div>
      <p class="routing-reason">Expansion and Shrinkage serve different regimes.<br>Mixing both is not always needed.</p>
      <div class="rl-reveal" :class="{ hidden: $clicks < 1 }">
        <div class="down-link"><span>↓</span><b>Top-2: select, then renormalize</b></div>
        <div class="expert-tiles sparse-tiles"><div v-for="(expert, i) in experts" :key="expert.name" :class="{ inactive: i === 2 }" :style="{ '--expert': expert.color }"><span>{{ expert.name }}</span><b>{{ expert.sparse }}</b></div></div>
        <div class="sparse-benefits"><b>Less head computation: two instead of three.</b></div>
      </div>
    </section>

    <section class="motivation objective-motivation">
      <div class="motivation-label">02 · Objective</div>
      <h3>Fit the distribution. Assess the CI.</h3>
      <div class="distribution-objective">
        <span class="example-label">SFT · distribution quality</span>
        <MathTex tex="\mathcal L_{\mathrm{SFT}}=\mathrm{NLL}+\eta_3\,\mathrm{CRPS}" />
      </div>
      <p class="objective-reason">Does not directly optimize<br><b>coverage probability or interval length.</b></p>
      <div class="rl-reveal" :class="{ hidden: $clicks < 2 }">
        <div class="down-link"><span>↓</span><b>RL: reward the resulting intervals</b></div>
        <div class="interval-objective">
          <div class="interval-icon" aria-hidden="true"><i class="interval-wide" /><i class="interval-tight" /><b /></div>
          <div><b>Coverage near the target</b><span>Shorter intervals, while preserving coverage</span></div>
        </div>
      </div>
    </section>

    <div class="why-rl-message rl-reveal" :class="{ hidden: $clicks < 2 }"><span>Sparse routing + RL</span><b>Select a few experts. Optimize the CI they produce.</b></div>
  </div>
</template>

<style scoped>
.why-rl{display:grid;grid-template-columns:1fr 1fr;gap:18px;width:876px;margin-top:21px}
.motivation{box-sizing:border-box;height:333px;border:1px solid #dce4f2;border-radius:15px;background:#fff;padding:18px 20px}
.motivation-label{font-size:10px;letter-spacing:.1em;text-transform:uppercase;font-weight:800;color:#7c4dce;margin-bottom:10px}.objective-motivation .motivation-label{color:#0b9687}
.motivation h3{font-size:20px;font-weight:800;line-height:1.3;letter-spacing:-.4px;margin:0 0 16px;color:#17233e}
.example-label{display:block;font-size:10px;font-weight:600;color:#7e8ca4;margin-bottom:8px}
.expert-tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.expert-tiles>div{display:flex;align-items:center;justify-content:space-between;gap:5px;border:1px solid #e3e7f1;border-top:2px solid var(--expert);background:#fafbff;border-radius:6px;padding:9px 8px;color:var(--expert);height:41px;box-sizing:border-box}.expert-tiles>div>span{font-size:9px;font-weight:700}.expert-tiles>div>b{font-size:15px;line-height:1}
.routing-reason,.objective-reason{font-size:12px;line-height:1.55!important;color:#73819a;margin:13px 0 0;height:38px}.objective-reason b{font-weight:600;color:#51627f}
.down-link{display:flex;align-items:center;gap:10px;height:39px;margin:3px 0 3px;color:#7c4dce}.down-link>span{font-size:24px;line-height:1}.down-link>b{font-size:11px;font-weight:700}.objective-motivation .down-link{color:#0b9687}
.sparse-tiles>div{background:#f5f1fc}.sparse-tiles>div.inactive{background:#f5f6f9;border-color:#e2e6ee;color:#aab3c4}.sparse-tiles>div.inactive>span{text-decoration:line-through}
.sparse-benefits{margin-top:12px}.sparse-benefits>b{font-size:12px;color:#7c4dce}
.distribution-objective{height:63px;box-sizing:border-box}.distribution-objective>.math-tex-inline{display:block;font-size:22px;line-height:1.5;color:#4263eb;margin-top:5px}
.interval-objective{display:flex;align-items:center;gap:16px;border-radius:9px;background:#edf8f5;height:66px;padding:10px 13px;box-sizing:border-box}.interval-objective>div:last-child{display:flex;flex-direction:column;gap:7px}.interval-objective>div:last-child>b{font-size:13px;color:#0b9687}.interval-objective>div:last-child>span{font-size:9px;color:#6c8e89}
.interval-icon{position:relative;width:65px;height:38px;flex-shrink:0}.interval-wide{position:absolute;left:0;top:17px;width:65px;height:3px;background:#bee0d8}.interval-tight{position:absolute;left:14px;top:14px;width:37px;height:9px;border-left:2px solid #0b9687;border-right:2px solid #0b9687}.interval-tight:after{content:'';position:absolute;left:0;right:0;top:3px;height:3px;background:#0b9687}.interval-icon>b{position:absolute;left:29px;top:14px;width:9px;height:9px;border-radius:50%;background:#17233e}
.why-rl-message{grid-column:1/-1;display:flex;align-items:center;gap:20px;background:#eef2ff;border-radius:10px;padding:14px 18px;border-left:3px solid #4263eb}.why-rl-message>span{font-size:12px;color:#4263eb;font-weight:800;white-space:nowrap}.why-rl-message>b{font-size:17px;font-weight:600;color:#17233e}
.rl-reveal{transition:opacity .45s ease}.rl-reveal.hidden{opacity:0;visibility:hidden;display:block!important}.why-rl-message.hidden{display:flex!important}
@media(prefers-reduced-motion:reduce){.rl-reveal{transition:none}}
</style>
