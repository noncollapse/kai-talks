<script setup>
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { useSlideContext } from '@slidev/client'

const { $clicks } = useSlideContext()
const activeStep = computed(() => Math.max(0, Math.min(3, $clicks.value)))

const genWords = [
  'A',
  'language',
  'model',
  'reads',
  'context,',
  'scores',
  'next-token',
  'probabilities,',
  'samples',
  'one,',
  'then',
  'repeats.',
]

const genCandidateSets = [
  [['A', 72], ['The', 18], ['This', 10]],
  [['language', 69], ['model', 20], ['system', 11]],
  [['model', 74], ['system', 17], ['assistant', 9]],
  [['reads', 67], ['predicts', 22], ['uses', 11]],
  [['context,', 71], ['text,', 19], ['prompts,', 10]],
  [['scores', 66], ['predicts', 23], ['computes', 11]],
  [['next-token', 73], ['token-level', 18], ['word', 9]],
  [['probabilities,', 76], ['logits,', 16], ['scores,', 8]],
  [['samples', 68], ['selects', 21], ['returns', 11]],
  [['one,', 70], ['a token,', 19], ['the best,', 11]],
  [['then', 65], ['and', 24], ['before', 11]],
  [['repeats.', 72], ['continues.', 18], ['stops.', 10]],
].map(candidates => candidates.map(([token, probability], index) => ({
  token,
  probability,
  selected: index === 0,
})))

const genVisibleCount = ref(0)
const genCandidateIndex = computed(() => Math.min(genVisibleCount.value, genCandidateSets.length - 1))
const genCandidates = computed(() => genCandidateSets[genCandidateIndex.value])
const predictedToken = computed(() => genWords[genCandidateIndex.value])
let genTimer

function clearGenTimer() {
  if (genTimer)
    clearTimeout(genTimer)
  genTimer = undefined
}

function runGenLoop(count = 0) {
  clearGenTimer()
  if (activeStep.value !== 1) {
    genVisibleCount.value = 0
    return
  }

  genVisibleCount.value = count

  if (count < genWords.length) {
    genTimer = setTimeout(() => runGenLoop(count + 1), 1000)
    return
  }

  genTimer = setTimeout(() => {
    genVisibleCount.value = 0
    genTimer = setTimeout(() => runGenLoop(1), 520)
  }, 1350)
}

watch(activeStep, (step) => {
  clearGenTimer()
  if (step === 1)
    runGenLoop(0)
  else
    genVisibleCount.value = 0
}, { immediate: true })

onBeforeUnmount(clearGenTimer)
</script>

<template>
  <div class="gpt-triptych" :class="`step-${activeStep}`">
    <div class="word-strip">
      <div class="word word-g">Generative</div>
      <div class="word word-p">Pre-trained</div>
      <div class="word word-t">Transformer</div>
    </div>

    <div class="rule"></div>

    <div class="columns">
      <section class="panel panel-g">
        <div class="gen-word-stream" aria-label="A language model reads context and generates one token at a time">
          <span
            v-for="(word, index) in genWords"
            :key="word"
            :class="{ visible: activeStep === 1 && index < genVisibleCount }"
          >{{ word }}</span>
        </div>
        <div class="gen-line">
          <span class="next-token-cue">next token <b aria-hidden="true">&rarr;</b></span>
          <span class="typing-token">{{ predictedToken }}</span>
        </div>
        <div class="prob-stack">
          <div
            v-for="(candidate, index) in genCandidates"
            :key="`${genCandidateIndex}-${index}-${candidate.token}`"
            :class="{ selected: candidate.selected }"
          >
            <b>{{ candidate.token }}</b>
            <i :style="{ '--w': `${candidate.probability}%` }"></i>
            <em>{{ candidate.probability }}%</em>
          </div>
        </div>
      </section>

      <section class="panel panel-p">
        <div class="corpus-card">
          <p class="corpus-line line-1">web pages, books, code, papers</p>
          <p class="corpus-line line-2">definitions, stories, proofs, forums</p>
          <p class="corpus-line line-3">question-answer traces, dialogs</p>
          <p class="corpus-line line-4">billions of tokens, one objective</p>
        </div>
        <div class="down-arrow"></div>
        <div class="weight-grid" aria-hidden="true">
          <span v-for="i in 48" :key="i"></span>
        </div>
        <div class="caption">broad text -> reusable weights</div>
      </section>

      <section class="panel panel-t">
        <div class="token-rail">
          <span>The</span>
          <span>cat</span>
          <span>sat</span>
          <span>on</span>
          <span>the</span>
          <span class="next-token">?</span>
        </div>

        <div class="transformer-stack" aria-hidden="true">
          <div class="layer layer-1">
            <div class="matrix"></div>
            <div class="attention-arc arc-1"></div>
            <div class="attention-arc arc-2"></div>
          </div>
          <div class="layer layer-2">
            <div class="matrix"></div>
          </div>
          <div class="layer layer-3">
            <div class="matrix"></div>
          </div>
          <div class="layer layer-4">
            <div class="matrix"></div>
          </div>
        </div>
        <div class="caption">causal attention mixes the past</div>
      </section>
    </div>

    <div class="bottom-line">
      GPT = a model that generates text, after pre-training, using a Transformer.
    </div>
  </div>
