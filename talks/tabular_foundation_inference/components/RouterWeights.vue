<script setup>
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'
import MathTex from './MathTex.vue'
const { $clicks } = useSlideContext()
const normalize = values => { const sum = values.reduce((a,b)=>a+b,0); return values.map(v=>v/sum) }
const gaussian = (mean, width) => normalize(Array.from({length:15},(_,i)=>Math.exp(-.5*((i-7-mean)/width)**2)))
const heads = [
  {name:'Global',key:'G',color:'#4263eb',weight:.35,p:gaussian(-.3,2.4)},
  {name:'Expansion',key:'E',color:'#7c4dce',weight:.65,p:gaussian(.5,4.2)},
  {name:'Shrinkage',key:'S',color:'#0b9687',weight:0,p:gaussian(0,1.5)},
]
const mixture = heads[0].p.map((p,i)=>.35*p+.65*heads[1].p[i])
const quantilePosition = probability => {
  let mass=0
  for (let i=0;i<mixture.length;i++) { if (mass+mixture[i]>=probability) return 15+20*(i+(probability-mass)/mixture[i]); mass+=mixture[i] }
  return 315
}
const quantiles=[quantilePosition(.025),quantilePosition(.975)]
const selected = computed(()=>$clicks.value>=1)
</script>

<template>
  <div class="blend-map">
    <svg class="blend-links" viewBox="0 0 876 360" aria-hidden="true">
      <defs><marker id="blend-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7" fill="#acb7cb" /></marker></defs>
      <g class="reveal" :class="{waiting:$clicks<1}" fill="none" stroke="#acb7cb" stroke-width="1.6" marker-end="url(#blend-arrow)">
        <path d="M204 77H263" /><path d="M204 165H263" /><path d="M204 253H263" />
        <path d="M401 165H460" />
      </g>
      <path class="reveal" :class="{waiting:$clicks<2}" d="M669 268V282" fill="none" stroke="#0b9687" stroke-width="1.7" marker-end="url(#blend-arrow)" />
    </svg>
    <span class="blend-section-label">Residual distributions</span>
    <section v-for="(head,i) in heads" :key="head.key" class="distribution-card" :class="{muted:selected&&i===2}" :style="{top:`${38+i*88}px`,'--expert':head.color}">
      <div><h3>{{head.name}}</h3><MathTex :tex="`p_${head.key}(r)`" /></div>
      <div class="mini-density" aria-hidden="true"><i v-for="(p,j) in head.p" :key="j" :style="{height:`${p*180}px`}" /></div>
    </section>
    <span class="gate-section-label reveal" :class="{waiting:$clicks<1}">Top-2 gate</span>
    <section class="top2-card reveal" :class="{waiting:$clicks<1}"><div v-for="(head,i) in heads" :key="head.key" class="selection-row" :class="{off:i===2}" :style="{top:`${i*88}px`,'--expert':head.color}"><span class="selection-check">{{i===2?'×':'✓'}}</span><b>{{head.weight.toFixed(2)}}</b><small>{{head.name}}</small></div></section>
    <p class="gate-caption reveal" :class="{waiting:$clicks<1}">Keep two. Renormalize.</p>
    <section class="blended-density reveal" :class="{waiting:$clicks<1}"><span class="small-label">Mix probabilities in each residual bin</span><h3>One residual distribution</h3>
      <svg class="density-chart" viewBox="0 0 330 160" aria-label="Illustrative mixture of the Global and Expansion residual distributions">
        <line x1="15" y1="130" x2="315" y2="130" stroke="#b8c5d9" />
        <g v-for="(p,i) in mixture" :key="i">
          <rect :x="15+i*20" :y="130-heads[0].p[i]*.35*880" width="14" :height="heads[0].p[i]*.35*880" fill="#4263eb" rx="2" />
          <rect :x="15+i*20" :y="130-p*880" width="14" :height="heads[1].p[i]*.65*880" fill="#a37ce0" rx="2" />
        </g>
        <g class="reveal" :class="{waiting:$clicks<2}"><line v-for="(x,i) in quantiles" :key="i" :x1="x" :x2="x" y1="12" y2="137" stroke="#0b9687" stroke-width="1.5" stroke-dasharray="4 4" /><text :x="quantiles[0]" y="153" text-anchor="middle" style="font-size:10px;fill:#0b9687">2.5%</text><text :x="quantiles[1]" y="153" text-anchor="middle" style="font-size:10px;fill:#0b9687">97.5%</text></g>
      </svg>
      <div class="blend-legend"><span><i style="background:#4263eb"/>0.35 Global</span><span><i style="background:#a37ce0"/>0.65 Expansion</span></div>
    </section>
    <section class="blend-ci reveal" :class="{waiting:$clicks<2}"><div><b>Read the mixture quantiles</b><span>Combine them with the fixed <MathTex tex="\widehat f(x)" /></span></div><div class="ci-picture"><i/><b/><span>Confidence interval</span></div></section>
    <div class="blend-caption">The router mixes distributions. The interval is constructed from that mixture.</div>
  </div>
