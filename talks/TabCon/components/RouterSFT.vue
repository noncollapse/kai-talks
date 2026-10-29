<script setup>
import MathTex from './MathTex.vue'

const density = (center, spread) => {
  const values = Array.from({ length: 15 }, (_, i) => Math.exp(-0.5 * ((i - center) / spread) ** 2))
  const total = values.reduce((a, b) => a + b, 0)
  return values.map(value => value / total)
}
const experts = [
  { name: 'Global', key: 'G', color: '#ce7b26', dense: 0.25, p: density(6, 2.2) },
  { name: 'Expansion', key: 'E', color: '#7c4dce', dense: 0.60, p: density(7, 3.5) },
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
const showMixture = true
const showGradient = true
</script>

<template>
  <div class="sft-map">
    <svg class="sft-connectors" viewBox="0 0 876 400" aria-hidden="true">
      <defs>
        <marker id="sft-forward" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7" fill="#a6b4ca" /></marker>
        <marker id="sft-backward" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7" fill="#cf649a" /></marker>
        <marker id="sft-orange" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7" fill="#ce7b26" /></marker>
        <marker id="sft-purple" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7" fill="#7c4dce" /></marker>
      </defs>
      <path d="M208 338H260" fill="none" stroke="#a6b4ca" stroke-width="1.7" marker-end="url(#sft-forward)" />
      <g class="sft-reveal" :class="{ concealed: !showMixture }" fill="none" stroke-width="1.7">
        <path d="M208 59H304" stroke="#ce7b26" marker-end="url(#sft-orange)" />
        <path d="M208 132H304" stroke="#7c4dce" marker-end="url(#sft-purple)" />
        <path d="M208 205H300" stroke="#bec8d8" stroke-dasharray="4 4" />
        <path d="M558 184H642" stroke="#a6b4ca" marker-end="url(#sft-forward)" />
        <path d="M762 116V144" stroke="#a6b4ca" marker-end="url(#sft-forward)" />
        <path d="M434 278V237" stroke="#a6b4ca" marker-end="url(#sft-forward)" />
      </g>
      <path class="sft-reveal gradient-path" :class="{ concealed: !showGradient }" d="M762 238V380Q762 392 750 392H444Q432 392 432 380V378" fill="none" stroke="#cf649a" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#sft-backward)" />
    </svg>

    <div class="sft-section-label experts-label">Frozen three experts</div>
    <section v-for="(expert, i) in experts" :key="expert.key" class="sft-expert" :style="{ top: `${28 + i * 73}px`, '--expert': expert.color }">
      <div><h3><span class="expert-ice">❄</span>{{ expert.name }}</h3><MathTex :tex="`p_${expert.key}`" /></div>
      <div class="expert-density" aria-hidden="true"><i v-for="(p, j) in expert.p" :key="j" :style="{ height: `${p * 130}px` }" /></div>
    </section>

    <section class="sft-distribution sft-reveal" :class="{ concealed: !showMixture }">
      <h3>Top-2 mixture distribution</h3>
      <MathTex tex="p=w_Gp_G+w_Ep_E" />
      <svg viewBox="0 0 236 100" aria-label="Illustrative Top-2 mixture: Global and Expansion contribute; Shrinkage has zero weight.">
        <line x1="13" x2="222" y1="93" y2="93" stroke="#b4c0d5" />
        <g v-for="(stack, bin) in stacks" :key="bin">
          <rect v-for="(part, head) in stack" :key="head" :x="14 + bin * 14" :y="part.y" width="10" :height="part.height" :fill="part.color" />
        </g>
      </svg>
    </section>

    <section class="sft-target"><span>Compute residual from simulated data</span><MathTex tex="r=\widehat f(x)-f(x)" /></section>
    <section class="sft-objective sft-reveal" :class="{ concealed: !showMixture }">
      <h3>Define the loss</h3>
      <MathTex tex="\mathrm{NLL}(p,r)+\mathrm{CRPS}(p,r)" />
    </section>

    <section class="sft-embeddings">
      <h3>Query embeddings</h3>
      <div class="embedding-tokens">
        <div v-for="token in 5" :key="token"><MathTex :tex="`\\boldsymbol{h}_{${token}}`"/><i v-for="cell in 2" :key="cell" :style="{opacity:.35+((token+cell)%4)*.15}"/></div>
      </div>
    </section>
    <section class="sft-trainable" :class="{ learning: showGradient }">
      <div class="router-heading"><h3>Router</h3><span class="router-fire" aria-label="Trainable">🔥</span></div>
      <div class="sft-weight-row"><span>Softmax</span><div v-for="expert in experts" :key="expert.key" :style="{ '--expert': expert.color }"><b>{{ expert.key }}</b>{{ expert.dense.toFixed(2) }}</div></div>
      <div class="sft-weight-row sft-reveal" :class="{ concealed: !showMixture }"><span>Top-2 + normalize</span><div v-for="expert in experts" :key="expert.key" :class="{ inactive: !expert.weight }" :style="{ '--expert': expert.color }"><b>{{ expert.key }}</b>{{ expert.weight ? expert.weight.toFixed(2) : '0' }}</div></div>
    </section>
    <div class="routing-weight-labels sft-reveal" :class="{ concealed: !showMixture }"><MathTex tex="w_G" /><MathTex tex="w_E" /></div>

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
.sft-zero{position:absolute;left:253px;top:190px;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;color:#9aa7bb;background:#fbfcff;padding:0 5px}.sft-zero b{font-size:17px;line-height:20px}.sft-zero span{font-size:9px}
.sft-distribution{left:310px;top:28px;width:248px;height:222px;padding:14px 5px 10px;background:#f3f5fc!important;text-align:center}
.sft-distribution>.math-tex-inline{display:block;font-size:17px;margin-top:9px}.sft-distribution>svg{display:block;width:236px;height:119px;margin-top:6px}
.mixture-note{font-size:9px;color:#7a88a0;margin-top:4px}
.sft-target{left:648px;top:28px;width:228px;height:62px;padding:9px 10px;background:#eef1f8!important;text-align:center}.sft-target>span:first-child{display:block;color:#7b89a1;font-size:9px;margin-bottom:7px}.sft-target>.math-tex-inline{font-size:19px}
.sft-objective{left:648px;top:118px;width:228px;height:132px;padding:14px 15px}.sft-objective>.math-tex-inline{display:block;margin-top:13px;font-size:17px}.sft-objective p{font-size:11px;line-height:1.5;margin:10px 0 0;color:#7b89a1}
.sft-embeddings{left:0;top:302px;width:208px;height:72px;padding:13px 12px;background:#eef1f8!important;border-color:#eef1f8!important}.sft-embeddings h3{font-size:15px;margin:5px 0 4px}.sft-embeddings p{font-size:10px;color:#7b89a1;margin:0}.sft-embeddings>.sft-badge{position:absolute;right:10px;top:8px;font-size:7px}
.sft-badge{font-size:8px;letter-spacing:.06em;font-weight:800}.frozen-badge{color:#8a97ad}.train-badge{background:#ede6fb;color:#7c4dce;padding:4px 7px;border-radius:5px}
.sft-trainable{left:266px;top:278px;width:332px;height:96px;padding:9px 12px;background:#f8f4ff!important;border-color:#d9c9f3!important;transition:box-shadow .5s,border-color .5s}.sft-trainable.learning{border-color:#9161d5!important;box-shadow:0 0 0 3px #9161d514}.router-heading{display:flex;justify-content:space-between;align-items:center}.router-heading h3{color:#7c4dce;font-size:16px}
.sft-weight-row{display:grid;grid-template-columns:112px repeat(3,minmax(0,1fr));gap:6px;margin-top:5px;align-items:center;font-size:13px}.sft-weight-row>span{color:#7e6c98;font-size:12px;white-space:nowrap}.sft-weight-row>div{display:flex;justify-content:space-between;align-items:center;gap:4px;padding:3px 4px;border-radius:4px;background:#fff;color:var(--expert);line-height:1.2}.sft-weight-row b{font-size:11px}.sft-weight-row>div.inactive{color:#9aa7bb;background:#eef0f5}
.weights-caption{position:absolute;left:487px;top:253px;font-size:9px;color:#7c4dce;white-space:nowrap}
.sft-backprop{position:absolute;left:648px;top:274px;width:228px;text-align:center;color:#7c4dce;background:#fbfcff;padding:5px 0}.sft-backprop>span{display:block;font-size:8px;letter-spacing:.06em;font-weight:700;margin-bottom:7px}.sft-backprop>b{font-size:19px}.sft-backprop>p{font-size:12px;line-height:1.5;margin:9px 0 0;color:#8c75ab}
.sft-reveal{transition:opacity .5s ease}.sft-reveal.concealed{opacity:0;pointer-events:none}.gradient-path{animation:sft-gradient-flow 1.8s linear infinite}
@keyframes sft-gradient-flow{to{stroke-dashoffset:-22}}
@media(prefers-reduced-motion:reduce){.gradient-path{animation:none}.sft-reveal,.sft-trainable{transition:none}}
</style>

<style scoped>
/* Match the architecture and routing diagrams on Pages 22–23. */
.sft-map h3,.sft-section-label{font-family:Manrope,sans-serif;font-size:17px;font-weight:800;line-height:1.3}
.experts-label{color:#17233e;top:0}
.sft-expert h3{font-size:17px;color:var(--expert)}
.sft-expert{border-radius:10px}
.sft-map .sft-distribution,.sft-map .sft-target{background:#fff!important}
.sft-map .sft-trainable{background:#fff!important;border:1px solid #dce3f1!important;border-left:3px solid #cf649a!important;border-radius:10px}
.sft-map .sft-trainable.learning{border-left-color:#cf649a!important;box-shadow:0 0 0 3px #cf649a14}
.router-heading h3{font-size:17px;color:#bd4d86}
.train-badge{background:#fff0f7;color:#bd4d86}
.sft-weight-row>span,.weights-caption{color:#64748b}
.sft-backprop{color:#bd4d86}.sft-backprop>p{color:#64748b}
.sft-map .sft-embeddings{top:302px;height:72px;padding:0;background:transparent!important;border:0!important}
.sft-embeddings h3{position:absolute;bottom:calc(100% + 7px);left:0;width:100%;font-size:15px;text-align:center;margin:0;color:#17233e}
.embedding-tokens{height:72px;box-sizing:border-box;display:flex;justify-content:center;gap:7px;padding:10px 8px;background:white;border:1px solid #dce3f1;border-radius:10px}
.embedding-tokens>div{display:flex;flex-direction:column;align-items:center;gap:5px}
.embedding-tokens .math-tex-inline{font-size:14px;color:#111}
.embedding-tokens i{display:block;width:23px;height:10px;border-radius:3px;background:#6d88c9}
.mixture-label{font-family:'DM Sans',sans-serif;font-size:10px;font-weight:700}
</style>

<style scoped>
.expert-ice{color:#4263eb;display:inline-block;margin-right:7px}
</style>

<style scoped>
.sft-weight-row>div,.sft-weight-row b{font-weight:800;font-variant-numeric:tabular-nums}
.router-fire{font-size:18px;line-height:1}
</style>

<style scoped>
.routing-weight-labels{position:absolute;left:397px;top:256px;width:74px;display:flex;justify-content:space-between;font-size:17px;color:#111;pointer-events:none}
</style>

<style scoped>
.sft-target>span:first-child{font-family:'DM Sans',sans-serif;font-size:11px;line-height:1.4}
.sft-target>.math-tex-inline{font-size:17px}
</style>

<style scoped>
.sft-distribution{height:202px}
.sft-distribution>svg{height:100px}
.sft-objective{height:88px}
.routing-weight-labels{top:246px}
</style>

<style scoped>
.sft-target{height:88px;padding:10px}
.sft-target>span:first-child{font-family:Manrope,sans-serif;font-size:17px;font-weight:800;line-height:1.3;color:#17233e;margin-bottom:7px}
.sft-objective{top:140px}
</style>

<style scoped>
.sft-objective{top:150px}
</style>

<style scoped>
.sft-target>span:first-child{margin-bottom:3px}
</style>
