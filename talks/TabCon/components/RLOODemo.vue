<script setup>
import { computed, ref } from 'vue'
import MathTex from './MathTex.vue'

const selected = ref(1)
const colors = ['#ce7b26', '#7c4dce', '#0b9687']
const candidates = [
  { name: 'A', weights: [.65, .35, 0], reward: .2 },
  { name: 'B', weights: [.35, .65, 0], reward: .8 },
  { name: 'C', weights: [.75, 0, .25], reward: -.1 },
  { name: 'D', weights: [0, .60, .40], reward: .5 },
]
const current = computed(() => candidates[selected.value])
const others = computed(() => candidates.filter((_, i) => i !== selected.value))
const baseline = computed(() => others.value.reduce((sum, item) => sum + item.reward, 0) / others.value.length)
const advantage = computed(() => current.value.reward - baseline.value)
const signed = value => (value > 0 ? '+' : '') + value.toFixed(1)
const baselineFormula = computed(() => 'b_{' + current.value.name + '}=\\frac{' + others.value.map(item => item.reward < 0 ? '(' + item.reward.toFixed(1) + ')' : item.reward.toFixed(1)).join('+') + '}{3}=' + baseline.value.toFixed(1))
const advantageFormula = computed(() => 'A_{' + current.value.name + '}=r_{' + current.value.name + '}-b_{' + current.value.name + '}=' + current.value.reward.toFixed(1) + '-' + baseline.value.toFixed(1) + '=' + signed(advantage.value))
</script>

<template>
  <div class="rloo-demo">
    <div class="rloo-comparison">
      <section class="rloo-candidates">
        <div class="candidate-columns"><span class="rloo-label sampling-label">1 · Sample multiple actions</span><span>Weights · <b :style="{color:colors[0]}">G</b> / <b :style="{color:colors[1]}">E</b> / <b :style="{color:colors[2]}">S</b></span><span>Reward <MathTex tex="r_i" /></span></div>
        <button v-for="(item, i) in candidates" :key="item.name" :aria-label="'Inspect candidate ' + item.name" :aria-pressed="selected === i" :class="{ inspecting: selected === i, 'in-baseline': selected !== i }" @click.stop="selected = i">
          <b class="candidate-letter">{{ item.name }}</b>
          <div class="candidate-weights"><div class="weight-bar" aria-hidden="true"><i v-for="(weight, head) in item.weights" :key="head" :style="{ width: weight * 100 + '%', background: colors[head] }" /></div><div class="weight-values"><span v-for="(weight, head) in item.weights" :key="head" :style="{ color: weight ? colors[head] : '#b8c0ce' }">{{ weight.toFixed(2) }}</span></div></div>
          <strong class="rloo-reveal">{{ signed(item.reward) }}</strong>
        </button>
      </section>

      <section class="rloo-baseline rloo-reveal">
        <div class="rloo-label">2 · Compute advantage function <MathTex tex="A_i" /></div>
        <h3>Compare {{ current.name }} with other actions</h3>
        <div class="baseline-rewards"><div v-for="(item, i) in candidates" :key="item.name" :class="{ excluded: i === selected }"><span>{{ item.name }}</span><b>{{ signed(item.reward) }}</b><small>{{ i === selected ? 'leave out' : 'include' }}</small></div></div>
        <div class="baseline-math"><MathTex :tex="baselineFormula" /></div>
        <div class="advantage-math" :class="{negative:advantage < 0}"><MathTex :tex="advantageFormula" /></div>
        <p><b>Advantage</b> = how much better this action did than the others.</p>
      </section>
    </div>

    <section class="rloo-update rloo-reveal">
      <div class="update-title"><span class="rloo-label">3 · Reinforce</span></div>
      <div class="policy-update-line"><span>Update router parameter according to the policy gradient of</span><MathTex tex="\mathcal{L}_{\textrm{RLOO}}=\frac{1}{4}\sum_i A_i\log\pi(i\mid\mathcal{D})" /></div>
    </section>
  </div>
</template>

