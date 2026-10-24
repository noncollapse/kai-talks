<script setup>
import { computed, ref } from 'vue'
import { useSlideContext } from '@slidev/client'
import MathTex from './MathTex.vue'

const { $clicks } = useSlideContext()
const selected = ref(1)
const colors = ['#4263eb', '#9161d5', '#0b9687']
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
    <div class="rloo-sampling">
      <div class="same-task"><b>01 · Same task <MathTex tex="T" /></b><small>Fixed data + frozen heads</small></div>
      <div class="sampling-step"><b>Router scores + noise</b><small>Sample from <MathTex tex="q_\psi" /></small></div><i>→</i>
      <div class="sampling-step"><b>Top-2 weights</b><small>One candidate route</small></div><i>→</i>
      <div class="sampling-step"><b>Intervals → reward</b><small>Score against known truth</small></div>
    </div>

    <div class="rloo-comparison">
      <section class="rloo-candidates">
        <div class="candidate-columns"><span>Route</span><span>Weights · <b :style="{color:colors[0]}">G</b> / <b :style="{color:colors[1]}">E</b> / <b :style="{color:colors[2]}">S</b></span><span>Reward <MathTex tex="r_i" /></span></div>
        <button v-for="(item, i) in candidates" :key="item.name" :aria-label="'Inspect candidate ' + item.name" :aria-pressed="selected === i" :class="{ inspecting: $clicks >= 2 && selected === i, 'in-baseline': $clicks >= 2 && selected !== i }" @click.stop="selected = i">
          <b class="candidate-letter">{{ item.name }}</b>
          <div class="candidate-weights"><div class="weight-bar" aria-hidden="true"><i v-for="(weight, head) in item.weights" :key="head" :style="{ width: weight * 100 + '%', background: colors[head] }" /></div><div class="weight-values"><span v-for="(weight, head) in item.weights" :key="head" :style="{ color: weight ? colors[head] : '#b8c0ce' }">{{ weight.toFixed(2) }}</span></div></div>
          <strong class="rloo-reveal" :class="{pending:$clicks < 1}">{{ signed(item.reward) }}</strong>
        </button>
        <div class="candidate-help">Click a route to inspect its leave-one-out baseline.</div>
      </section>

      <section class="rloo-baseline rloo-reveal" :class="{pending:$clicks < 2}">
        <div class="rloo-label">02 · Leave one out</div>
        <h3>Compare {{ current.name }} with the other routes</h3>
        <div class="baseline-rewards"><div v-for="(item, i) in candidates" :key="item.name" :class="{ excluded: i === selected }"><span>{{ item.name }}</span><b>{{ signed(item.reward) }}</b><small>{{ i === selected ? 'leave out' : 'include' }}</small></div></div>
        <div class="baseline-math"><MathTex :tex="baselineFormula" /></div>
        <div class="advantage-math" :class="{negative:advantage < 0}"><MathTex :tex="advantageFormula" /></div>
        <p><b>Advantage</b> = how much better this route did than the others.</p>
      </section>
    </div>

    <section class="rloo-update rloo-reveal" :class="{pending:$clicks < 3}">
      <div class="update-title"><span class="rloo-label">03 · Reinforce</span><h3>Update router <MathTex tex="\psi" /></h3><small>All sampled routes contribute.</small></div>
      <div class="update-math"><MathTex tex="\mathcal L_{\mathrm{RLOO}}=-\frac1K\sum_{i=1}^K\underbrace{A_i}_{\text{held fixed}}\log q_\psi(z_i\mid T)" /><p><span>Positive advantage → favor the sampled route.</span><span>Negative → discourage it.</span></p></div>
    </section>
  </div>
</template>

