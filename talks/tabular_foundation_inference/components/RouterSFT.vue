<script setup>
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'
import MathTex from './MathTex.vue'

const { $clicks } = useSlideContext()
const normalize = values => {
  const total = values.reduce((sum, value) => sum + value, 0)
  return values.map(value => value / total)
}
const density = (center, spread) => normalize(Array.from({ length: 15 }, (_, i) => Math.exp(-0.5 * ((i - center) / spread) ** 2)))
const experts = [
  { name: 'Global', key: 'G', color: '#4263eb', weight: 0.25, p: density(6, 2.2) },
  { name: 'Expansion', key: 'E', color: '#9161d5', weight: 0.60, p: density(7, 3.5) },
  { name: 'Shrinkage', key: 'S', color: '#0b9687', weight: 0.15, p: density(6, 1.2) },
]
const stacks = experts[0].p.map((_, bin) => {
  let cumulative = 0
  return experts.map(expert => {
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
      <path d="M224 328H298" fill="none" stroke="#a6b4ca" stroke-width="1.7" marker-end="url(#sft-forward)" />
      <g class="sft-reveal" :class="{ concealed: !showMixture }" fill="none" stroke-width="1.7" marker-end="url(#sft-forward)">
        <path v-for="(expert, i) in experts" :key="expert.key" :d="`M224 ${65 + i * 78}H298`" :stroke="expert.color" stroke-opacity=".6" />
        <path d="M574 164H632" stroke="#a6b4ca" />
        <path d="M757 94V112" stroke="#a6b4ca" />
        <path d="M439 290V260" stroke="#a6b4ca" />
      </g>
      <path class="sft-reveal gradient-path" :class="{ concealed: !showGradient }" d="M757 254V376Q757 390 743 390H453Q439 390 439 376V369" fill="none" stroke="#7c4dce" stroke-width="2.2" stroke-dasharray="6 5" marker-end="url(#sft-backward)" />
    </svg>

    <div class="sft-section-label experts-label">Three frozen residual heads</div>
    <section v-for="(expert, i) in experts" :key="expert.key" class="sft-expert" :style="{ top: `${32 + i * 78}px`, '--expert': expert.color }">
      <div><h3>{{ expert.name }}</h3><MathTex :tex="`p_${expert.key}`" /></div>
      <div class="expert-density" aria-hidden="true"><i v-for="(p, j) in expert.p" :key="j" :style="{ height: `${p * 150}px` }" /></div>
    </section>

    <div class="sft-section-label mixture-label sft-reveal" :class="{ concealed: !showMixture }">Mix all three distributions</div>
    <section class="sft-distribution sft-reveal" :class="{ concealed: !showMixture }">
      <h3>Mixture for one query</h3>
      <MathTex tex="p=\pi_G p_G+\pi_E p_E+\pi_S p_S" />
      <svg viewBox="0 0 236 119" aria-label="Illustrative dense mixture with contributions from all three frozen experts, and the observed training error e">
        <line x1="13" x2="222" y1="93" y2="93" stroke="#b4c0d5" />
        <g v-for="(stack, bin) in stacks" :key="bin">
          <rect v-for="(part, head) in stack" :key="head" :x="14 + bin * 14" :y="part.y" width="10" :height="part.height" :fill="part.color" />
        </g>
        <path d="M173 12V96" stroke="#17233e" stroke-width="1.5" stroke-dasharray="3 3" />
        <text x="173" y="9" text-anchor="middle" style="font-style:italic;fill:#17233e;font-size:13px">e</text>
        <text x="14" y="113" style="fill:#8490a7;font-size:9px">Estimation error</text>
        <text x="173" y="113" text-anchor="middle" style="fill:#17233e;font-size:9px">Observed</text>
      </svg>
      <div class="mixture-key"><span v-for="expert in experts" :key="expert.key"><i :style="{ background: expert.color }" />{{ expert.name }}</span></div>
    </section>

    <section class="sft-target">
      <span>Known error from the simulated task</span>
      <MathTex tex="e=\widehat f(x)-f(x)" />
    </section>
    <section class="sft-objective sft-reveal" :class="{ concealed: !showMixture }">
      <h3>Score the mixture</h3>
      <MathTex tex="\begin{aligned}\mathcal L_{\mathrm{SFT}}={}&\mathrm{NLL}(p,e)\\&+\eta_3\,\mathrm{CRPS}(p,e)\end{aligned}" />
    </section>

    <section class="sft-embeddings"><span class="sft-badge frozen-badge">FROZEN</span><h3>Query embeddings</h3><p>From the TabPFN backbone</p></section>
    <section class="sft-trainable" :class="{ learning: showGradient }">
      <div class="router-heading"><h3>Router <MathTex tex="\psi" /></h3><span class="sft-badge train-badge">TRAINABLE</span></div>
      <div class="sft-weight-chips"><span v-for="expert in experts" :key="expert.key" :style="{ '--expert': expert.color }"><b>{{ expert.key }}</b>{{ expert.weight.toFixed(2) }}</span></div>
    </section>
    <div class="weights-caption sft-reveal" :class="{ concealed: !showMixture }">Dense weights <MathTex tex="\pi" /></div>
    <div class="sft-backprop sft-reveal" :class="{ concealed: !showGradient }"><b>Update router only</b><p>Backpropagate through<br>the mixing weights.</p></div>
  </div>
</template>

<style scoped>
.sft-map{position:relative;width:876px;height:400px;margin-top:19px}
.sft-connectors{position:absolute;inset:0;width:876px;height:400px;pointer-events:none}
.sft-map section{position:absolute;box-sizing:border-box;background:#fff;border:1px solid #dce4f2;border-radius:13px}
.sft-map h3{margin:0;font-size:17px;line-height:1.3;font-weight:800}
.sft-section-label{position:absolute;top:0;font-size:10px;font-weight:700;letter-spacing:.035em;color:#7d8ba4}
.experts-label{left:0}.mixture-label{left:304px}
.sft-expert{left:0;width:224px;height:66px;border-left:3px solid var(--expert)!important;padding:11px 14px;display:flex;justify-content:space-between;align-items:center}
.sft-expert h3{font-size:16px;color:var(--expert)}.sft-expert .math-tex-inline{display:inline-block;margin-top:4px;font-size:13px;color:#7c89a2}
.expert-density{display:flex;align-items:flex-end;gap:2px;height:42px}.expert-density i{width:4px;display:block;background:var(--expert);opacity:.65;border-radius:1.5px 1.5px 0 0}
.sft-distribution{left:304px;top:32px;width:270px;height:222px;padding:16px 15px 12px;background:#f3f5fc!important;text-align:center}
.sft-distribution>.math-tex-inline{display:block;font-size:17px;margin-top:10px}.sft-distribution>svg{display:block;width:236px;height:119px;margin-top:7px}
.mixture-key{display:flex;justify-content:center;gap:11px;margin-top:3px;font-size:8px;color:#7a88a0}.mixture-key>span{display:flex;align-items:center;gap:4px}.mixture-key i{display:inline-block;width:6px;height:6px;border-radius:1px}
.sft-target{left:638px;top:32px;width:238px;height:62px;padding:9px 14px;background:#eef1f8!important;text-align:center}.sft-target>span:first-child{display:block;color:#7b89a1;font-size:9px;margin-bottom:7px}.sft-target>.math-tex-inline{font-size:19px}
.sft-objective{left:638px;top:118px;width:238px;height:136px;padding:16px 18px}.sft-objective h3{font-size:17px}.sft-objective>.math-tex-inline{display:block;margin-top:13px;font-size:19px}
.sft-embeddings{left:0;top:292px;width:224px;height:74px;padding:13px 14px;background:#eef1f8!important;border-color:#eef1f8!important}.sft-embeddings h3{font-size:15px;margin:5px 0 4px}.sft-embeddings p{font-size:10px;color:#7b89a1;margin:0}.sft-embeddings>.sft-badge{position:absolute;right:10px;top:8px;font-size:7px}
.sft-badge{font-size:8px;letter-spacing:.06em;font-weight:800}.frozen-badge{color:#8a97ad}.train-badge{background:#ede6fb;color:#7c4dce;padding:4px 7px;border-radius:5px}
.sft-trainable{left:304px;top:290px;width:270px;height:76px;padding:11px 14px;background:#f8f4ff!important;border-color:#d9c9f3!important;transition:box-shadow .5s,border-color .5s}.sft-trainable.learning{border-color:#9161d5!important;box-shadow:0 0 0 3px #9161d514}.router-heading{display:flex;justify-content:space-between;align-items:center}.router-heading h3{color:#7c4dce}
.sft-weight-chips{display:flex;gap:7px;margin-top:8px}.sft-weight-chips>span{display:flex;justify-content:space-between;gap:9px;flex:1;padding:4px 9px;border-radius:5px;background:#fff;color:var(--expert);font-size:11px;line-height:1.2}.sft-weight-chips b{font-size:10px}
.weights-caption{position:absolute;left:454px;top:268px;font-size:10px;color:#7c4dce;white-space:nowrap}
.sft-backprop{position:absolute;left:638px;top:291px;width:238px;text-align:center;color:#7c4dce;background:#fbfcff;padding:3px 0}.sft-backprop>b{font-size:16px}.sft-backprop>p{font-size:12px;line-height:1.5;margin:8px 0 0;color:#8c75ab}
.sft-reveal{transition:opacity .5s ease}.sft-reveal.concealed{opacity:0;pointer-events:none}.gradient-path{stroke-dashoffset:0;animation:sft-gradient-flow 1.8s linear infinite}
@keyframes sft-gradient-flow{to{stroke-dashoffset:-22}}
@media(prefers-reduced-motion:reduce){.gradient-path{animation:none}.sft-reveal,.sft-trainable{transition:none}}
</style>
