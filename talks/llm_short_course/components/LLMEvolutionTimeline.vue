<script setup>
import { computed } from 'vue'

const props = defineProps({
  step: {
    type: Number,
    default: 0,
  },
})

const milestones = [
  {
    year: '2017',
    title: 'Transformer',
    badge: 'architecture appears',
    note: 'Attention-only sequence modeling makes large-scale parallel pre-training practical.',
    why: 'The engine under most modern LLMs.',
    tone: 'green',
  },
  {
    year: '2018',
    title: 'GPT and BERT',
    badge: 'pre-training era',
    note: 'Generative pre-training and bidirectional pre-training turn unlabeled text into reusable language representations.',
    why: 'Pre-train once, adapt many times.',
    tone: 'blue',
  },
  {
    year: '2020',
    title: 'GPT-3',
    badge: 'prompting works',
    note: 'A 175B language model showed that tasks can be specified through prompts and examples, without task-specific fine-tuning.',
    why: 'Tasks move into the prompt.',
    tone: 'cyan',
  },
  {
    year: '2022',
    title: 'ChatGPT',
    badge: 'public breakthrough',
    note: 'RLHF and a dialogue interface turn LLMs from research artifacts into everyday assistants.',
    why: 'The iPhone moment for LLMs.',
    tone: 'purple',
  },
  {
    year: '2025',
    title: 'DeepSeek-R1',
    badge: 'open reasoning',
    note: 'An open-source reasoning model reaches o1-level performance on several math, code, and reasoning benchmarks.',
    why: 'Not the first reasoning model, but a turning point for open reasoning.',
    tone: 'amber',
  },
  {
    year: '2025',
    title: 'IMO Gold-Level AI',
    badge: 'competition-grade reasoning',
    note: 'Gemini Deep Think officially reaches gold-medal standard at the International Mathematical Olympiad.',
    why: 'Reasoning systems start to look like serious solvers.',
    tone: 'rose',
  },
]

const activeIndex = computed(() => {
  const index = Number.isFinite(props.step) ? Math.floor(props.step) : 0
  return Math.min(Math.max(index, 0), milestones.length - 1)
})

const activeMilestone = computed(() => milestones[activeIndex.value])
</script>

<template>
  <div class="llm-evolution">
    <header class="hero">
      <div>
        <div class="eyebrow">major milestones only</div>
        <h1>Evolution of LLMs</h1>
      </div>
      <div class="timeline-count">
        <span>{{ activeIndex + 1 }}</span>
        <small>/ {{ milestones.length }}</small>
      </div>
    </header>

    <main class="stage" :class="`tone-${activeMilestone.tone}`">
      <section class="spotlight">
        <div class="year">{{ activeMilestone.year }}</div>
        <div class="badge">{{ activeMilestone.badge }}</div>
        <h2>{{ activeMilestone.title }}</h2>
        <p>{{ activeMilestone.note }}</p>
        <div class="why">{{ activeMilestone.why }}</div>
      </section>

      <section class="orbit" aria-label="Major LLM milestones">
        <div
          v-for="(item, index) in milestones"
          :key="`${item.year}-${item.title}`"
          class="node"
          :class="[{ active: index === activeIndex, passed: index < activeIndex }, `tone-${item.tone}`]"
        >
          <span>{{ item.year }}</span>
          <b>{{ item.title }}</b>
        </div>
      </section>
    </main>

    <footer class="rail">
      <div
        v-for="(item, index) in milestones"
        :key="`rail-${item.year}`"
        class="tick"
        :class="{ active: index === activeIndex, passed: index < activeIndex }"
      >
        <span></span>
      </div>
      <div class="rail-fill" :style="{ width: `${(activeIndex / (milestones.length - 1)) * 100}%` }"></div>
    </footer>
  </div>
</template>

<style scoped>
:global(.slidev-layout.full:has(.llm-evolution)) {
  padding: 0 !important;
}

