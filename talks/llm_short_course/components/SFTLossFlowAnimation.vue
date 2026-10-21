<script setup>
const slots = [
  { input: 'User:', label: '-100', role: 'prompt', loss: 'ignore' },
  { input: 'Explain', label: '-100', role: 'prompt', loss: 'ignore' },
  { input: 'gravity.', label: '-100', role: 'prompt', loss: 'ignore' },
  { input: 'Assistant:', label: 'Gravity', role: 'prompt', loss: 'train', pulse: 0 },
  { input: 'Gravity', label: 'pulls', role: 'assistant', loss: 'train', pulse: 1 },
  { input: 'pulls', label: 'objects', role: 'assistant', loss: 'train', pulse: 2 },
  { input: 'objects', label: 'together.', role: 'assistant', loss: 'train', pulse: 3 },
  { input: 'together.', label: '', role: 'assistant', loss: 'drop' },
]

const vocabRows = ['Gravity', 'pulls', 'objects', 'together.', '<other>']
</script>

<template>
  <div class="sft-loss-sketch">
    <div class="label input-title">input_ids</div>

    <div class="input-row">
      <div
        v-for="(slot, index) in slots"
        :key="`input-${slot.input}-${index}`"
        class="token input-token"
        :class="[slot.role, slot.loss === 'train' ? `pulse-${slot.pulse}` : '']"
      >
        {{ slot.input }}
      </div>
    </div>

    <div class="arrow arrow-input"></div>
    <div class="model-box">Model</div>
    <div class="arrow arrow-model"></div>

    <div class="label logits-title">logits</div>
    <div class="vocab-size">vocab size</div>
    <div class="vocab-axis"></div>

    <div class="logits-grid">
      <template v-for="row in vocabRows" :key="row">
        <div
          v-for="(slot, col) in slots"
          :key="`${row}-${col}`"
          class="logit-cell"
          :class="[slot.loss, slot.loss === 'train' ? `pulse-${slot.pulse}` : '']"
        ></div>
      </template>
    </div>

    <div class="label labels-title">labels</div>
    <div class="label labels-subtitle">(next token targets)</div>

    <div class="label-row">
      <div
        v-for="(slot, index) in slots"
        :key="`label-${slot.label}-${index}`"
        class="token label-token"
        :class="[slot.loss, slot.loss === 'train' ? `pulse-${slot.pulse}` : '']"
      >
        {{ slot.label }}
      </div>
    </div>

    <svg class="loss-wires" viewBox="0 0 980 430" aria-hidden="true">
      <defs>
        <marker
          id="sft-wire-arrow"
          markerWidth="6"
          markerHeight="6"
          refX="0"
          refY="3"
          orient="auto"
          markerUnits="strokeWidth"
        >
          <path d="M 0 0 L 6 3 L 0 6 Z" />
        </marker>
      </defs>
      <path
        class="wire"
        d="M 570 259 C 563 259 581 263 670 250"
        marker-end="url(#sft-wire-arrow)"
      />
      <path
        class="wire"
        d="M 560 386 C 590 374 618 340 670 310"
        marker-end="url(#sft-wire-arrow)"
      />
    </svg>

    <div class="ce-diamond">
      <span>cross</span>
      <span>entropy</span>
      <span>loss</span>
    </div>

    <div class="loss-arrow"></div>
    <div class="label loss-title">loss</div>
    <div class="loss-square"></div>

  </div>
</template>

<style scoped>
.sft-loss-sketch {
  position: relative;
  box-sizing: border-box;
  width: 100%;
  max-width: 980px;
  height: 430px;
  margin: 12px auto 0;
  background: #ffffff;
  color: #202124;
  overflow: hidden;
  font-family: "Inter", "Noto Sans SC", sans-serif;
  --flow-left: 142px;
  --col-w: 44px;
  --col-gap: 6px;
}

.label {
  position: absolute;
  font-family: "Comic Sans MS", "Marker Felt", "Bradley Hand", "Inter", sans-serif;
  font-weight: 900;
  letter-spacing: 0;
  line-height: 1;
}

