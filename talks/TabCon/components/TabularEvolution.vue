<script setup>
const rows = [
  { title:'Classical statistical methods', color:'#71839f', items:[
    { year:'1805', labels:['Linear regression'], url:'https://www.york.ac.uk/depts/maths/histstat/legendre.pdf' },
    { year:'1964', labels:['Smoothing splines'], url:'https://doi.org/10.1073/pnas.52.4.947' },
    { year:'1972', labels:['GLMs'], url:'https://doi.org/10.2307/2344614' },
    { year:'1979', labels:['Local polynomial regression'], url:'https://doi.org/10.1080/01621459.1979.10481038' },
  ]},
  { title:'Modern machine learning', color:'#9673bc', items:[
    { year:'1986', labels:['MLPs'], url:'https://doi.org/10.1038/323533a0' },
    { year:'1995', labels:['SVMs'], url:'https://research.google/pubs/support-vector-networks/' },
    { year:'2001', labels:['Random forests','Gradient boosting'], url:'https://doi.org/10.1214/aos/1013203450' },
  ]},
  { title:'Tabular foundation models', color:'#0b9687', items:[
    { year:'2021', labels:['PFNs'], url:'https://arxiv.org/abs/2112.10510' },
    { year:'2023', labels:['TabPFN'], url:'https://arxiv.org/abs/2207.01848' },
    { year:'2025', labels:['TabPFN v2 / 2.5','TabICL','LimiX / LimiX-2M'], url:'https://doi.org/10.1038/s41586-024-08328-6' },
    { year:'2026', labels:['TabPFN 2.6 / 3 / 3.5','TabICL v2','LimiX-2'], url:'https://github.com/PriorLabs/TabPFN/blob/main/CHANGELOG.md' },
  ]},
]
</script>

<template>
  <div class="history-rows">
    <section v-for="row in rows" :key="row.title" class="history-row" :style="{'--row-color': row.color}">
      <h3>{{ row.title }}</h3>
      <div class="history-track" :style="{'--milestones': row.items.length}">
        <a v-for="item in row.items" :key="item.year" :href="item.url" class="milestone">
          <span class="milestone-year">{{ item.year }}</span><i></i>
          <b v-for="label in item.labels" :key="label">{{ label }}</b>
        </a>
      </div>
    </section>
  </div>
</template>

<style scoped>
.history-rows{display:flex;flex-direction:column;gap:34px;margin-top:53px}
.history-row{display:grid;grid-template-columns:158px 1fr;gap:18px;align-items:start}
.history-row h3{font-size:19px;line-height:1.3;color:var(--row-color);font-weight:800;padding-top:12px;margin:0}
.history-track{display:grid;grid-template-columns:repeat(var(--milestones),minmax(0,1fr));position:relative;gap:12px}
.history-track::before{content:'';position:absolute;left:5px;right:0;top:24px;height:2px;background:var(--row-color);opacity:.35}
.history-track::after{content:'';position:absolute;right:0;top:20px;border-left:7px solid var(--row-color);border-top:5px solid transparent;border-bottom:5px solid transparent;opacity:.5}
.milestone{position:relative;display:flex;flex-direction:column;border:0!important;text-decoration:none!important;color:#17233e;min-height:68px}
.milestone-year{font-size:13px;line-height:17px;color:var(--row-color);font-weight:800}
.milestone i{display:block;width:10px;height:10px;border-radius:50%;background:var(--row-color);border:2px solid #fbfcff;box-sizing:content-box;margin:1px 0 9px;z-index:1}
.milestone b{font-size:14px;line-height:1.4;font-weight:700;color:#17233e}
.milestone b + b{margin-top:5px}
</style>
