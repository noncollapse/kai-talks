<script setup>
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'
import MathTex from './MathTex.vue'

const { $clicks } = useSlideContext()
const density = (center, spread) => {
  const values = Array.from({ length: 15 }, (_, i) => Math.exp(-0.5 * ((i - center) / spread) ** 2))
  const total = values.reduce((a, b) => a + b, 0)
  return values.map(value => value / total)
}
const experts = [
  { name: 'Global', key: 'G', color: '#4263eb', dense: 0.25, p: density(6, 2.2) },
  { name: 'Expansion', key: 'E', color: '#9161d5', dense: 0.60, p: density(7, 3.5) },
  { name: 'Shrinkage', key: 'S', color: '#0b9687', dense: 0.15, p: density(6, 1.2) },
]
const selected = [...experts].sort((a, b) => b.dense - a.dense).slice(0, 2)
const selectedMass = selected.reduce((sum, expert) => sum + expert.dense, 0)
experts.forEach(expert => { expert.weight = selected.includes(expert) ? expert.dense / selectedMass : 0 })
const stacks = experts[0].p.map((_, bin) => {
  let cumulative = 0
  return experts.filter(expert => expert.weight > 0).map(expert => {
    const height = expert.weight * expert.p[bin] * 470
    cumulative += height
    return { height, y: 92 - cumulative, color: expert.color }
  })
})
const showMixture = computed(() => $clicks.value >= 1)
const showGradient = computed(() => $clicks.value >= 2)
</script>