</template>

<style scoped>
:global(.slidev-layout.full:has(.gpt-triptych)) {
  padding: 0 !important;
}

.gpt-triptych {
  box-sizing: border-box;
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 18px 24px 16px;
  border-radius: 0;
  overflow: hidden;
  background:
    radial-gradient(circle at 88% 90%, rgba(124, 58, 237, .08), transparent 12%),
    linear-gradient(180deg, #ffffff, #f8fafc);
  color: #0f172a;
  box-shadow: inset 0 0 0 1px #e5e7eb;
}

.word-strip {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  align-items: end;
  height: 78px;
}

.word {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 36px;
  line-height: 1;
  color: #7c8da3;
  text-align: center;
  white-space: nowrap;
  text-shadow: none;
  transition: color .28s ease, text-shadow .28s ease, transform .28s ease;
}

.step-1 .word-g {
  color: #16a34a;
  text-shadow: 0 0 18px rgba(22, 163, 74, .18);
  transform: translateY(-2px);
}

.step-2 .word-p {
  color: #0284c7;
  text-shadow: 0 0 18px rgba(14, 165, 233, .18);
  transform: translateY(-2px);
}

.step-3 .word-t {
  color: #7c3aed;
  text-shadow: 0 0 18px rgba(124, 58, 237, .18);
  transform: translateY(-2px);
}

.rule {
  height: 2px;
  margin-top: 8px;
  background: linear-gradient(90deg, transparent, #94a3b8 10%, #94a3b8 90%, transparent);
}

.columns {
  position: relative;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  height: 372px;
}

.columns::before,
.columns::after {
  content: "";
  position: absolute;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(180deg, #94a3b8, rgba(148, 163, 184, .3));
}

.columns::before { left: 33.333%; }
.columns::after { left: 66.666%; }

.panel {
  position: relative;
  padding: 18px 24px;
  opacity: .4;
  filter: grayscale(.34);
  transition: opacity .28s ease, filter .28s ease;
}

.step-1 .panel-g,
.step-2 .panel-p,
.step-3 .panel-t {
  opacity: 1;
  filter: grayscale(0);
}

.gen-word-stream {
  display: flex;
  flex-wrap: wrap;
  align-content: flex-start;
  gap: 7px 8px;
  min-height: 118px;
  padding-right: 4px;
}

.gen-word-stream span {
  display: inline-flex;
  align-items: center;
  height: 23px;
  padding: 0 8px;
  border: 1px solid rgba(148, 163, 184, .55);
  border-radius: 5px;
  color: #334155;
  background: rgba(236, 242, 248, .98);
  font-size: 11px;
  font-weight: 800;
  opacity: .4;
  transform: translateY(6px);
  transition:
    opacity .22s ease,
    transform .22s ease,
    color .22s ease,
    border-color .22s ease,
    box-shadow .22s ease;
}

.step-1 .gen-word-stream span.visible {
  opacity: 1;
  transform: translateY(0);
  color: #166534;
  background: #ecfdf5;
  border-color: rgba(34, 197, 94, .62);
  box-shadow: 0 0 14px rgba(34, 197, 94, .18);
}

.gen-line {
  position: absolute;
  left: 24px;
  right: 24px;
  bottom: 88px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.typing-token,
.token-rail span {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 40px;
  height: 24px;
  padding: 0 8px;
  border: 1px solid #cbd5e1;
  border-radius: 5px;
  color: #334155;
  background: #e9eef5;
  font-size: 12px;
  font-weight: 800;
}

.next-token-cue {
  color: #64748b;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: .08em;
  text-transform: uppercase;
}

.next-token-cue b {
  display: inline-block;
  margin-left: 5px;
  color: #16a34a;
  font-size: 15px;
  line-height: 1;
}

.typing-token {
  color: #166534 !important;
  background: #dcfce7 !important;
  border-color: #22c55e !important;
  box-shadow: 0 0 18px rgba(34, 197, 94, .18);
}

.step-1 .typing-token {
  animation: typeBlink 1s steps(1) infinite;
}

.prob-stack {
  position: absolute;
  left: 24px;
  right: 24px;
  bottom: 12px;
}

.prob-stack div {
  display: grid;
  grid-template-columns: 86px 1fr 34px;
  gap: 8px;
  align-items: center;
  margin-top: 7px;
}

.prob-stack b {
  overflow: hidden;
  color: #64748b;
  font-size: 11px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.prob-stack i {
  height: 8px;
  width: var(--w);
  border-radius: 99px;
  background: #cbd5e1;
  transform-origin: left center;
}

.prob-stack em {
  color: #64748b;
  font-size: 10px;
  font-style: normal;
  text-align: right;
}

.prob-stack div.selected b,
.prob-stack div.selected em {
  color: #15803d;
  font-weight: 800;
}

.prob-stack div.selected i {
  background: #22c55e;
}

.step-1 .prob-stack i {
  animation: probabilityReveal .24s ease-out both;
}

.corpus-card {
  position: relative;
  width: 82%;
  height: 70px;
  margin: 4px auto 0;
  padding: 12px 16px;
  border: 1px solid rgba(96, 165, 250, .92);
  color: #1e40af;
  background: #dbeafe;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 13px;
  line-height: 1.35;
  opacity: .9;
  overflow: hidden;
}

.corpus-card p {
  position: absolute;
  left: 16px;
  right: 16px;
  top: 50%;
  margin: 0;
  opacity: 0;
  transform: translateY(-30%);
}

.corpus-card .line-1 {
  opacity: .8;
  transform: translateY(-50%);
}

.down-arrow {
  width: 0;
  height: 0;
  margin: 20px auto 12px;
  border-left: 14px solid transparent;
  border-right: 14px solid transparent;
  border-top: 34px solid #60a5fa;
  opacity: .35;
}

.step-2 .corpus-card {
  animation: corpusFrameGlow 4.8s ease-in-out infinite;
  opacity: 1;
}

.step-2 .corpus-line {
  animation: corpusTextSwap 4.8s ease-in-out infinite;
}

.step-2 .line-1 { animation-delay: 0s; }
.step-2 .line-2 { animation-delay: 1.2s; }
.step-2 .line-3 { animation-delay: 2.4s; }
.step-2 .line-4 { animation-delay: 3.6s; }

.step-2 .down-arrow {
  animation: arrowPulse 1.9s ease-in-out infinite;
}

.weight-grid {
  display: grid;
  grid-template-columns: repeat(8, 18px);
  gap: 9px;
  justify-content: center;
  width: max-content;
  margin: 0 auto;
  padding: 14px;
  border: 1px solid rgba(96, 165, 250, .92);
  background: #dbeafe;
}

.weight-grid span {
  width: 18px;
  height: 18px;
  border: 2px solid #93c5fd;
  border-top-color: #0369a1;
  border-radius: 999px;
}

.step-2 .weight-grid span {
  animation: dialSpin 1.9s ease-in-out infinite;
}

.weight-grid span:nth-child(3n) { animation-delay: .12s; }
.weight-grid span:nth-child(4n) { animation-delay: .22s; }
.weight-grid span:nth-child(5n) { animation-delay: .34s; }

.caption {
  margin-top: 10px;
  text-align: center;
  color: #334155;
  font-size: 12px;
  font-weight: 800;
}

.token-rail {
  display: flex;
  justify-content: center;
  gap: 7px;
  margin-top: 24px;
  transform: perspective(700px) rotateX(8deg);
}

.token-rail .next-token {
  color: #6d28d9;
  background: #f5f3ff;
  border-color: #8b5cf6;
}

.step-3 .token-rail .next-token {
  animation: questionGlow 1.6s ease-in-out infinite;
}

.transformer-stack {
  position: relative;
  width: 250px;
  height: 190px;
  margin: 18px auto 0;
  perspective: 760px;
}

.layer {
  position: absolute;
  left: 14px;
  right: 14px;
  height: 96px;
  border: 1px solid rgba(196, 181, 253, .75);
  background:
    linear-gradient(90deg, rgba(255, 255, 255, .9), rgba(245, 243, 255, .78)),
    #ede9fe;
  transform: skewY(-8deg) rotateX(58deg);
  box-shadow: 16px 24px 18px rgba(124, 58, 237, .12);
}

.layer-1 { bottom: 0; z-index: 4; }
.layer-2 { bottom: 24px; z-index: 3; opacity: .78; }
.layer-3 { bottom: 48px; z-index: 2; opacity: .58; }
.layer-4 { bottom: 72px; z-index: 1; opacity: .42; }

.step-3 .layer-1 { animation: layerLift1 1.8s ease-in-out infinite; }
.step-3 .layer-2 { animation: layerLift2 1.8s ease-in-out infinite; }
.step-3 .layer-3 { animation: layerLift3 1.8s ease-in-out infinite; }
.step-3 .layer-4 { animation: layerLift4 1.8s ease-in-out infinite; }

.matrix {
  width: 74%;
  height: 72%;
  margin: 14px auto 0;
  border: 1px solid rgba(124, 58, 237, .28);
  background-image:
    linear-gradient(rgba(124, 58, 237, .22) 1px, transparent 1px),
    linear-gradient(90deg, rgba(124, 58, 237, .22) 1px, transparent 1px);
  background-size: 16px 16px;
  opacity: .8;
}

.attention-arc {
  position: absolute;
  height: 44px;
  border: 2px solid rgba(124, 58, 237, .68);
  border-bottom: 0;
  border-radius: 80px 80px 0 0;
  opacity: 0;
}

.step-3 .attention-arc {
  animation: arcFlash 1.4s ease-in-out infinite;
}

.arc-1 {
  left: 34px;
  top: 18px;
  width: 104px;
}

.arc-2 {
  left: 78px;
  top: 28px;
  width: 124px;
  animation-delay: .2s;
}

.bottom-line {
  margin-top: 8px;
  color: #0f172a;
  font-size: 15px;
  text-align: center;
  font-weight: 800;
  opacity: .82;
}

@keyframes focusWordG {
  0%, 26% { color: #16a34a; text-shadow: 0 0 20px rgba(22, 163, 74, .18); }
  34%, 100% { color: #94a3b8; text-shadow: none; }
}

@keyframes focusWordP {
  0%, 30%, 66%, 100% { color: #94a3b8; text-shadow: none; }
  38%, 58% { color: #0284c7; text-shadow: 0 0 20px rgba(14, 165, 233, .18); }
}

@keyframes focusWordT {
  0%, 62% { color: #94a3b8; text-shadow: none; }
  72%, 100% { color: #7c3aed; text-shadow: 0 0 22px rgba(124, 58, 237, .18); }
}

@keyframes focusPanelG {
  0%, 28% { opacity: 1; filter: grayscale(0); }
  36%, 100% { opacity: .4; filter: grayscale(.28); }
}

@keyframes focusPanelP {
  0%, 32%, 66%, 100% { opacity: .4; filter: grayscale(.28); }
  40%, 58% { opacity: 1; filter: grayscale(0); }
}

@keyframes focusPanelT {
  0%, 64% { opacity: .4; filter: grayscale(.28); }
  74%, 100% { opacity: 1; filter: grayscale(0); }
}

@keyframes typeBlink {
  0%, 8%, 16%, 24%, 100% { opacity: 1; }
  12%, 20% { opacity: .38; }
}

@keyframes genWordAppear {
  0%, 8% {
    opacity: .05;
    transform: translateY(7px);
    color: #475569;
    border-color: rgba(148, 163, 184, .55);
    box-shadow: none;
  }
  18%, 70% {
    opacity: 1;
    transform: translateY(0);
    color: #166534;
    border-color: rgba(34, 197, 94, .62);
    box-shadow: 0 0 14px rgba(34, 197, 94, .18);
  }
  82%, 100% {
    opacity: .32;
    transform: translateY(6px);
    color: #475569;
    border-color: rgba(148, 163, 184, .55);
    box-shadow: none;
  }
}

@keyframes probabilityReveal {
  from { transform: scaleX(.08); opacity: .35; }
  to { transform: scaleX(1); opacity: 1; }
}

@keyframes corpusFrameGlow {
  0%, 100% {
    border-color: rgba(147, 197, 253, .78);
    box-shadow: none;
  }
  50% {
    border-color: rgba(14, 165, 233, .72);
    box-shadow: 0 0 22px rgba(14, 165, 233, .18);
  }
}

@keyframes corpusTextSwap {
  0% {
    opacity: 0;
    transform: translateY(-8%);
  }
  7%, 24% {
    opacity: 1;
    transform: translateY(-50%);
  }
  31%, 100% {
    opacity: 0;
    transform: translateY(-90%);
  }
}

@keyframes corpusDrop {
  0%, 34% { transform: translateY(-8px); opacity: .44; }
  44%, 58% { transform: translateY(0); opacity: 1; }
  68%, 100% { transform: translateY(-8px); opacity: .44; }
}

@keyframes arrowPulse {
  0%, 35%, 68%, 100% { opacity: .2; transform: translateY(-8px); }
  46%, 58% { opacity: .95; transform: translateY(0); }
}

@keyframes dialSpin {
  0%, 36% { transform: rotate(-25deg); opacity: .4; }
  48%, 60% { transform: rotate(165deg); opacity: 1; }
  70%, 100% { transform: rotate(40deg); opacity: .5; }
}

@keyframes questionGlow {
  0%, 64% { box-shadow: none; }
  76%, 100% { box-shadow: 0 0 22px rgba(124, 58, 237, .24); }
}

@keyframes layerLift1 {
  0%, 65% { transform: skewY(-8deg) rotateX(58deg) translateY(0); }
  78%, 100% { transform: skewY(-8deg) rotateX(58deg) translateY(-5px); }
}

@keyframes layerLift2 {
  0%, 67% { transform: skewY(-8deg) rotateX(58deg) translateY(0); }
  80%, 100% { transform: skewY(-8deg) rotateX(58deg) translateY(-8px); }
}

@keyframes layerLift3 {
  0%, 69% { transform: skewY(-8deg) rotateX(58deg) translateY(0); }
  82%, 100% { transform: skewY(-8deg) rotateX(58deg) translateY(-11px); }
}

@keyframes layerLift4 {
  0%, 71% { transform: skewY(-8deg) rotateX(58deg) translateY(0); }
  84%, 100% { transform: skewY(-8deg) rotateX(58deg) translateY(-14px); }
}

@keyframes arcFlash {
  0%, 70% { opacity: 0; transform: translateY(5px); }
  80%, 92% { opacity: .9; transform: translateY(0); }
  100% { opacity: 0; transform: translateY(-4px); }
}

@keyframes bottomGlow {
  0%, 74% { opacity: .75; }
  84%, 100% { opacity: 1; }
}

@media (prefers-reduced-motion: reduce) {
  .gpt-triptych *,
  .gpt-triptych *::before,
  .gpt-triptych *::after {
    animation: none !important;
  }

  .word-t,
  .panel-t {
    opacity: 1;
    filter: none;
    color: #7c3aed;
  }
}
</style>
