<script setup>
defineProps({ active: { type: String, default: 'ci' } })

// Schematic repeated samples: two intervals cover the same fixed mean, one misses.
const ciSamples = [
  { id: 1, y: 58, estimate: 230, lower: 155, upper: 305, covers: true },
  { id: 2, y: 106, estimate: 280, lower: 220, upper: 340, covers: true },
  { id: 3, y: 154, estimate: 170, lower: 126, upper: 214, covers: false },
]

const tableRows = [0, 1, 2]
const tableCells = [0, 1, 2, 3]
</script>

<template>
  <nav class="background-agenda-visual" aria-label="Background topics">
    <a href="#/confidence-intervals" class="agenda-topic" :class="{ selected: active === 'ci' }" :aria-current="active === 'ci' ? 'step' : undefined">
      <div class="topic-index"><span>01</span><span class="topic-progress"></span></div>
      <h2>CI construction</h2>

      <svg class="topic-illustration ci-illustration" viewBox="0 0 400 205" role="img" aria-label="Three confidence intervals surround different estimates. The ground truth stays fixed. Two illustrative intervals cover it, and one misses it.">
        <text class="truth-label" x="250" y="19" text-anchor="middle">Ground truth</text>
        <line x1="250" y1="30" x2="250" y2="174" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3 5" opacity=".6" />

        <g v-for="sample in ciSamples" :key="sample.id" class="ci-trial" :class="`trial-${sample.id}`" :style="{ color: sample.covers ? 'var(--topic-color)' : '#b27a46' }">
          <text class="sample-label" x="5" :y="sample.y + 4">Interval {{ sample.id }}</text>
          <path :d="`M 80 ${sample.y} H 105 M 100 ${sample.y - 4} L 105 ${sample.y} L 100 ${sample.y + 4}`" fill="none" stroke="#9ba9bf" stroke-width="1.2" stroke-linecap="round" />
          <g :transform="`translate(${sample.estimate} ${sample.y})`">
            <g class="ci-span">
              <rect :x="sample.lower - sample.estimate" y="-9" :width="sample.upper - sample.lower" height="18" rx="9" fill="currentColor" opacity=".09" />
              <path :d="`M ${sample.lower - sample.estimate} 0 H ${sample.upper - sample.estimate} M ${sample.lower - sample.estimate} -6 V 6 M ${sample.upper - sample.estimate} -6 V 6`" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" vector-effect="non-scaling-stroke" />
            </g>
            <circle r="5" fill="currentColor" stroke="#fbfcff" stroke-width="1.5" />
          </g>
        </g>

        <g class="illustration-key" fill="currentColor">
          <path d="M 87 195 H 111" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" />
          <text x="121" y="199">Covers</text>
          <path d="M 233 195 H 257" stroke="#b27a46" stroke-width="2.5" stroke-linecap="round" />
          <text x="267" y="199" fill="#b27a46">Misses</text>
        </g>
      </svg>
    </a>


    <a href="#/foundation-models" class="agenda-topic" :class="{ selected: active === 'tfm' }" :aria-current="active === 'tfm' ? 'step' : undefined">
      <div class="topic-index"><span>02</span><span class="topic-progress"></span></div>
      <h2>Tabular foundation models</h2>

      <svg class="topic-illustration model-illustration" viewBox="0 0 400 205" role="img" aria-label="A dataset flows through a model to produce predictions">
        <g class="table" v-for="(y, i) in [77]" :key="y" :transform="`translate(31 ${y})`">
          <rect width="66" height="44" rx="6" fill="#fbfcff" stroke="currentColor" stroke-width="1.3" opacity=".65" />
          <rect x="5" y="5" width="56" height="7" rx="2" fill="currentColor" opacity=".24" />
          <g v-for="row in tableRows" :key="row">
            <rect v-for="col in tableCells" :key="col" :x="6 + col * 14" :y="16 + row * 8" width="11" height="4.5" rx="1.2" fill="currentColor" :opacity=".10 + ((row + col + i) % 3) * .12" />
          </g>
        </g>

        <g fill="none" stroke="currentColor" stroke-width="1.5" opacity=".3">
          <path d="M 98 99 H 165 M 159 94 L 165 99 L 159 104" />
          <path d="M 258 99 H 302 M 296 94 L 302 99 L 296 104" />
        </g>
        <g class="flow-dots" fill="currentColor">

          <circle class="flow-dot dot-two" r="3.2" />

        </g>

        <rect class="model-halo" x="153" y="50" width="117" height="98" rx="25" fill="currentColor" opacity=".04" />
        <rect x="165" y="61" width="93" height="76" rx="15" fill="#fbfcff" stroke="currentColor" stroke-width="1.8" />
        <rect x="165" y="61" width="93" height="76" rx="15" fill="currentColor" opacity=".06" />
        <g stroke="currentColor" stroke-width="1" opacity=".33" fill="none">
          <path d="M 185 82 L 211 86 L 237 82 M 185 82 L 211 112 L 237 82 M 185 116 L 211 86 L 237 116 M 185 116 L 211 112 L 237 116" />
        </g>
        <g fill="currentColor">
          <circle cx="185" cy="82" r="4" /><circle cx="185" cy="116" r="4" />
          <circle cx="211" cy="86" r="4" /><circle cx="211" cy="112" r="4" />
          <circle cx="237" cy="82" r="4" /><circle cx="237" cy="116" r="4" />
        </g>

        <g class="prediction" transform="translate(315 76)">
          <rect width="53" height="46" rx="9" fill="currentColor" opacity=".09" />
          <path d="M 12 32 V 26 M 26 32 V 14 M 40 32 V 21" stroke="currentColor" stroke-width="5" stroke-linecap="round" fill="none" />
        </g>
        <g class="illustration-key" fill="currentColor" font-family="DM Sans, sans-serif" font-size="11" text-anchor="middle">
          <text x="64" y="198">Dataset</text><text x="211" y="198">Model</text><text x="341" y="198">Predictions</text>
        </g>
      </svg>
    </a>

  </nav>