<template>
  <div class="sft-map">
    <svg class="sft-connectors" viewBox="0 0 876 400" aria-hidden="true">
      <defs>
        <marker id="sft-forward" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7" fill="#a6b4ca" /></marker>
        <marker id="sft-backward" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7" fill="#7c4dce" /></marker>
      </defs>
      <path d="M208 338H260" fill="none" stroke="#a6b4ca" stroke-width="1.7" marker-end="url(#sft-forward)" />
      <g class="sft-reveal" :class="{ concealed: !showMixture }" fill="none" stroke-width="1.7">
        <path d="M208 59H344" stroke="#4263eb" marker-end="url(#sft-forward)" />
        <path d="M208 132H344" stroke="#9161d5" marker-end="url(#sft-forward)" />
        <path d="M208 205H300" stroke="#bec8d8" stroke-dasharray="4 4" />
        <path d="M598 171H642" stroke="#a6b4ca" marker-end="url(#sft-forward)" />
        <path d="M762 90V112" stroke="#a6b4ca" marker-end="url(#sft-forward)" />
        <path d="M474 278V257" stroke="#a6b4ca" marker-end="url(#sft-forward)" />
      </g>
      <path class="sft-reveal gradient-path" :class="{ concealed: !showGradient }" d="M762 250V380Q762 392 750 392H444Q432 392 432 380V378" fill="none" stroke="#7c4dce" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#sft-backward)" />
    </svg>

    <div class="sft-section-label experts-label">Frozen residual heads</div>
    <section v-for="(expert, i) in experts" :key="expert.key" class="sft-expert" :style="{ top: `${28 + i * 73}px`, '--expert': expert.color }">
      <div><h3>{{ expert.name }}</h3><MathTex :tex="`p_${expert.key}`" /></div>
      <div class="expert-density" aria-hidden="true"><i v-for="(p, j) in expert.p" :key="j" :style="{ height: `${p * 130}px` }" /></div>
    </section>
    <div class="computed-note">All three are evaluated during SFT.</div>
    <div class="sft-zero sft-reveal" :class="{ concealed: !showMixture }"><b>0</b><span>weight</span></div>

    <div class="sft-section-label mixture-label sft-reveal" :class="{ concealed: !showMixture }">Forward · only two nonzero weights</div>
    <section class="sft-distribution sft-reveal" :class="{ concealed: !showMixture }">
      <h3>Top-2 mixture</h3>
      <MathTex tex="p=w_Gp_G+w_Ep_E" />
      <svg viewBox="0 0 236 119" aria-label="Illustrative Top-2 mixture: Global and Expansion contribute; Shrinkage has zero weight. The dashed line marks the observed error.">
        <line x1="13" x2="222" y1="93" y2="93" stroke="#b4c0d5" />
        <g v-for="(stack, bin) in stacks" :key="bin">
          <rect v-for="(part, head) in stack" :key="head" :x="14 + bin * 14" :y="part.y" width="10" :height="part.height" :fill="part.color" />
        </g>
        <path d="M173 12V96" stroke="#17233e" stroke-width="1.5" stroke-dasharray="3 3" />
        <text x="173" y="9" text-anchor="middle" style="font-style:italic;fill:#17233e;font-size:13px">e</text>
        <text x="14" y="113" style="fill:#8490a7;font-size:9px">Estimation error</text>
        <text x="173" y="113" text-anchor="middle" style="fill:#17233e;font-size:9px">Observed</text>
      </svg>
      <div class="mixture-note">Pair and weights are chosen per task.</div>
    </section>

    <section class="sft-target"><span>Known error from the simulated task</span><MathTex tex="e=\widehat f(x)-f(x)" /></section>
    <section class="sft-objective sft-reveal" :class="{ concealed: !showMixture }">
      <h3>Score the mixture</h3>
      <MathTex tex="\mathrm{NLL}(p,e)+\mathrm{CRPS}(p,e)" />
      <p>Learn from the observed errors.<br>No expert-selection labels.</p>
    </section>

    <section class="sft-embeddings"><span class="sft-badge frozen-badge">FROZEN</span><h3>Query embeddings</h3><p>From the TabPFN backbone</p></section>
    <section class="sft-trainable" :class="{ learning: showGradient }">
      <div class="router-heading"><h3>Task router <MathTex tex="\psi" /></h3><span class="sft-badge train-badge">TRAINABLE</span></div>
      <div class="sft-weight-row"><span>Softmax</span><div v-for="expert in experts" :key="expert.key" :style="{ '--expert': expert.color }"><b>{{ expert.key }}</b>{{ expert.dense.toFixed(2) }}</div></div>
      <div class="sft-weight-row sft-reveal" :class="{ concealed: !showMixture }"><span>Top-2 + normalize</span><div v-for="expert in experts" :key="expert.key" :class="{ inactive: !expert.weight }" :style="{ '--expert': expert.color }"><b>{{ expert.key }}</b>{{ expert.weight ? expert.weight.toFixed(2) : '0' }}</div></div>
    </section>
    <div class="weights-caption sft-reveal" :class="{ concealed: !showMixture }">Shared across queries</div>
    <div class="sft-backprop sft-reveal" :class="{ concealed: !showGradient }"><span>BACKWARD · ROUTER ONLY</span><b>Straight-through</b><p>Dense-softmax proxy gradient.<br>All three scores can change.</p></div>
  </div>
</template>

