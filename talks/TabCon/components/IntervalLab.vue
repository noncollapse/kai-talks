<script setup>
import { computed, ref, watch } from 'vue'
import { useSlideContext } from '@slidev/client'
const props=defineProps({mode:{default:'compare'}})
const {$clicks}=useSlideContext()
const override=ref(null)
watch($clicks,()=>{override.value=null})
const n=computed(()=>props.mode==='grow'?(override.value??[20,80,320][Math.min($clicks.value,2)]):40)
function rng(seed){return()=>{seed=(1664525*seed+1013904223)>>>0;return(seed+.5)/4294967296}}
const points=computed(()=>{const random=rng(4581);return Array.from({length:n.value},()=>{const a=45+110*random();const z=Math.sqrt(-2*Math.log(random()))*Math.cos(2*Math.PI*random());return{x:a,y:180+3*a+65*z}})})
const fit=computed(()=>{const data=points.value,xb=data.reduce((a,p)=>a+p.x,0)/n.value,yb=data.reduce((a,p)=>a+p.y,0)/n.value,sxx=data.reduce((a,p)=>a+(p.x-xb)**2,0),b=data.reduce((a,p)=>a+(p.x-xb)*(p.y-yb),0)/sxx;return{a:yb-b*xb,b,xb,sxx}})
const sx = x => 52 + (x - 40) / 120 * 560
function sy(value) {
  const proportion = (value - 150) / 650
  const distance = proportion * 245
  return 272 - distance
}
const prediction=x=>fit.value.a+fit.value.b*x
const half=(x,pi)=>1.96*65*Math.sqrt((pi?1:0)+1/n.value+(x-fit.value.xb)**2/fit.value.sxx)
const xs=Array.from({length:61},(_,i)=>40+i*2)
const band=pi=>xs.map((x,i)=>`${i?'L':'M'}${sx(x)},${sy(prediction(x)+half(x,pi))}`).join(' ')+[...xs].reverse().map(x=>` L${sx(x)},${sy(prediction(x)-half(x,pi))}`).join(' ')+' Z'
const line=computed(()=>xs.map((x,i)=>`${i?'L':'M'}${sx(x)},${sy(prediction(x))}`).join(' '))
const showLine=computed(()=>props.mode==='grow'||$clicks.value>=1)
const showPI=computed(()=>props.mode==='grow'||$clicks.value>=2)
const showCI=computed(()=>props.mode==='grow'||$clicks.value>=3)
</script>
<template>
  <div class="lab">
    <svg viewBox="0 0 650 315" role="img" :aria-label="`Simulated house prices with ${n} observations, a prediction band and a confidence band for the mean.`">
      <g v-for="v in [200,400,600,800]" :key="v"><line x1="52" x2="612" :y1="sy(v)" :y2="sy(v)" stroke="#e7ecf4"/><text x="42" :y="sy(v)+4" text-anchor="end" fill="#8b97aa" style="font-size: 11px">{{v}}</text></g>
      <!-- Inline CSS avoids UnoCSS interpreting SVG opacity="1" as 1%. -->
      <path :d="band(true)" fill="#4263eb19" stroke="#4263eb55" stroke-width="1" :style="{opacity:showPI?1:0}" class="band"/>
      <g><circle v-for="(p,i) in points" :key="i" :cx="sx(p.x)" :cy="sy(p.y)" :r="n>100?2:3.5" :fill="showPI?'#aab7cf':'#91a6d4'" :style="{opacity:n>100?.45:.75}"/></g>
      <path :d="band(false)" fill="#0b96874a" stroke="#0b9687" stroke-width="1" :style="{opacity:showCI?1:0}" class="band"/>
      <path :d="line" fill="none" stroke="#17233e" stroke-width="2.5" :style="{opacity:showLine?1:0}" class="band"/>
      <line :x1="sx(100)" :x2="sx(100)" y1="22" y2="276" stroke="#7c4dce66" stroke-dasharray="4 5"/>
      <text :x="sx(100)" y="15" text-anchor="middle" fill="#7c4dce" style="font-size: 11px">100 m²</text>
      <line x1="52" x2="612" y1="276" y2="276" stroke="#bac5d6"/>
      <g v-for="v in [40,80,120,160]" :key="v"><text :x="sx(v)" y="295" text-anchor="middle" fill="#8b97aa" style="font-size: 11px">{{v}}</text></g>
      <text x="610" y="312" text-anchor="end" fill="#64748b" style="font-size: 11px">Floor area (m²)</text><text x="52" y="15" fill="#64748b" style="font-size: 11px">Price (£k)</text>
    </svg>
    <aside>
      <div class="sample"><b>{{n}}</b> observations</div>
      <div class="metric" :class="{muted:!showPI}"><span class="dot pi"/> Future sale <strong>£{{Math.round(prediction(100)-half(100,true))}}k–£{{Math.round(prediction(100)+half(100,true))}}k</strong><small>Prediction interval</small></div>
      <div class="metric" :class="{muted:!showCI}"><span class="dot ci"/> Average price <strong>£{{Math.round(prediction(100)-half(100,false))}}k–£{{Math.round(prediction(100)+half(100,false))}}k</strong><small>Confidence interval</small></div>
      <div v-if="mode==='grow'" class="controls"><button v-for="v in [20,80,320]" :key="v" @click.stop="override=v" :class="{selected:n===v}" :aria-label="`Show ${v} observations`">{{v}}</button></div>
    </aside>
  </div>
  <div class="lab-caption">{{mode==='grow'?'More data can pin down the average. Individual outcomes can still vary.':'The two intervals describe different targets at the same floor area.'}}</div>
</template>
<style scoped>
.lab{display:grid;grid-template-columns:650px 1fr;gap:10px;align-items:center;margin-left:-20px}.lab svg{width:650px;height:315px}.band{transition:d .7s ease,opacity .6s ease}.sample{font-size:13px;color:#64748b;margin-bottom:18px}.sample b{font-size:28px;font-family:Manrope;color:#17233e;display:block}.metric{font-size:14px;margin:18px 0;transition:opacity .6s}.metric.muted{opacity:.12}.metric strong{font-size:21px;display:block;margin:5px 0;font-variant-numeric:tabular-nums}.metric small{font-size:11px;color:#64748b}.dot{width:8px;height:8px;display:inline-block;border-radius:50%;margin-right:5px}.pi{background:#4263eb}.ci{background:#0b9687}.controls{display:flex;gap:5px}.controls button{font-size:12px;border:1px solid #d6deed;border-radius:7px;padding:5px 9px;color:#64748b;background:white}.controls button.selected{background:#4263eb;color:white;border-color:#4263eb}.lab-caption{font-size:18px;padding:14px 18px;border-left:3px solid #0b9687;background:#e9f8f4;margin-top:5px;border-radius:0 10px 10px 0}
</style>
