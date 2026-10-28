<script setup>
const categories = [
  { title:'More predictive models', color:'#4263eb', papers:[
    { name:'TabICL / TabICL v2', citation:'Qu et al., 2025 / 2026', url:'https://github.com/soda-inria/tabicl' },
    { name:'LimiX / LimiX-2', citation:'Zhang et al., 2025 / 2026', url:'https://github.com/limix-ldm-ai/LimiX' },
    { name:'SOMTab', citation:'Wang, Zhang & Ma, 2026', url:'https://arxiv.org/abs/2608.27882' },
    { name:'TabFM', citation:'Google Research, 2026', url:'https://research.google/blog/introducing-tabfm-a-zero-shot-foundation-model-for-tabular-data/' },
    { name:'Kumo Tabular', citation:'NVIDIA, 2026', url:'https://build.nvidia.com/nvidia/kumo-tabular/modelcard' },
  ]},
  { title:'Causal effect estimation', color:'#0b9687', papers:[
    { name:'Do-PFN', citation:'Robertson et al., NeurIPS 2025', url:'https://arxiv.org/abs/2506.06039' },
    { name:'CausalPFN', citation:'Balazadeh et al., 2025', url:'https://arxiv.org/abs/2506.07918' },
    { name:'CausalFM', citation:'Ma et al., ICLR 2026', url:'https://proceedings.iclr.cc/paper_files/paper/2026/hash/7f8cabaf2de70e1a9d3eb187f02bd58c-Abstract-Conference.html' },
    { name:'Learning to Fluctuate', citation:'Zhang, 2026', url:'https://arxiv.org/abs/2609.26290' },
  ]},
  { title:'Uncertainty quantification', color:'#7c4dce', papers:[
    { name:'Approximate martingale posteriors (AMP)', citation:'Nagler & Rügamer, 2026', url:'https://arxiv.org/abs/2505.11325' },
    { name:'TabMGP', citation:'Ng et al., ICML 2026', url:'https://proceedings.mlr.press/v306/ng26a.html' },
    { name:'Uncertainty decomposition', citation:'Fortini et al., 2026', url:'https://arxiv.org/abs/2602.04596' },
    { name:'Conformal PFNs with missing data', citation:'van Leeuwen, EurIPS workshop 2025', url:'https://sites.google.com/view/eurips25-ai-td' },
  ]},
]
</script>

<template>
  <div class="pfn-ecosystem">
    <section v-for="(category,index) in categories" :key="category.title" class="ecosystem-card" :style="{'--accent':category.color}">
      <div class="ecosystem-number">{{ index + 1 }}</div>
      <h3>{{ category.title }}</h3>
      <a v-for="paper in category.papers" :key="paper.name" :href="paper.url"><b>{{ paper.name }}</b><small>{{ paper.citation }}</small></a>
    </section>
  </div>
</template>

<style scoped>
.pfn-ecosystem{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin-top:22px}
.ecosystem-card{background:#fff;border:1px solid #dfe5f1;border-top:3px solid var(--accent);border-radius:0 0 14px 14px;padding:16px 17px 20px}
.ecosystem-number{font-size:12px;font-weight:800;color:var(--accent);letter-spacing:.05em}
.ecosystem-card h3{font-size:19px;line-height:1.3;font-weight:800;margin:8px 0 20px;color:#17233e;min-height:49px}
.ecosystem-card a{display:block;border:0!important;text-decoration:none!important;margin-top:16px}
.ecosystem-card a b{display:block;color:#17233e;font-size:15px;font-weight:700;line-height:1.3}
.ecosystem-card a small{display:block;font-size:10px;color:#8490a4;line-height:1.4;margin-top:4px}
</style>
