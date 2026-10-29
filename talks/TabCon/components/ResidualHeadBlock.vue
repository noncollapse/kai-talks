<script setup>
defineProps({ residual:Boolean })
</script>
<template>
  <div class="branch-head" :class="{red:residual}">
    <h3>{{ residual ? 'Residual head' : 'Regression head' }}</h3>
    <div class="branch-badge"><span aria-hidden="true">{{ residual ? '🔥' : '❄' }}</span> {{ residual ? 'Trainable' : 'Frozen' }}</div>
    <div class="branch-stack"><i></i><i></i><div>
      <svg viewBox="0 0 110 76" aria-hidden="true"><g stroke="currentColor" stroke-width="2" stroke-opacity=".45" fill="none"><path d="M15 13L55 21L95 13M15 13L55 55L95 13M15 63L55 21L95 63M15 63L55 55L95 63"/></g><g fill="currentColor"><circle cx="15" cy="13" r="5"/><circle cx="15" cy="63" r="5"/><circle cx="55" cy="21" r="5"/><circle cx="55" cy="55" r="5"/><circle cx="95" cy="13" r="5"/><circle cx="95" cy="63" r="5"/></g></svg>
    </div></div>
  </div>
</template>
<style scoped>
.branch-head{--ink:#4263eb;--border:#a4b6ee;--fill:#eef2ff;text-align:center;width:150px}.branch-head.red{--ink:#cf4b53;--border:#e7acb0;--fill:#fff0f1}
.branch-head h3{font-size:17px;font-weight:800;line-height:1.3;color:#17233e;margin:0 0 6px}
.branch-badge{font-size:11px;font-weight:700;color:var(--ink);margin-bottom:9px;line-height:20px}.branch-badge span{font-size:18px}
.branch-stack{position:relative;width:138px;height:88px;margin:auto;color:var(--ink)}
.branch-stack>i,.branch-stack>div{position:absolute;width:122px;height:72px;border:1.5px solid var(--border);border-radius:11px;background:var(--fill);box-sizing:border-box}
.branch-stack>i:first-child{left:16px;top:0}.branch-stack>i:nth-child(2){left:8px;top:8px}
.branch-stack>div{left:0;top:16px;background:white;display:flex;align-items:center;justify-content:center}.branch-stack svg{width:87px;height:60px}
.red .branch-stack{animation:branchTrain 3s ease-in-out infinite}@keyframes branchTrain{50%{filter:drop-shadow(0 0 6px #cf4b5330)}}
@media(prefers-reduced-motion:reduce){.red .branch-stack{animation:none}}
</style>