</template>

<style scoped>
.blend-map{position:relative;width:876px;height:385px;margin-top:16px}
.blend-links{position:absolute;left:0;top:0;width:876px;height:360px;pointer-events:none}
.blend-map section{position:absolute;box-sizing:border-box;border:1px solid #dce4f2;background:white;border-radius:13px}
.blend-map h3{font-size:20px;font-weight:800;line-height:1.3;margin:0}.small-label{font-size:10px;color:#7b89a2}
.blend-section-label{position:absolute;top:6px;left:0;font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#8190aa}
.distribution-card{left:0;width:204px;height:78px;border-left:3px solid var(--expert)!important;display:flex;align-items:center;justify-content:space-between;padding:12px;transition:opacity .45s}
.distribution-card h3{font-size:16px;color:var(--expert);margin-bottom:8px}.distribution-card .math-tex-inline{font-size:15px;color:var(--expert)}
.mini-density{display:flex;align-items:flex-end;gap:2px;height:49px}.mini-density i{display:block;width:4px;border-radius:2px 2px 0 0;background:var(--expert);opacity:.6}
.distribution-card.muted{opacity:.25}
.gate-section-label{position:absolute;top:6px;left:267px;width:134px;text-align:center;font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#7c4dce}
.top2-card{left:267px;top:38px;width:134px;height:256px;text-align:center;background:#f8f4fd!important;border-color:#dacbef!important}
.selection-row{position:absolute;left:12px;right:12px;height:78px;color:var(--expert);display:flex;flex-direction:column;justify-content:center}.selection-row>b{font-size:23px;line-height:1.3}.selection-row small{display:block;font-size:10px;line-height:1.3;margin-top:5px}.selection-check{font-size:14px;position:absolute;left:2px;top:26px}.selection-row.off{opacity:.35}
.gate-caption{position:absolute;left:267px;top:301px;width:134px;margin:0;text-align:center;font-size:10px;color:#8c7a9f}
.blended-density{left:464px;top:12px;width:412px;height:256px;text-align:center;padding:16px;background:#f6f7fd!important}.blended-density h3{margin-top:7px;font-size:21px}.density-chart{display:block;width:330px;height:148px;margin:0 auto}.blend-legend{display:flex;justify-content:center;gap:25px;font-size:10px;color:#77849b}.blend-legend span{display:flex;align-items:center;gap:6px}.blend-legend i{width:8px;height:8px;border-radius:2px}
.blend-ci{left:464px;top:286px;width:412px;height:70px;padding:13px 15px;display:flex;justify-content:space-between;align-items:center;background:#edf9f5!important;border-color:#c8e5dd!important}.blend-ci>div:first-child{width:230px}.blend-ci b{font-size:13px;color:#0b9687}.blend-ci>div:first-child>span{display:block;font-size:10px;color:#709386;margin-top:7px}.ci-picture{position:relative;width:130px;height:40px;text-align:center}.ci-picture i{position:absolute;left:8px;right:8px;height:3px;top:9px;background:#0b9687}.ci-picture b{position:absolute;left:60px;top:5px;width:10px;height:10px;border-radius:50%;background:#17233e}.ci-picture span{display:block;padding-top:18px;font-size:9px;color:#709386;margin-top:7px}
.blend-caption{position:absolute;left:0;top:363px;width:876px;text-align:center;font-size:12px;color:#7e8ba2}
</style>