<style scoped>
.sft-map{position:relative;width:876px;height:400px;margin-top:19px}
.sft-connectors{position:absolute;inset:0;width:876px;height:400px;pointer-events:none}
.sft-map section{position:absolute;box-sizing:border-box;background:#fff;border:1px solid #dce4f2;border-radius:13px}
.sft-map h3{margin:0;font-size:17px;line-height:1.3;font-weight:800}
.sft-section-label{position:absolute;top:0;font-size:10px;font-weight:700;color:#7d8ba4}.experts-label{left:0}.mixture-label{left:350px}
.sft-expert{left:0;width:208px;height:62px;border-left:3px solid var(--expert)!important;padding:9px 12px;display:flex;justify-content:space-between;align-items:center}
.sft-expert h3{font-size:15px;color:var(--expert)}.sft-expert .math-tex-inline{display:inline-block;margin-top:3px;font-size:13px;color:#7c89a2}
.expert-density{display:flex;align-items:flex-end;gap:2px;height:40px}.expert-density i{width:3px;display:block;background:var(--expert);opacity:.65;border-radius:1px 1px 0 0}
.computed-note{position:absolute;left:0;top:247px;font-size:10px;color:#7d8ba4}
.sft-zero{position:absolute;left:299px;top:192px;display:flex;flex-direction:column;align-items:center;color:#9aa7bb;background:#fbfcff;padding:0 5px}.sft-zero b{font-size:17px;line-height:20px}.sft-zero span{font-size:9px}
.sft-distribution{left:350px;top:28px;width:248px;height:222px;padding:14px 5px 10px;background:#f3f5fc!important;text-align:center}
.sft-distribution>.math-tex-inline{display:block;font-size:17px;margin-top:9px}.sft-distribution>svg{display:block;width:236px;height:119px;margin-top:6px}
.mixture-note{font-size:9px;color:#7a88a0;margin-top:4px}
.sft-target{left:648px;top:28px;width:228px;height:62px;padding:9px 10px;background:#eef1f8!important;text-align:center}.sft-target>span:first-child{display:block;color:#7b89a1;font-size:9px;margin-bottom:7px}.sft-target>.math-tex-inline{font-size:19px}
.sft-objective{left:648px;top:118px;width:228px;height:132px;padding:14px 15px}.sft-objective>.math-tex-inline{display:block;margin-top:13px;font-size:17px}.sft-objective p{font-size:11px;line-height:1.5;margin:10px 0 0;color:#7b89a1}
.sft-embeddings{left:0;top:302px;width:208px;height:72px;padding:13px 12px;background:#eef1f8!important;border-color:#eef1f8!important}.sft-embeddings h3{font-size:15px;margin:5px 0 4px}.sft-embeddings p{font-size:10px;color:#7b89a1;margin:0}.sft-embeddings>.sft-badge{position:absolute;right:10px;top:8px;font-size:7px}
.sft-badge{font-size:8px;letter-spacing:.06em;font-weight:800}.frozen-badge{color:#8a97ad}.train-badge{background:#ede6fb;color:#7c4dce;padding:4px 7px;border-radius:5px}
.sft-trainable{left:266px;top:278px;width:332px;height:96px;padding:9px 12px;background:#f8f4ff!important;border-color:#d9c9f3!important;transition:box-shadow .5s,border-color .5s}.sft-trainable.learning{border-color:#9161d5!important;box-shadow:0 0 0 3px #9161d514}.router-heading{display:flex;justify-content:space-between;align-items:center}.router-heading h3{color:#7c4dce;font-size:16px}
.sft-weight-row{display:grid;grid-template-columns:112px repeat(3,1fr);gap:6px;margin-top:6px;align-items:center;font-size:10px}.sft-weight-row>span{color:#7e6c98;font-size:10px}.sft-weight-row>div{display:flex;justify-content:space-between;gap:4px;padding:4px 6px;border-radius:4px;background:#fff;color:var(--expert);line-height:1.2}.sft-weight-row b{font-size:9px}.sft-weight-row>div.inactive{color:#9aa7bb;background:#eef0f5}
.weights-caption{position:absolute;left:487px;top:253px;font-size:9px;color:#7c4dce;white-space:nowrap}
.sft-backprop{position:absolute;left:648px;top:274px;width:228px;text-align:center;color:#7c4dce;background:#fbfcff;padding:5px 0}.sft-backprop>span{display:block;font-size:8px;letter-spacing:.06em;font-weight:700;margin-bottom:7px}.sft-backprop>b{font-size:19px}.sft-backprop>p{font-size:12px;line-height:1.5;margin:9px 0 0;color:#8c75ab}
.sft-reveal{transition:opacity .5s ease}.sft-reveal.concealed{opacity:0;pointer-events:none}.gradient-path{animation:sft-gradient-flow 1.8s linear infinite}
@keyframes sft-gradient-flow{to{stroke-dashoffset:-22}}
@media(prefers-reduced-motion:reduce){.gradient-path{animation:none}.sft-reveal,.sft-trainable{transition:none}}
</style>
