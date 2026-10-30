<script setup>
import { computed, ref, watch } from 'vue'
import { useSlideContext } from '@slidev/client'
const { $clicks } = useSlideContext()
const selected=ref(0)
watch(() => $clicks.value, clicks => { selected.value=Math.min(clicks,3) }, {immediate:true})
const settings=['In-distribution','Out-of-distribution','Stress-test','CC18']
// Table 1, arXiv:2609.33114 (95% nominal coverage).
const methods=[
 {name:'Linear regression',color:'#ce7b26',cp:[.8653,.6814,.7673,.5377],length:[8.5699,2.5411,6.9267,78.0342]},
 {name:'RFF',color:'#0b9687',cp:[.8511,.8029,.7381,.6238],length:[4.0549,2.5039,2.6404,.7514]},
 {name:'TabPFN PI',color:'#8292b0',cp:[.9792,.9695,.9902,.9953],length:[4.0261,2.1793,3.2091,2.6531]},
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
    <text x="155" y="22" style="font-size: 13px" fill="#64748b">Coverage probability of the regression mean</text><text x="540" y="22" style="font-size: 13px" fill="#64748b">Average interval length</text>
    <line :x1="xcp(.95)" :x2="xcp(.95)" y1="37" y2="228" stroke="#17233e" stroke-dasharray="4 5"/><text :x="xcp(.95)" y="259" style="font-size: 11px" text-anchor="middle" fill="#17233e">95% target</text>
    <g v-for="(m,i) in methods" :key="m.name" :transform="`translate(0,${61+i*30})`">
      <text x="6" y="5" :fill="m.name==='TabCon'?'#4263eb':'#53637d'" style="font-size: 13px" :font-weight="m.name==='TabCon'?800:500">{{m.name}}</text>
      <line x1="155" x2="430" y1="0" y2="0" stroke="#e3e8f2"/><circle :cx="xcp(m.cp[selected])" cy="0" r="6" :fill="m.color" class="moving"/>
      <text x="448" y="5" :fill="m.color" style="font-size: 14px" font-weight="700">{{(m.cp[selected]*100).toFixed(2)}}%</text>
      <rect x="540" y="-10" :width="width(m.length[selected])" height="20" rx="4" :fill="m.color" opacity=".75" class="moving"/>
      <text :x="548+width(m.length[selected])" y="5" :fill="m.color" style="font-size: 13px" font-weight="700">{{m.length[selected].toFixed(2)}}</text>
    </g>
    <text x="155" y="239" fill="#99a4b7" style="font-size: 10px">50%</text><text x="430" y="239" fill="#99a4b7" style="font-size: 10px" text-anchor="end">100%</text>
  </svg>
  <div class="detail-message">TabCon: <b>coverage closest to 95%</b> and <b>shortest intervals</b> among methods with sufficient coverage.</div>
</template>
<style scoped>
.settings{display:flex;gap:8px;margin:4px 0 8px}.settings button{font-size:12px;font-weight:600;padding:9px 16px;border:1px solid #dde4f0;border-radius:24px;color:#64748b;background:white}.settings button.selected{background:#17233e;color:white;border-color:#17233e}.bench{width:100%;height:260px}.moving{transition:cx .55s,width .55s}.result-note{font-size:17px;background:#eef2ff;padding:13px 18px;border-radius:10px;color:#4263eb}.foot{font-size:10px!important;color:#7d8ba1;margin-top:10px!important;line-height:1.45!important}
</style>

<style scoped>
.bench{height:300px}
.detail-message{margin-top:8px}
</style>