<style scoped>
.rloo-demo{width:876px;margin-top:22px}
.rloo-comparison{display:grid;grid-template-columns:364px 1fr;gap:22px;height:278px}
.rloo-candidates,.rloo-baseline{box-sizing:border-box;background:#fff;border:1px solid #dce3f1;border-radius:13px;padding:14px}
.rloo-label{font-family:inherit;font-size:16px;font-weight:600;line-height:1.4;color:#17233e}
.candidate-columns{display:grid;grid-template-columns:32px 1fr 54px;align-items:center;gap:6px 0;margin-bottom:8px;font-size:12px;color:#64748b}
.candidate-columns .sampling-label{grid-column:1/-1}
.candidate-columns>span:nth-child(2){grid-column:2}
.candidate-columns>span:last-child{text-align:right;white-space:nowrap}
.rloo-candidates button{display:grid;grid-template-columns:32px 1fr 54px;align-items:center;width:100%;height:43px;box-sizing:border-box;padding:6px 10px;border:1px solid #dfe5f0;border-radius:8px;margin-bottom:7px;background:#fff;text-align:left;transition:border-color .3s,box-shadow .3s}
.rloo-candidates button:last-child{margin-bottom:0}
.rloo-candidates button.inspecting{border-color:#cf649a;box-shadow:0 0 0 1px #cf649a25}
.rloo-candidates button:hover{border-color:#cf649a}
.candidate-letter{font-size:17px;color:#17233e}
.candidate-weights{padding-right:12px}
.weight-bar{display:flex;height:7px;overflow:hidden;border-radius:3px;background:#edf0f6}
.weight-bar>i{height:100%;display:block}
.weight-values{display:flex;justify-content:space-between;font-size:13px;line-height:1;margin-top:7px;font-weight:600;font-variant-numeric:tabular-nums}
.rloo-candidates button>strong{text-align:right;font-size:19px;font-variant-numeric:tabular-nums;color:#17233e}
.rloo-baseline{padding:14px 18px}
.rloo-baseline h3{font-family:inherit;font-size:19px;line-height:1.3;font-weight:800;color:#17233e;margin:8px 0 14px}
.baseline-rewards{display:grid;grid-template-columns:repeat(4,1fr);gap:7px}
.baseline-rewards>div{display:grid;grid-template-columns:18px 1fr;align-items:center;gap:3px 4px;background:#fff;border:1px solid #e5e7eb;border-radius:6px;padding:7px 9px;color:#17233e}
.baseline-rewards>div>span{font-size:12px;font-weight:800}
.baseline-rewards>div>b{font-size:16px;text-align:right;font-variant-numeric:tabular-nums}
.baseline-rewards small{grid-column:1/-1;font-size:11px;line-height:1.2;text-align:right}
.baseline-rewards>.excluded{color:#9ca3af}
.baseline-rewards>.excluded>b{text-decoration:line-through}
.baseline-math{font-size:22px;line-height:1.5;margin-top:15px;color:#17233e}
.advantage-math{font-size:24px;line-height:1.5;margin-top:9px;color:#17233e}
.rloo-baseline>p{font-size:14px;color:#64748b;margin:9px 0 0;line-height:1.5}
.rloo-demo :deep(.katex){font-size:1em}
.rloo-update{display:grid;grid-template-columns:120px 1fr;align-items:center;gap:18px;box-sizing:border-box;min-height:84px;margin-top:14px;border:1px solid #dce3f1;border-radius:11px;background:#fff;padding:12px 18px}
.update-title{align-self:start;padding-top:3px}
.policy-update-line{display:flex;flex-direction:column;align-items:flex-start;gap:8px;font-size:15px;line-height:1.5;color:#17233e}
.policy-update-line>span{font-family:inherit;font-weight:400;font-size:15px}
.policy-update-line>.math-tex-inline{font-size:23px}
.rloo-reveal{transition:opacity .4s ease}
@media(prefers-reduced-motion:reduce){.rloo-reveal,.rloo-candidates button{transition:none}}
</style>