.input-title {
  left: 20px;
  top: 12px;
  color: #1976d2;
  font-size: 24px;
}

.logits-title {
  left: 20px;
  top: 226px;
  color: #f59e0b;
  font-size: 24px;
}

.labels-title {
  left: 20px;
  bottom: 48px;
  color: #1976d2;
  font-size: 24px;
}

.labels-subtitle {
  left: 20px;
  bottom: 31px;
  color: #1976d2;
  font-size: 12px;
}

.loss-title {
  left: 764px;
  top: 211px;
  color: #16a34a;
  font-size: 28px;
}

.input-row,
.label-row {
  position: absolute;
  display: grid;
  grid-template-columns: repeat(8, var(--col-w));
  gap: var(--col-gap);
}

.input-row {
  left: var(--flow-left);
  top: 8px;
}

.label-row {
  left: var(--flow-left);
  bottom: 28px;
}

.token {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 31px;
  border: 4px solid #202124;
  border-radius: 8px;
  color: #202124;
  font-size: 7.5px;
  line-height: 1;
  font-weight: 900;
  overflow: hidden;
  text-align: center;
}

.input-token {
  background: #9fd2f6;
}

.input-token.assistant {
  background: #b8ead0;
}

.label-token {
  background: #9fd2f6;
}

.label-token.ignore {
  color: #94a3b8;
  border-color: #9fd2f6;
  background:
    repeating-linear-gradient(135deg, rgba(159, 210, 246, .08), rgba(159, 210, 246, .08) 7px, rgba(159, 210, 246, .55) 7px, rgba(159, 210, 246, .55) 10px),
    #ffffff;
}

.label-token.train {
  background: #b8ead0;
}

.label-token.drop {
  color: transparent;
  border-color: #9fd2f6;
  background:
    repeating-linear-gradient(135deg, rgba(159, 210, 246, .08), rgba(159, 210, 246, .08) 7px, rgba(159, 210, 246, .55) 7px, rgba(159, 210, 246, .55) 10px),
    #ffffff;
}

.arrow {
  position: absolute;
  width: 4px;
  background: #202124;
}

.arrow::after {
  content: "";
  position: absolute;
  left: -8px;
  bottom: -2px;
  width: 18px;
  height: 18px;
  border-right: 4px solid #202124;
  border-bottom: 4px solid #202124;
  transform: rotate(45deg);
}

.arrow-input {
  left: 339px;
  top: 40px;
  height: 31px;
  animation: arrowNudge 1.4s ease-in-out infinite;
}

.arrow-model {
  left: 339px;
  top: 145px;
  height: 31px;
  animation: arrowNudge 1.4s ease-in-out infinite .25s;
}

.model-box {
  position: absolute;
  left: 124px;
  top: 86px;
  width: 430px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 4px solid #202124;
  border-radius: 20px;
  background: #ffffff;
  color: #202124;
  font-family: "Comic Sans MS", "Marker Felt", "Bradley Hand", "Inter", sans-serif;
  font-size: 30px;
  font-weight: 900;
}

.vocab-axis {
  position: absolute;
  left: 124px;
  top: 184px;
  width: 3px;
  height: 149px;
  background: #202124;
}

.vocab-axis::before,
.vocab-axis::after {
  content: "";
  position: absolute;
  left: -8px;
  width: 18px;
  height: 18px;
  border-left: 3px solid #202124;
  border-top: 3px solid #202124;
}

.vocab-axis::before {
  top: -1px;
  transform: rotate(45deg);
}

.vocab-axis::after {
  bottom: -1px;
  transform: rotate(225deg);
}

.vocab-size {
  position: absolute;
  left: 50px;
  top: 253px;
  color: #202124;
  font-family: "Comic Sans MS", "Marker Felt", "Bradley Hand", "Inter", sans-serif;
  font-size: 14px;
  font-weight: 900;
  white-space: nowrap;
}