.llm-evolution {
  box-sizing: border-box;
  width: 100%;
  height: 100%;
  padding: 24px 34px 24px;
  background:
    linear-gradient(120deg, rgba(15, 23, 42, .035) 0 1px, transparent 1px 100%),
    linear-gradient(180deg, #ffffff, #f8fafc);
  background-size: 26px 26px, 100% 100%;
  color: #0f172a;
  overflow: hidden;
}

.hero {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18px;
}

.eyebrow {
  color: #64748b;
  font-size: 12px;
  font-weight: 900;
  letter-spacing: .14em;
  text-transform: uppercase;
}

h1 {
  margin: 4px 0 0;
  padding: 0;
  border: 0;
  color: #0f172a;
  font-size: 42px;
  line-height: 1;
  letter-spacing: 0;
}

.timeline-count {
  display: flex;
  align-items: baseline;
  gap: 4px;
  padding-top: 2px;
  color: #94a3b8;
  font-weight: 900;
}

.timeline-count span {
  color: #0f172a;
  font-size: 34px;
}

.timeline-count small {
  font-size: 15px;
}

.stage {
  display: grid;
  grid-template-columns: minmax(0, 1.04fr) minmax(0, .96fr);
  gap: 24px;
  align-items: stretch;
  margin-top: 22px;
}

.spotlight {
  position: relative;
  min-height: 258px;
  padding: 24px 26px;
  border: 2px solid var(--accent-soft);
  border-radius: 8px;
  background:
    radial-gradient(circle at 88% 18%, var(--accent-wash), transparent 36%),
    #ffffff;
  box-shadow: 0 18px 36px rgba(15, 23, 42, .1);
  overflow: hidden;
}

.spotlight::after {
  content: "";
  position: absolute;
  right: -34px;
  bottom: -54px;
  width: 190px;
  height: 190px;
  border: 28px solid var(--accent-soft);
  border-radius: 999px;
  opacity: .5;
  animation: breathe 2.2s ease-in-out infinite;
}

.year {
  color: var(--accent);
  font-size: 52px;
  line-height: .9;
  font-weight: 950;
}

.badge {
  display: inline-flex;
  align-items: center;
  height: 24px;
  margin-top: 14px;
  padding: 0 10px;
  border-radius: 999px;
  color: #ffffff;
  background: var(--accent);
  font-size: 11px;
  font-weight: 900;
  letter-spacing: .06em;
  text-transform: uppercase;
}

h2 {
  margin: 16px 0 0;
  color: #0f172a;
  font-size: 38px;
  line-height: 1;
  font-weight: 950;
  letter-spacing: 0;
}

p {
  position: relative;
  z-index: 1;
  max-width: 570px;
  margin: 16px 0 0;
  color: #334155;
  font-size: 18px;
  line-height: 1.28;
  font-weight: 700;
}

.why {
  position: relative;
  z-index: 1;
  display: inline-flex;
  margin-top: 18px;
  padding: 10px 12px;
  border-left: 6px solid var(--accent);
  border-radius: 8px;
  background: var(--accent-wash);
  color: var(--accent-dark);
  font-size: 15px;
  line-height: 1.15;
  font-weight: 950;
}

.orbit {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 11px;
}

.node {
  min-height: 76px;
  padding: 12px 13px;
  border: 1.5px solid #e2e8f0;
  border-radius: 8px;
  background: rgba(255, 255, 255, .9);
  color: #475569;
  text-align: left;
  opacity: .72;
  transform: translateY(0);
  transition:
    opacity .35s ease,
    transform .35s ease,
    border-color .35s ease,
    box-shadow .35s ease,
    background .35s ease;
}

.node span {
  display: block;
  color: var(--accent);
  font-size: 13px;
  line-height: 1;
  font-weight: 950;
}

.node b {
  display: block;
  margin-top: 8px;
  color: #0f172a;
  font-size: 15px;
  line-height: 1.05;
  font-weight: 950;
}

.node.active {
  opacity: 1;
  transform: translateY(-4px);
  border-color: var(--accent);
  background: linear-gradient(180deg, #ffffff, var(--accent-wash));
  box-shadow: 0 14px 24px rgba(15, 23, 42, .11);
}

.node.passed {
  opacity: .88;
}

.rail {
  position: relative;
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 0;
  height: 22px;
  margin: 24px 42px 0;
}

.rail::before,
.rail-fill {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  top: 9px;
  height: 4px;
  border-radius: 999px;
}

.rail::before {
  background: #e2e8f0;
}

.rail-fill {
  right: auto;
  width: 0;
  background: linear-gradient(90deg, #16a34a, #0284c7, #7c3aed, #e11d48);
  transition: width .55s ease;
}

.tick {
  position: relative;
}

.tick span {
  position: absolute;
  z-index: 1;
  left: 50%;
  top: 2px;
  width: 18px;
  height: 18px;
  transform: translateX(-50%);
  border: 3px solid #cbd5e1;
  border-radius: 999px;
  background: #ffffff;
  transition: border-color .35s ease, transform .35s ease, box-shadow .35s ease;
}

.tick.active span {
  border-color: #0f172a;
  transform: translateX(-50%) scale(1.24);
  box-shadow: 0 0 0 7px rgba(15, 23, 42, .08);
}

.tick.passed span {
  border-color: #64748b;
}

.tone-green {
  --accent: #16a34a;
  --accent-dark: #166534;
  --accent-soft: rgba(34, 197, 94, .34);
  --accent-wash: #ecfdf5;
}

.tone-blue {
  --accent: #2563eb;
  --accent-dark: #1d4ed8;
  --accent-soft: rgba(37, 99, 235, .3);
  --accent-wash: #eff6ff;
}

.tone-cyan {
  --accent: #0891b2;
  --accent-dark: #155e75;
  --accent-soft: rgba(6, 182, 212, .32);
  --accent-wash: #ecfeff;
}

.tone-purple {
  --accent: #7c3aed;
  --accent-dark: #5b21b6;
  --accent-soft: rgba(124, 58, 237, .3);
  --accent-wash: #f5f3ff;
}

.tone-amber {
  --accent: #d97706;
  --accent-dark: #92400e;
  --accent-soft: rgba(245, 158, 11, .34);
  --accent-wash: #fffbeb;
}

.tone-rose {
  --accent: #e11d48;
  --accent-dark: #9f1239;
  --accent-soft: rgba(225, 29, 72, .28);
  --accent-wash: #fff1f2;
}

@keyframes breathe {
  0%, 100% { transform: scale(.92); opacity: .3; }
  50% { transform: scale(1); opacity: .58; }
}
</style>