</template>

<style scoped>
.background-agenda-visual{display:grid;grid-template-columns:1fr 1fr;gap:72px;position:relative;margin-top:38px}
.background-agenda-visual::after{content:'';position:absolute;left:50%;top:0;bottom:0;width:1px;background:linear-gradient(transparent,#dfe5ef 14%,#dfe5ef 84%,transparent)}
.agenda-topic{--topic-color:#a1adbf;display:block;border:0!important;color:var(--topic-color);text-decoration:none!important;outline-offset:12px;transition:color .3s}
.agenda-topic.selected{--topic-color:#4263eb}
.topic-index{display:flex;gap:13px;align-items:center;color:var(--topic-color);font-size:14px;font-weight:700;letter-spacing:.05em}
.topic-index>span:first-child{font-family:Manrope,sans-serif;font-size:18px;font-weight:800;letter-spacing:-.4px}
.topic-progress{height:2px;flex:1;background:currentColor;opacity:.25}
.selected .topic-progress{opacity:.65}
.agenda-topic h2{font-family:Manrope,sans-serif;font-size:28px;line-height:1.2;font-weight:800;letter-spacing:-.7px;margin:20px 0 24px;white-space:nowrap;color:#7a889e}
.agenda-topic.selected h2{color:#17233e}
.topic-illustration{display:block;width:100%;height:230px;overflow:visible;color:var(--topic-color)}
.illustration-key{opacity:.8}
.topic-illustration text{font-size:12px!important;font-family:DM Sans,sans-serif!important;font-weight:500!important}
.agenda-topic p{font-size:14.5px;line-height:1.4!important;color:#8996aa;margin:20px 0 17px;white-space:nowrap;letter-spacing:-.2px}
.agenda-topic.selected p{color:#53637c}
.topic-bottom{display:flex;justify-content:space-between;align-items:center;border-top:1px solid #e1e6ef;padding-top:11px;font-size:10px;font-weight:600;letter-spacing:.035em;color:#9ba7b9}
.selected .topic-bottom{color:#4263eb}
.topic-arrow{font-size:16px;font-weight:400;line-height:1}
.truth-label{fill:#64748b}
.sample-label{fill:#64748b}
.ci-trial{animation-duration:6s;animation-timing-function:ease;animation-iteration-count:infinite}
.trial-1{animation-name:trialOne}
.trial-2{animation-name:trialTwo}
.trial-3{animation-name:trialThree}
.ci-span{transform-origin:0 0;animation-duration:6s;animation-timing-function:ease-out;animation-iteration-count:infinite}
.trial-1 .ci-span{animation-name:spanOne}
.trial-2 .ci-span{animation-name:spanTwo}
.trial-3 .ci-span{animation-name:spanThree}
.agenda-topic:not(.selected) .ci-trial,.agenda-topic:not(.selected) .ci-span{animation:none}
.flow-dot{opacity:0;offset-distance:0%;animation:tableFlow 5.8s linear infinite paused}
.dot-one{offset-path:path('M 98 41 C 128 41 128 99 165 99');animation-delay:0s}
.dot-two{offset-path:path('M 98 99 H 165');animation-delay:.8s}
.dot-three{offset-path:path('M 98 157 C 128 157 128 99 165 99');animation-delay:1.6s}
.selected .flow-dot{animation-play-state:running}
.model-halo{transform-origin:211px 99px;animation:modelPulse 5.8s ease-in-out infinite paused}
.selected .model-halo{animation-play-state:running}
.prediction{animation:predictionPulse 5.8s ease-in-out infinite paused}
.selected .prediction{animation-play-state:running}
@keyframes trialOne{0%{opacity:0}5%,87%{opacity:1}95%,100%{opacity:0}}
@keyframes trialTwo{0%,22%{opacity:0}27%,87%{opacity:1}95%,100%{opacity:0}}
@keyframes trialThree{0%,44%{opacity:0}49%,87%{opacity:1}95%,100%{opacity:0}}
@keyframes spanOne{0%,7%{transform:scaleX(0)}16%,100%{transform:scaleX(1)}}
@keyframes spanTwo{0%,29%{transform:scaleX(0)}38%,100%{transform:scaleX(1)}}
@keyframes spanThree{0%,51%{transform:scaleX(0)}60%,100%{transform:scaleX(1)}}
@keyframes tableFlow{0%{offset-distance:0%;opacity:0}7%{opacity:.85}34%{offset-distance:100%;opacity:.85}40%,100%{offset-distance:100%;opacity:0}}
@keyframes modelPulse{0%,35%,80%,100%{opacity:.04;transform:scale(1)}55%{opacity:.14;transform:scale(1.045)}}
@keyframes predictionPulse{0%,45%,100%{opacity:.6}65%,80%{opacity:1}}
@media(prefers-reduced-motion:reduce){.ci-trial,.ci-span,.flow-dot,.model-halo,.prediction{animation:none!important}.flow-dot{display:none}}
</style>
