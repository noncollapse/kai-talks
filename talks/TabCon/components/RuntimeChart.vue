<script setup>
import { computed, ref } from 'vue'
const contexts=[64,128,256,512,1024], queries=[64,256,1024]
const context=ref(64), query=ref(64)
// Table 2: Linear, RFF, PI, Global, Bootstrap, AMP, TabCon; seconds.
const timings=[
[.0024,.0025,.2089,.1978,10.5411,.2579,.2036],
[.0024,.0025,.2108,.1990,10.6450,.2742,.2072],
[.0026,.0028,.2185,.2109,10.9722,.4773,.2297],
[.0025,.0028,.2103,.1986,10.5650,.2595,.2054],
[.0025,.0029,.2119,.1999,10.6264,.2758,.2082],
[.0026,.0033,.2214,.2139,11.0762,.4803,.2320],
[.0026,.0063,.2128,.2010,10.6597,.2619,.2072],
[.0026,.0065,.2137,.2017,10.7106,.2772,.2097],
[.0027,.0077,.2236,.2160,11.1982,.4821,.2340],
[.0028,.0108,.2176,.2060,10.9422,.2670,.2120],
[.0028,.0112,.2187,.2064,10.9773,.2825,.2146],
[.0029,.0123,.2265,.2192,11.3492,.4859,.2376],
[.0031,.0158,.2211,.2095,11.1274,.2702,.2155],
[.0032,.0159,.2243,.2129,11.3183,.2882,.2201],
[.0033,.0175,.2299,.2224,11.5502,.4890,.2403],
]
const values=computed(()=>timings[contexts.indexOf(context.value)*3+queries.indexOf(query.value)])
const ampSpeedupRange=computed(()=>{
  const ratios=timings.map(row=>row[5]/row[6])
  return `${Math.min(...ratios).toFixed(2)}–${Math.max(...ratios).toFixed(2)}`
})
const names=['Linear regression','RFF','TabPFN PI','Global','Bootstrap','AMP','TabCon']
const colors=['#ce7b26','#0b9687','#8292b0','#edaa63','#c2a16d','#a28cc5','#4263eb']
const rows=computed(()=>names.map((name,i)=>({name,color:colors[i],time:values.value[i]})))
const x=v=>175+(Math.log10(v)+3)*135
</script>
<template>
  <div class="runtime-selectors">
    <div role="group" aria-label="Training sample size"><b>C</b><button v-for="c in contexts" :key="c" :class="{selected:context===c}" :aria-pressed="context===c" @click.stop="context=c">{{c}}</button></div>
    <div role="group" aria-label="Number of queries"><b>Q</b><button v-for="q in queries" :key="q" :class="{selected:query===q}" :aria-pressed="query===q" @click.stop="query=q">{{q}}</button></div>
    <p class="runtime-definitions">C: training sample size · Q: number of queries</p>
  </div>
  <svg viewBox="0 18 875 262" style="display:block;width:100%;height:247px;margin-bottom:12px" role="img" :aria-label="`Median runtime for C=${context} and Q=${query}. Logarithmic time axis.`">
    <g v-for="v in [.001,.01,.1,1,10]" :key="v"><line :x1="x(v)" :x2="x(v)" y1="25" y2="247" stroke="#e1e7f1"/><text :x="x(v)" y="265" text-anchor="middle" fill="#8b97aa" style="font-size: 14px">{{v}} s</text></g>
    <g v-for="(r,i) in rows" :key="r.name" :transform="`translate(0,${35+i*32})`"><text x="10" y="6" :fill="r.color" style="font-size: 15px" font-weight="700">{{r.name}}</text><line x1="175" :x2="x(r.time)" y1="0" y2="0" :stroke="r.color" stroke-width="16" stroke-linecap="butt"/><text :x="x(r.time)+18" y="5" :fill="r.color" style="font-size: 17px" font-weight="700">{{r.time < .01 ? r.time.toFixed(4) : r.time.toFixed(2)}} s</text></g>
    <text x="750" y="265" text-anchor="start" fill="#8b97aa" style="font-size: 9px">Logarithmic time axis</text>
  </svg>
  <div class="callout">TabCon is <b>{{Math.round(values[4]/values[6])}}×</b> faster than Bootstrap and <b>{{ampSpeedupRange}}×</b> faster than AMP.</div>
</template>
<style scoped>
.runtime-selectors{display:flex;gap:28px;margin-top:5px}
.runtime-selectors>div{display:flex;align-items:center;gap:7px}
.runtime-selectors b{font-size:13px;color:#17233e;margin-right:3px}
.runtime-selectors button{font-size:12px;font-weight:600;padding:6px 12px;border:1px solid #dde4f0;border-radius:24px;color:#64748b;background:white}
.runtime-selectors button.selected{background:#17233e;color:white;border-color:#17233e}
.runtime-definitions{font-size:12px;color:#64748b;margin:10px 0 3px}
svg line{transition:x2 .4s ease}
.callout{padding:10px 18px}
</style>

<style scoped>
.runtime-selectors{align-items:center;gap:18px;margin-bottom:20px}
.runtime-selectors>div{gap:5px;flex-shrink:0}
.runtime-selectors button{padding:6px 9px}
.runtime-selectors .runtime-definitions{margin:0 0 0 auto;font-size:11px;line-height:1.4;white-space:nowrap}
</style>