<style scoped>
.rloo-demo{width:876px;margin-top:19px}
.rloo-sampling{height:51px;box-sizing:border-box;display:flex;align-items:center;justify-content:space-between;gap:13px;background:#eef2ff;border-radius:11px;padding:10px 16px}.same-task{border-right:1px solid #d3dcef;padding-right:22px}.same-task>b{font-size:13px;color:#4263eb;display:block}.same-task>small{display:block;font-size:9px;color:#8693aa;margin-top:3px}.sampling-step>b{display:block;font-size:12px;color:#506384}.sampling-step>small{display:block;font-size:9px;color:#8693aa;margin-top:3px}.rloo-sampling>i{font-size:19px;font-style:normal;color:#a1b0c9}
.rloo-comparison{display:grid;grid-template-columns:364px 1fr;gap:24px;margin-top:14px;height:232px}
.candidate-columns{display:grid;grid-template-columns:37px 1fr 69px;align-items:center;padding:0 12px;margin-bottom:8px;font-size:10px;color:#7d8ba3;height:16px}.candidate-columns>span:last-child{text-align:right}
.rloo-candidates button{display:grid;grid-template-columns:37px 1fr 69px;align-items:center;width:100%;height:42px;box-sizing:border-box;padding:6px 12px;border:1px solid #dfe5f0;border-radius:8px;margin-bottom:6px;background:#fff;text-align:left;transition:background .3s,border-color .3s,box-shadow .3s}.rloo-candidates button.inspecting{border-color:#7c4dce;box-shadow:0 0 0 1px #7c4dce25;background:#f5f0fc}.rloo-candidates button.in-baseline{background:#f4f7fc}.rloo-candidates button:hover{border-color:#a68ad5}.candidate-letter{font-size:15px;color:#7d8ba5}.rloo-candidates button.inspecting .candidate-letter{color:#7c4dce}.candidate-weights{padding-right:18px}.weight-bar{display:flex;height:6px;overflow:hidden;border-radius:3px;background:#edf0f6}.weight-bar>i{height:100%;display:block}.weight-values{display:flex;justify-content:space-between;font-size:10px;line-height:1;margin-top:7px;font-variant-numeric:tabular-nums}.rloo-candidates button>strong{text-align:right;font-size:19px;font-variant-numeric:tabular-nums;color:#4263eb}.candidate-help{font-size:9px;color:#8e9ab0;margin-top:7px}
.rloo-baseline{box-sizing:border-box;border:1px solid #ded5ed;background:#faf8fe;border-radius:13px;padding:13px 17px;height:232px}.rloo-label{font-size:9px;color:#7c4dce;font-weight:800;letter-spacing:.08em;text-transform:uppercase}.rloo-baseline h3{font-size:18px;line-height:1.3;font-weight:800;color:#17233e;margin:6px 0 10px}.baseline-rewards{display:grid;grid-template-columns:repeat(4,1fr);gap:7px}.baseline-rewards>div{display:grid;grid-template-columns:18px 1fr;align-items:center;gap:1px 5px;background:#eee7fa;border-radius:6px;padding:6px 9px;color:#7c4dce}.baseline-rewards>div>span{font-size:11px;font-weight:800}.baseline-rewards>div>b{font-size:15px;text-align:right;font-variant-numeric:tabular-nums}.baseline-rewards small{grid-column:1/-1;font-size:8px;line-height:1.2;text-align:right}.baseline-rewards>.excluded{background:#f1f2f6;color:#a3acba}.baseline-rewards>.excluded>b{text-decoration:line-through}
.baseline-math{font-size:21px;line-height:1.45;margin-top:12px;color:#7c4dce}.advantage-math{font-size:22px;line-height:1.5;margin-top:9px;color:#0b9687}.advantage-math.negative{color:#c46f65}.rloo-baseline>p{font-size:10px;color:#8a7d9d;margin:8px 0 0;line-height:1.5}
.rloo-update{display:grid;grid-template-columns:185px 1fr;gap:16px;box-sizing:border-box;height:91px;margin-top:14px;border-radius:11px;background:#edf8f5;border-left:3px solid #0b9687;padding:11px 15px}.update-title{display:flex;flex-direction:column;justify-content:center;gap:6px}.update-title>.rloo-label{color:#0b9687;line-height:1.3}.update-title h3{font-size:17px;line-height:1.3;font-weight:800;margin:0;color:#0b9687}.update-title>small{display:block;font-size:9px;line-height:1.4;color:#7f9b94}.update-math>.math-tex-inline{font-size:21px;line-height:1.5;display:block;color:#17233e}.update-math>p{font-size:10px;line-height:1.4;margin:7px 0 0;display:flex;gap:14px;color:#5e8b80}
.rloo-reveal{transition:opacity .4s ease}.rloo-reveal.pending{opacity:0;visibility:hidden;pointer-events:none}
@media(prefers-reduced-motion:reduce){.rloo-reveal,.rloo-candidates button{transition:none}}
</style>
