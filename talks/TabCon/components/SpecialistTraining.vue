<script setup>
import { ref, watch } from 'vue'
import { useSlideContext } from '@slidev/client'
import MathTex from './MathTex.vue'
const { $clicks } = useSlideContext()
const regime = ref('under')
watch(() => $clicks.value, clicks => {
  regime.value = clicks >= 2 ? 'middle' : clicks >= 1 ? 'over' : 'under'
}, { immediate: true })
const modes = [
  {id:'under',name:'Low score',rule:String.raw`S\le s_1`,color:'#7c4dce'},
  {id:'middle',name:'Middle score',rule:String.raw`s_1<S<s_2`,color:'#64748b'},
  {id:'over',name:'High score',rule:String.raw`S\ge s_2`,color:'#0b9687'},
]
</script>

<template>
  <div class="specialist-controls" role="group" aria-label="Training task regime"><button v-for="mode in modes" :key="mode.id" :aria-label="mode.name" :aria-pressed="regime===mode.id" :style="{'--regime-color':mode.color}" @click.stop="regime=mode.id"><span class="regime-name">{{mode.name}}</span><MathTex :tex="mode.rule" /></button></div>
  <div class="specialist-graph">
    <div class="task-tile">
      <h3>3 Loss Components</h3>
      <ol>
        <li><strong>NLL</strong></li>
        <li><strong>CRPS</strong></li>
        <li><strong>KL</strong><p>Penalizes divergence between the specialist’s and Global’s residual distributions.</p></li>
      </ol>
    </div>
    <div class="branch-symbol">→</div>
    <div class="specialist-updates">
      <div v-for="head in [{name:'Expansion',active:'under',color:'#7c4dce'},{name:'Shrinkage',active:'over',color:'#0b9687'}]" :key="head.name" class="specialist-update" :style="{'--specialist':head.color}">
        <h3>{{head.name}}</h3><div class="loss-chips"><span :class="{enabled:regime===head.active}">NLL</span><span :class="{enabled:regime===head.active}">CRPS</span><span class="enabled">KL</span></div>
        <p>{{regime===head.active?"Fit this task's error distribution.":'Use KL to stay close to Global.'}}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.specialist-controls{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:14px 0 16px}
.specialist-controls button{display:flex;align-items:center;justify-content:space-between;gap:12px;border:1px solid #dce3ef;border-top-width:3px;border-radius:10px;padding:14px 16px;color:#64748b;background:#fff;font-size:21px;transition:background .2s,border-color .2s}
.specialist-controls .regime-name{font-size:15px;font-weight:600;white-space:nowrap}
.specialist-controls button[aria-pressed=true]{background:color-mix(in srgb,var(--regime-color) 6%,white);border-color:var(--regime-color);color:var(--regime-color)}
.specialist-graph{display:grid;grid-template-columns:296px 42px 1fr;align-items:stretch}
.task-tile{border-top:2px solid #cad4e5;padding:18px 20px 12px 0}
.task-tile h3{font-size:20px;margin:0 0 18px;line-height:1.3}
.task-tile ol{padding-left:23px;margin:0;font-size:17px;color:#17233e}
.task-tile li+li{margin-top:13px}
.task-tile li strong{font-weight:600}
.task-tile li p{font-size:15px;line-height:1.5;margin:8px 0 0;color:#64748b}
.branch-symbol{display:flex;align-items:center;justify-content:center;font-size:28px;color:#acb8ca}
.specialist-updates{display:grid;gap:16px}
.specialist-update{border:1px solid #dfe5ef;border-left:3px solid var(--specialist);border-radius:10px;padding:14px 21px;background:#fff}
.specialist-update h3{font-size:22px;color:var(--specialist);margin:0 0 12px;line-height:1.25}
.loss-chips{display:flex;gap:10px}.loss-chips span{padding:5px 11px;font-size:14px;background:#f1f3f7;color:#a3adbf;border-radius:5px;opacity:.45}
.loss-chips .enabled{opacity:1;background:color-mix(in srgb,var(--specialist) 9%,white);color:var(--specialist);font-weight:600}
.specialist-update p{font-size:14px;line-height:1.5;color:#64748b;margin:10px 0 0}
</style>
