<script setup>
import { computed, ref } from 'vue'
import MathTex from './MathTex.vue'
const regime = ref('under')
const modes = [
  {id:'under',name:'Low score',rule:String.raw`S\le s_1`,color:'#7c4dce'},
  {id:'middle',name:'Middle score',rule:String.raw`s_1<S<s_2`,color:'#64748b'},
  {id:'over',name:'High score',rule:String.raw`S\ge s_2`,color:'#0b9687'},
]
const selected = computed(() => modes.find(mode => mode.id === regime.value))
</script>

<template>
  <div class="specialist-controls" role="group" aria-label="Training task regime"><button v-for="mode in modes" :key="mode.id" :aria-label="mode.name" :aria-pressed="regime===mode.id" :style="{'--regime-color':mode.color}" @click.stop="regime=mode.id"><span class="regime-name">{{mode.name}}</span><MathTex :tex="mode.rule" /></button></div>
  <div class="specialist-graph">
    <div class="task-tile"><span>Score the new training dataset</span><div class="task-condition" :style="{color:selected.color}"><MathTex :tex="selected.rule" /></div><p>Compute <MathTex tex="S" /> from Global's coverage.<br>Apply the fixed cutoffs.</p><b>Backbone + Global: frozen</b></div>
    <div class="branch-symbol">→</div>
    <div class="specialist-updates">
      <div v-for="head in [{name:'Expansion',active:'under',color:'#7c4dce'},{name:'Shrinkage',active:'over',color:'#0b9687'}]" :key="head.name" class="specialist-update" :style="{'--specialist':head.color}">
        <h3>{{head.name}}</h3><div class="loss-chips"><span :class="{enabled:regime===head.active}">NLL</span><span :class="{enabled:regime===head.active}">CRPS</span><span class="enabled">KL</span></div>
        <p>{{regime===head.active?"Fit this task's error distribution.":'Use KL to stay close to Global.'}}</p>
      </div>
    </div>
  </div>
  <div class="detail-message">Both heads receive KL. Only the assigned head receives NLL + CRPS.</div>
</template>

<style scoped>
.specialist-controls{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:18px 0 17px}.specialist-controls button{display:flex;align-items:center;justify-content:space-between;gap:10px;border:1px solid #dce3f2;border-top:3px solid #dce3f2;border-radius:10px;padding:13px 17px;color:#64748b;background:white;font-size:20px;transition:background .2s,border-color .2s}.specialist-controls .regime-name{font-size:12px;font-weight:700;white-space:nowrap}.specialist-controls button[aria-pressed=true]{background:#f2f4fb;color:var(--regime-color);border-color:var(--regime-color)}.specialist-graph{display:grid;grid-template-columns:260px 50px 1fr;align-items:center}.task-tile{background:#eef1f8;border-radius:14px;padding:24px}.task-tile>span{font-size:11px;color:#64748b}.task-condition{font-size:28px;line-height:1.5;margin:13px 0}.task-tile p{font-size:14px;color:#64748b;line-height:1.7}.task-tile b{font-size:11px;color:#7d89a1;display:block;margin-top:22px}.branch-symbol{text-align:center;font-size:29px;color:#b0bdd5}.specialist-updates{display:grid;gap:12px}.specialist-update{border:1px solid #dfe5f1;border-left:3px solid var(--specialist);background:#fff;border-radius:12px;padding:12px 17px}.specialist-update h3{font-size:18px;font-weight:800;color:var(--specialist);margin:0 0 8px}.loss-chips{display:flex;gap:8px}.loss-chips span{padding:5px 10px;font-size:12px;background:#edf0f7;color:#aab4c6;border-radius:6px;opacity:.35;transition:opacity .4s,color .4s}.loss-chips .enabled{opacity:1;color:var(--specialist);font-weight:700}.specialist-update p{font-size:12px;color:#64748b;margin:8px 0 0}
</style>