.logits-grid {
  position: absolute;
  left: var(--flow-left);
  top: 184px;
  display: grid;
  grid-template-columns: repeat(8, var(--col-w));
  grid-template-rows: repeat(5, 24px);
  gap: var(--col-gap);
}

.logit-cell {
  border: 4px solid #202124;
  border-radius: 7px;
  background: #fed7a6;
}

.logit-cell.ignore {
  opacity: .55;
  background: #f3f4f6;
}

.logit-cell.train {
  background: #fed7a6;
}

.logit-cell.drop {
  opacity: .9;
  border: 3px dashed #fbbf24;
  background:
    repeating-linear-gradient(135deg, rgba(251, 191, 36, .08), rgba(251, 191, 36, .08) 7px, rgba(251, 191, 36, .6) 7px, rgba(251, 191, 36, .6) 10px),
    #fffaf0;
}

.loss-wires {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: visible;
}

.wire {
  fill: none;
  stroke: #202124;
  stroke-width: 3.2;
  stroke-linecap: round;
  stroke-linejoin: round;
  marker-end: url(#sft-wire-arrow);
}

.loss-wires marker path {
  fill: #202124;
}

.ce-diamond {
  position: absolute;
  left: 620px;
  top: 220px;
  width: 90px;
  height: 90px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 4px solid #202124;
  border-radius: 20px;
  background: #aef0bd;
  transform: rotate(45deg);
  animation: cePulse 1.8s ease-in-out infinite;
}

.ce-diamond span {
  display: block;
  color: #202124;
  font-family: "Comic Sans MS", "Marker Felt", "Bradley Hand", "Inter", sans-serif;
  font-size: 15px;
  line-height: 1.03;
  font-weight: 900;
  transform: rotate(-45deg);
}

.loss-arrow {
  position: absolute;
  left: 738px;
  top: 266px;
  width: 30px;
  height: 4px;
  background: #202124;
}

.loss-arrow::after {
  content: "";
  position: absolute;
  right: -2px;
  top: -5px;
  width: 14px;
  height: 14px;
  border-right: 4px solid #202124;
  border-top: 4px solid #202124;
  transform: rotate(45deg);
}

.loss-square {
  position: absolute;
  left: 778px;
  top: 249px;
  width: 31px;
  height: 31px;
  border: 4px solid #202124;
  border-radius: 8px;
  background: #aef0bd;
}

.pulse-0 { --delay: 0s; }
.pulse-1 { --delay: 1.05s; }
.pulse-2 { --delay: 2.1s; }
.pulse-3 { --delay: 3.15s; }

.input-token.pulse-0,
.input-token.pulse-1,
.input-token.pulse-2,
.input-token.pulse-3,
.label-token.pulse-0,
.label-token.pulse-1,
.label-token.pulse-2,
.label-token.pulse-3 {
  animation: tokenGlow 5.3s ease-in-out infinite;
  animation-delay: var(--delay);
}

.logit-cell.pulse-0,
.logit-cell.pulse-1,
.logit-cell.pulse-2,
.logit-cell.pulse-3 {
  animation: cellGlow 5.3s ease-in-out infinite;
  animation-delay: var(--delay);
}

@keyframes tokenGlow {
  0%, 18%, 100% {
    transform: translateY(0);
    box-shadow: 0 1px 0 rgba(0, 0, 0, .18);
  }
  6%, 11% {
    transform: translateY(-5px);
    box-shadow: 0 0 0 8px rgba(34, 197, 94, .24);
  }
}

@keyframes cellGlow {
  0%, 18%, 100% {
    transform: scale(1);
    box-shadow: none;
  }
  6%, 11% {
    transform: scale(1.08);
    box-shadow: 0 0 0 8px rgba(251, 191, 36, .28);
  }
}

@keyframes cePulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, .22); }
  50% { box-shadow: 0 0 0 10px rgba(34, 197, 94, .16); }
}

@keyframes arrowNudge {
  0%, 100% { transform: translateY(-2px); opacity: .7; }
  50% { transform: translateY(4px); opacity: 1; }
}
</style>
