<script setup>
import { useSlideContext } from '@slidev/client'
const { $clicks } = useSlideContext()
</script>
<template>
  <div class="training-overview">
    <div class="training-cards">
      <section class="global-stage"><span>1</span><h3>Global</h3><p>Learn <strong>residual distribution</strong> across <strong>all</strong> datasets.</p><small>50,000 synthetic datasets</small></section>
      <section class="specialist-stage reveal" :class="{waiting:$clicks<1}"><span>2</span><h3>Specialists</h3><p>Clone Global &amp; specialize on data subsets with <strong>undercoverage</strong> or <strong>overcoverage</strong>.</p><small>Global data subsets</small></section>
      <section class="router-stage reveal" :class="{waiting:$clicks<2}"><span>3</span><h3>Router</h3><p><strong>Supervised fine-tuning</strong> (SFT) to learn <strong>routing weights</strong>.</p><small>50,000 additional datasets</small></section>
      <section class="router-stage reveal" :class="{waiting:$clicks<3}"><span>4</span><h3>Router</h3><p><strong>Reinforcement learning</strong> (RL) to fine-tune <strong>routing weights</strong>.</p><small>100,000 additional datasets</small></section>
    </div>
    <div class="phase-labels">
      <b class="pretraining-label">Pre-training</b>
      <b class="posttraining-label">Post-training</b>
    </div>
  </div>
</template>
<style scoped>
.training-overview{position:relative;margin-top:30px;padding-bottom:0}
.training-cards{position:relative;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;z-index:1}
.training-cards section{position:relative;box-sizing:border-box;min-height:248px;padding:17px 15px 19px;background:white;border:1px solid #e1e6ef;border-top:3px solid var(--stage-color);border-radius:0 0 10px 10px}
.global-stage{--stage-color:#ce7b26}.specialist-stage{--stage-color:#7c4dce}.router-stage{--stage-color:#cf649a}
.training-cards .specialist-stage{border-top:0;padding-top:20px}.specialist-stage::before{content:'';position:absolute;left:-1px;right:-1px;top:0;height:3px;background:linear-gradient(90deg,#7c4dce 50%,#0b9687 50%)}
.training-cards section>span{font-family:Manrope,sans-serif;font-size:29px;line-height:1;font-weight:800;color:var(--stage-color)}
.training-cards h3{font-family:Manrope,sans-serif;font-size:22px;font-weight:800;color:#17233e;margin:15px 0 13px}
.training-cards p{font-size:15px;line-height:1.5;color:#64748b;margin:0;min-height:104px}.training-cards strong{font-weight:800;color:#17233e}
.training-cards small{display:block;font-size:10px;line-height:1.4;color:#8490a4;margin-top:12px}
.phase-labels{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:18px;text-align:center;font-family:Manrope,sans-serif;font-size:17px;font-weight:800}
.pretraining-label{color:#4263eb}.posttraining-label{color:#c44747}
</style>
