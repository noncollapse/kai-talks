<script setup>
const rows=[{name:'TabPFN PI',time:.2137,color:'#8292b0'},{name:'AMP',time:.2772,color:'#a28cc5'},{name:'Bootstrap',time:10.7106,color:'#c2a16d'},{name:'TabCon',time:.2097,color:'#4263eb'}]
const x=v=>160+(Math.log10(v)+1)*265
</script>
<template>
  <svg viewBox="0 0 875 295" style="width:100%;height:280px" role="img" aria-label="Median runtime: TabPFN PI 0.2137 seconds, AMP 0.2772, Bootstrap 10.7106, TabCon 0.2097. Logarithmic time axis.">
    <g v-for="v in [.1,1,10]" :key="v"><line :x1="x(v)" :x2="x(v)" y1="25" y2="245" stroke="#e1e7f1"/><text :x="x(v)" y="266" text-anchor="middle" fill="#8b97aa" style="font-size: 12px">{{v}} s</text></g>
    <g v-for="(r,i) in rows" :key="r.name" :transform="`translate(0,${53+i*53})`"><text x="10" y="6" :fill="r.color" style="font-size: 17px" font-weight="700">{{r.name}}</text><line x1="160" :x2="x(r.time)" y1="0" y2="0" :stroke="r.color" stroke-width="12" stroke-linecap="round"/><circle :cx="x(r.time)" cy="0" r="8" :fill="r.color"/><text :x="x(r.time)+18" y="5" :fill="r.color" style="font-size: 15px" font-weight="700">{{r.time.toFixed(2)}} s</text></g>
    <text x="825" y="287" text-anchor="end" fill="#8b97aa" style="font-size: 11px">Logarithmic time axis</text>
  </svg>
</template>
