<script setup>
import MathTex from './MathTex.vue'

// Illustrative score distribution; cutoffs interpolate its cumulative bin counts.
const counts = [1, 2, 3, 5, 7, 9, 12, 14, 12, 10, 7, 4, 2, 1]
const plotLeft = 24
const binWidth = 40
const total = counts.reduce((sum, count) => sum + count, 0)
function quantileX(probability) {
  let cumulative = 0
  for (let i = 0; i < counts.length; i++) {
    if (cumulative + counts[i] >= probability * total)
      return plotLeft + binWidth * (i + (probability * total - cumulative) / counts[i])
    cumulative += counts[i]
  }
  return plotLeft + counts.length * binWidth
}
const lowerCutoff = quantileX(1 / 3)
const upperCutoff = quantileX(2 / 3)
</script>

<template>
  <div class="threshold-calibration">
    <section class="score-definition">
      <div class="score-equation">
        <span class="step-label">Step 1. Score each DGP</span>
        <div class="score-math"><MathTex tex="S=\sum_j\lambda_j\left[C_{\alpha_j}-(1-\alpha_j)\right]" /></div>
        <p>Observed coverage minus target coverage, averaged over significance levels &amp; datasets from the same DGP.</p>
      </div>
      <div class="score-legend">
        <div><MathTex tex="C_{\alpha_j}" /><span>Coverage across this dataset's query points</span></div>
        <div><MathTex tex="1-\alpha_j" /><span>Target coverage</span></div>
        <div><MathTex tex="\lambda_j" /><span>Nonnegative weights summing to 1</span></div>
        <small>Levels used: 50%, 80%, 90%, 95%.</small>
      </div>
    </section>

    <section class="quantile-step reveal">
      <span class="step-label">Step 2. Compute the two empirical quantiles of all scores</span>
      <div class="cutoff-row">
      <div class="fixed-cutoffs">
        <div class="lower"><MathTex tex="s_1=Q_{1/3}(S)" /></div>
        <div class="upper"><MathTex tex="s_2=Q_{2/3}(S)" /></div>
      </div>
      <div class="score-distribution reveal">
        <div class="score-chart">
          <svg preserveAspectRatio="none" viewBox="0 0 620 164" aria-label="Illustrative distribution of coverage scores with one-third and two-thirds quantile cutoffs">
            <defs>
              <clipPath id="score-low-region"><rect x="0" y="0" :width="lowerCutoff" height="120" /></clipPath>
              <clipPath id="score-high-region"><rect :x="upperCutoff" y="0" :width="620-upperCutoff" height="120" /></clipPath>
            </defs>
            <g fill="#c3cee2"><rect v-for="(count,i) in counts" :key="i" :x="plotLeft+i*binWidth+4" :y="112-count*5" width="32" :height="count*5" rx="3" /></g>
            <g class="reveal">
              <g fill="#9b7bd4" clip-path="url(#score-low-region)"><rect v-for="(count,i) in counts" :key="i" :x="plotLeft+i*binWidth+4" :y="112-count*5" width="32" :height="count*5" rx="3" /></g>
              <g fill="#67b6ae" clip-path="url(#score-high-region)"><rect v-for="(count,i) in counts" :key="i" :x="plotLeft+i*binWidth+4" :y="112-count*5" width="32" :height="count*5" rx="3" /></g>
              <path :d="`M${lowerCutoff} 20V121`" stroke="#7c4dce" stroke-width="2" stroke-dasharray="4 4" />
              <path :d="`M${upperCutoff} 20V121`" stroke="#0b9687" stroke-width="2" stroke-dasharray="4 4" />
            </g>
            <path d="M22 113H596" stroke="#a8b5cc" stroke-width="1.5" />
          </svg>
          <div class="cutoff-marker lower reveal" :style="{left:`${lowerCutoff/620*100}%`}"><MathTex tex="s_1" /><span>1/3 quantile</span></div>
          <div class="cutoff-marker upper reveal" :style="{left:`${upperCutoff/620*100}%`}"><MathTex tex="s_2" /><span>2/3 quantile</span></div>
          <span class="score-axis lower-score">Lower scores</span><span class="score-axis higher-score">Higher scores</span>
        </div>
      </div>
      </div>
    </section>

  </div>
</template>

<style scoped>
.threshold-calibration{width:876px;margin-top:18px}
.score-definition{display:grid;grid-template-columns:475px 1fr;gap:20px;background:#fff;border:1px solid #dfe6f3;border-radius:15px;padding:16px 20px}
.step-label{display:block;font-size:14px;line-height:1.4;font-weight:700;letter-spacing:.01em;color:#657896}
.score-math{font-size:27px;line-height:1.4;margin:8px 0 7px;color:#17233e}
.score-equation p{font-size:14px;line-height:1.45;margin:0;color:#697b98}
.score-legend{border-left:1px solid #d6dfef;padding:3px 0 0 17px;display:flex;flex-direction:column;gap:8px}
.score-legend>div{display:grid;grid-template-columns:68px 1fr;gap:8px;align-items:center;font-size:16px;color:#4263eb}
.score-legend>div>span:last-child{font-size:13px;line-height:1.4;color:#697b98}
.score-legend small{font-size:12px;line-height:1.4;color:#8490a7;margin-top:1px}
.quantile-step{box-sizing:border-box;margin-top:16px;padding:16px 20px;background:#fff;border:1px solid #dfe6f3;border-radius:15px}
.quantile-step>.step-label{white-space:nowrap}
.cutoff-row{display:grid;grid-template-columns:220px minmax(0,1fr);gap:24px;margin-top:8px;align-items:center}
.score-distribution{min-width:0}
.score-distribution>.step-label{padding-left:2px}
.score-chart{position:relative;width:100%;height:164px;margin-top:1px}
.score-chart svg{position:absolute;inset:0;width:100%;height:164px}
.cutoff-marker{position:absolute;top:121px;transform:translateX(-50%);text-align:center;font-size:18px;line-height:1.2;transition:opacity .5s ease}
.cutoff-marker.waiting{transform:translateX(-50%);opacity:0}
.cutoff-marker>span:last-child{display:block;margin-top:4px;font-size:12px;line-height:1.3;white-space:nowrap}
.lower{color:#7c4dce}.upper{color:#0b9687}
.score-axis{position:absolute;top:132px;font-size:12px;color:#8390a6}.lower-score{left:24px}.higher-score{right:24px}
.fixed-cutoffs{padding:0 10px}
.fixed-cutoffs>div{font-size:22px;margin-top:14px;line-height:1.4}
.fixed-cutoffs p{font-size:11px;line-height:1.5;color:#7c89a2;margin:12px 0 0}
.threshold-message{margin-top:15px;border-left:3px solid #4263eb;border-radius:0 9px 9px 0;background:#eef2ff;padding:11px 15px;color:#4263eb;font-size:15px;line-height:1.4}
</style>
