<script setup>
import { computed, ref } from 'vue'
const selected=ref(0)
const settings=['Standard ID','Standard OOD','Stress-test','CC18']
const methods=[
 {name:'TabPFN PI*',color:'#8292b0',cp:[.9792,.9695,.9902,.9953],length:[4.0261,2.1793,3.2091,2.6531]},
 {name:'Bootstrap',color:'#c2a16d',cp:[.5935,.6820,.6970,.7328],length:[.9200,.8107,.6651,.4084]},
 {name:'AMP',color:'#a28cc5',cp:[.9369,.9351,.9729,.9818],length:[3.9612,2.0706,3.2663,2.4117]},
 {name:'TabCon',color:'#4263eb',cp:[.9548,.9531,.9561,.9654],length:[2.6824,1.9288,1.8581,1.0686]},
]
const xcp=v=>155+(v-.5)/.5*275
const maxLength=computed(()=>Math.max(...methods.map(m=>m.length[selected.value]))*1.12)
const width=v=>v/maxLength.value*265
</script>
<template>
  <div class="settings" role="group" aria-label="Benchmark setting"><button v-for="(name,i) in settings" :key="name" @click.stop="selected=i" :class="{selected:selected===i}" :aria-pressed="selected===i">{{name}}</button></div>
  <svg viewBox="0 0 875 274" class="bench" role="img" :aria-label="`Coverage and interval length for ${settings[selected]}, from Table 1 of the TabCon paper.`">
    <text x="155" y="22" style="font-size: 13px" fill="#64748b">Coverage of the regression mean</text><text x="540" y="22" style="font-size: 13px" fill="#64748b">Average interval length</text>
    <line :x1="xcp(.95)" :x2="xcp(.95)" y1="37" y2="228" stroke="#17233e" stroke-dasharray="4 5"/><text :x="xcp(.95)" y="259" style="font-size: 11px" text-anchor="middle" fill="#17233e">95% target</text>
    <g v-for="(m,i) in methods" :key="m.name" :transform="`translate(0,${61+i*48})`">
      <text x="6" y="5" :fill="m.name==='TabCon'?'#4263eb':'#53637d'" style="font-size: 15px" :font-weight="m.name==='TabCon'?800:500">{{m.name}}</text>
      <line x1="155" x2="430" y1="0" y2="0" stroke="#e3e8f2"/><circle :cx="xcp(m.cp[selected])" cy="0" r="6" :fill="m.color" class="moving"/>
      <text x="448" y="5" :fill="m.color" style="font-size: 14px" font-weight="700">{{(m.cp[selected]*100).toFixed(2)}}%</text>
      <rect x="540" y="-10" :width="width(m.length[selected])" height="20" rx="4" :fill="m.color" opacity=".75" class="moving"/>
      <text :x="548+width(m.length[selected])" y="5" :fill="m.color" style="font-size: 13px" font-weight="700">{{m.length[selected].toFixed(2)}}</text>
    </g>
    <text x="155" y="239" fill="#99a4b7" style="font-size: 10px">50%</text><text x="430" y="239" fill="#99a4b7" style="font-size: 10px" text-anchor="end">100%</text>
  </svg>
  <div class="result-note"><b>Coverage first. Then width.</b> A short interval is useful only if it covers reliably.</div>
  <p class="foot">*PI was designed for future outcomes. This comparison scores it against the regression mean. Selected baselines; averages over datasets and query points.</p>
</template>
<style scoped>
.settings{display:flex;gap:8px;margin:4px 0 8px}.settings button{font-size:12px;font-weight:600;padding:9px 16px;border:1px solid #dde4f0;border-radius:24px;color:#64748b;background:white}.settings button.selected{background:#17233e;color:white;border-color:#17233e}.bench{width:100%;height:260px}.moving{transition:cx .55s,width .55s}.result-note{font-size:17px;background:#eef2ff;padding:13px 18px;border-radius:10px;color:#4263eb}.foot{font-size:10px!important;color:#7d8ba1;margin-top:10px!important;line-height:1.45!important}
</style>
