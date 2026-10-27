<script setup>
import { ref } from 'vue'
// Horizontal lines show directions over time; dashed links identify conceptual bridges.
const activeConnection = ref(null)
const years = [
  { x: 299, label: 'Earlier foundations' },
  { x: 445, label: '2016–17' }, { x: 570, label: '2020' },
  { x: 674, label: '2022' }, { x: 790, label: '2024' },
  { x: 921, label: '2026' },
]
const lanes = [
  { key: 'classical', y: 85, start: 399, title: 'Classical ML', detail: 'Fit a model to each dataset' },
  { key: 'deep', y: 170, start: 423, title: 'Tabular deep learning', detail: 'Learn features & interactions' },
  { key: 'transfer', y: 255, start: 552, title: 'Pretraining & transfer', detail: 'Reuse learned representations' },
  { key: 'foundation', y: 340, start: 674, title: 'Foundation models', detail: 'Learn across tasks' },
]
const milestones = [
  { lane: 'classical', x: 420, labelX: 430, side: 'above', lines: ['XGBoost'], year: '2016' },
  { lane: 'classical', x: 465, side: 'below', lines: ['LightGBM', 'CatBoost'], year: '2017' },
  { lane: 'classical', x: 570, side: 'above', lines: ['NGBoost'], year: '2020' },
  { lane: 'classical', x: 620, side: 'below', lines: ['PGBM'], year: '2021', description: 'Probabilistic Gradient Boosting Machines (KDD 2021): efficient probabilistic prediction with a single tree ensemble.' },
  { lane: 'classical', x: 674, side: 'above', lines: ['Distributional', 'random forests'], year: '2022', description: 'Distributional Random Forests (JMLR 2022): estimate joint conditional distributions using distribution-sensitive tree splits.' },
  { lane: 'classical', x: 848, side: 'above', lines: ['FIGS', 'Interpretable tree sums'], year: '2025', caption: true, description: 'Fast Interpretable Greedy-Tree Sums (PNAS 2025; preprint 2022): jointly grow a small sum of trees. The timeline uses the journal publication year.' },
  { lane: 'classical', x: 921, labelX: 906, side: 'below', lines: ['XGBoost 3.2', 'Software release'], year: '2026', caption: true, description: 'XGBoost 3.2 (February 2026): progress on multi-target trees and GPU external-memory training. This is a software milestone, not a new model family.' },
  { lane: 'deep', x: 465, side: 'above', lines: ['SNN'], year: '2017' },
  { lane: 'deep', x: 524, side: 'above', lines: ['AutoInt'], year: '2019' },
  { lane: 'deep', x: 570, side: 'below', lines: ['NODE', 'TabTransformer'], year: '2020' },
  { lane: 'deep', x: 620, side: 'above', lines: ['TabNet', 'FT-Transformer'], year: '2021' },
  { lane: 'deep', x: 674, side: 'below', lines: ['MLP-PLR'], year: '2022' },
  { lane: 'deep', x: 790, side: 'above', lines: ['TabR · RealMLP'], year: '2024' },
  { lane: 'deep', x: 848, side: 'below', lines: ['TabM', 'ModernNCA'], year: '2025' },
  { lane: 'transfer', x: 570, side: 'above', lines: ['VIME'], year: '2020' },
  { lane: 'transfer', x: 620, side: 'below', lines: ['SubTab'], year: '2021' },
  { lane: 'transfer', x: 674, side: 'above', lines: ['SCARF · TransTab'], year: '2022' },
  { lane: 'transfer', x: 732, side: 'below', lines: ['XTab · TabLLM'], year: '2023' },
  { lane: 'transfer', x: 790, side: 'above', lines: ['CARTE · CM2'], year: '2024' },
  { lane: 'foundation', x: 674, side: 'above', lines: ['PFNs'], year: '2022' },
  { lane: 'foundation', x: 732, side: 'below', lines: ['TabPFN'], year: '2023' },
  { lane: 'foundation', x: 790, side: 'above', lines: ['HyperFast'], year: '2024' },
  { lane: 'foundation', x: 848, side: 'below', lines: ['TabPFN 2 / 2.5', 'TabICL'], year: '2025' },
  { lane: 'foundation', x: 921, side: 'above', lines: ['TabPFN 2.6 / 3 / 3.5', 'TabICL v2 · TabFM'], year: '2026', latest: true },
]
const roots = [
  { lane: 'deep', y: 170, title: 'MLPs & autoencoders', detail: 'Learn useful representations', period: 'Neural representation learning' },
  { lane: 'transfer', y: 255, title: 'Unsupervised pretraining', detail: 'Pretrain first, then fine-tune', period: 'Layer-wise pretraining · 2006' },
  { lane: 'foundation', y: 340, title: 'Multitask & meta-learning', detail: 'Learn from related tasks', period: 'Learning to learn · 1990s–2000s' },
]
const connections = [
  {
    id: 'trees', from: 'classical', to: 'deep',
    path: 'M 500 85 C 524 85 530 170 564 170',
    arrow: 'M 558 166 L 564 170 L 558 174',
    label: ['Differentiable', 'trees in NODE'], x: 548, y: 113,
    description: 'Tree ensembles meet end-to-end neural training in NODE (ICLR 2020).',
  },
  {
    id: 'neighbors', from: 'classical', to: 'deep',
    path: 'M 720 85 C 752 85 750 170 784 170',
    arrow: 'M 778 166 L 784 170 L 778 174',
    label: ['Neighbor retrieval', 'in TabR'], x: 791, y: 113,
    description: 'TabR (ICLR 2024) combines a neural network with a learned nearest-neighbor retrieval component.',
  },
  {
    id: 'representations', from: 'deep', to: 'transfer',
    path: 'M 430 170 C 450 170 488 255 552 255',
    arrow: 'M 546 251 L 552 255 L 546 259',
    label: ['Pretrain', 'representations'], x: 421, y: 213,
    description: 'Representation learning can become a pretraining stage, followed by adaptation to a downstream task. This is a change in training strategy, not a paper-to-paper ancestry claim.',
  },
  {
    id: 'tasks', from: 'transfer', to: 'foundation',
    path: 'M 586 255 C 588 305 624 340 668 340',
    arrow: 'M 662 336 L 668 340 L 662 344',
    label: ['Pretrain across', 'prediction tasks'], x: 546, y: 301,
    description: 'The PFN approach pretrains on sampled prediction tasks to learn a reusable prediction procedure. This link marks a change in the unit of pretraining, not descent from a particular representation-pretraining model.',
  },
]
const laneY = Object.fromEntries(lanes.map(lane => [lane.key, lane.y]))
const labelLineHeight = 18
const labelY = m => laneY[m.lane] + (m.side === 'above' ? (m.latest ? -17 : -20) - (m.lines.length - 1) * labelLineHeight : 24)
const connected = lane => {
  const current = connections.find(connection => connection.id === activeConnection.value)
  return current && (current.from === lane || current.to === lane)
}
</script>

<template>
  <div class="history-map">
    <svg class="history-chart" viewBox="0 0 1000 435" role="group" aria-labelledby="history-title history-description">
      <title id="history-title">The connected development of tabular learning</title>
      <desc id="history-description">Classical machine learning, neural networks, pretraining and foundation models share ideas. Dashed arrows show these connections and can be focused or hovered to highlight the related research directions. Early classical methods, neural representations, pretraining and meta-learning are expanded before the modern timeline. After NGBoost, the classical route includes PGBM, Distributional Random Forests, FIGS and the XGBoost 3.2 software release. The timeline includes TabPFN 2.5, 2.6, 3 and 3.5, TabICL v2, and TabFM, checked through October 2026. All content is visible without clicking.</desc>
      <defs>
        <linearGradient id="pfn-history-band" x1="0" x2="1">
          <stop offset="0" stop-color="#f5f7ff" stop-opacity="0" />
          <stop offset=".25" stop-color="#edf2ff" />
          <stop offset="1" stop-color="#e9f5f4" />
        </linearGradient>
      </defs>

      <rect x="565" y="286" width="429" height="143" rx="20" fill="url(#pfn-history-band)" />
      <path class="header-rule" d="M 0 30 H 984" />
      <g class="year-grid">
        <g v-for="year in years" :key="year.label">
          <text :x="year.x" y="18" text-anchor="middle">{{ year.label }}</text>
          <line :x1="year.x" :x2="year.x" y1="36" :y2="year.end || 382" />
        </g>
      </g>
      <text x="0" y="18" class="axis-caption">RESEARCH DIRECTIONS</text>

      <g v-for="lane in lanes" :key="lane.key" :class="['research-lane', lane.key, { connected: connected(lane.key) }]">
        <text x="0" :y="lane.y - 4" class="lane-title">{{ lane.title }}</text>
        <text x="0" :y="lane.y + 15" class="lane-detail">{{ lane.detail }}</text>
        <path class="lane-path" :d="`M ${lane.start} ${lane.y} H 975`" />
        <path class="lane-arrow" :d="`M 969 ${lane.y - 4} L 975 ${lane.y} L 969 ${lane.y + 4}`" />
      </g>

      <g :class="['classical-roots', { connected: connected('classical') }]">
        <rect x="204" y="39" width="193" height="87" rx="9" />
        <path d="M 215 53 V 111" />
        <g v-for="(text, i) in ['Linear / logistic regression', 'kNN · SVM · CART', 'AdaBoost · random forests', 'Gradient boosting (GBDT)']" :key="text">
          <circle cx="215" :cy="55 + i * 18" r="2.1" />
          <text x="225" :y="58 + i * 18">{{ text }}</text>
        </g>
      </g>
      <path class="axis-break" d="M 401 81 L 405 89 M 406 81 L 410 89" />

      <g v-for="root in roots" :key="root.lane" :class="['learning-root', root.lane, { connected: connected(root.lane) }]">
        <title>{{ root.period }}. This panel marks shared conceptual foundations, not a direct paper lineage.</title>
        <path class="root-bridge" :d="`M 397 ${root.y} H ${lanes.find(lane => lane.key === root.lane).start}`" />
        <rect x="204" :y="root.y - 27" width="193" height="54" rx="9" />
        <text x="220" :y="root.y - 6" class="root-title">{{ root.title }}</text>
        <text x="220" :y="root.y + 12" class="root-detail">{{ root.detail }}</text>
      </g>

      <g v-for="c in connections" :key="c.id" :class="['connection', { active: activeConnection === c.id }]" tabindex="0" :aria-label="c.description" @mouseenter="activeConnection = c.id" @mouseleave="activeConnection = null" @focus="activeConnection = c.id" @blur="activeConnection = null" @click.stop>
        <title>{{ c.description }}</title>
        <path class="connection-hit" :d="c.path" />
        <path class="connection-path" :d="c.path" />
        <path class="connection-arrow" :d="c.arrow" />
        <text v-for="(line, i) in c.label" :key="line" :x="c.x" :y="c.y + i * 14" text-anchor="middle">{{ line }}</text>
      </g>

      <g v-for="m in milestones" :key="`${m.lane}-${m.x}`" :class="['milestone', m.lane, { latest: m.latest, connected: connected(m.lane) }]">
        <title>{{ m.description || `${m.lines.join(' · ')} (${m.year})` }}</title>
        <line :x1="m.x" :x2="m.x" :y1="laneY[m.lane]" :y2="laneY[m.lane] + (m.side === 'above' ? -10 : 11)" />
        <circle :cx="m.x" :cy="laneY[m.lane]" r="4.2" />
        <text v-for="(line, i) in m.lines" :key="line" :class="{ 'milestone-caption': m.caption && i > 0 }" :x="m.labelX || m.x" :y="labelY(m) + i * labelLineHeight" text-anchor="middle">{{ line }}</text>
      </g>

      <g class="tabcon-destination">
        <title>TabCon uses the TabPFN-3 backbone; the other 2026 releases are parallel developments.</title>
        <path d="M 921 346 V 387 M 917 383 L 921 387 L 925 383" />
        <rect x="879" y="391" width="84" height="36" rx="9" />
        <text x="921" y="406" text-anchor="middle" class="tabcon-name">TabCon</text>
        <text x="921" y="421" text-anchor="middle" class="tabcon-target">via TabPFN 3</text>
      </g>
      <path class="legend-dash" d="M 0 428 H 22" />
      <text x="28" y="431" class="map-note">Dashed links: shared ideas & changes in training</text>
    </svg>
  </div>
</template>

<style scoped>
.history-map{width:100%;margin-top:21px;font-family:'DM Sans',sans-serif}
.history-chart{display:block;width:100%;overflow:visible;font-family:'DM Sans',sans-serif}
.header-rule{fill:none;stroke:#dce4ef;stroke-width:1}
.year-grid text{fill:#536b8b;font-size:13.021px;font-weight:700}.year-grid line{stroke:#e3e9f2;stroke-width:1;stroke-dasharray:1 7;stroke-linecap:round}
.axis-caption{fill:#7f90a9;font-size:9.375px;letter-spacing:1px;font-weight:700}
.lane-title{fill:#243650;font-size:17.708px;font-weight:700;letter-spacing:-.35px}.lane-detail{fill:#71829c;font-size:11.979px}
.lane-path,.lane-arrow{fill:none;stroke:#b3c0d4;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;transition:stroke .15s,stroke-width .15s}.deep .lane-path,.deep .lane-arrow{stroke:#8c9cb8}.transfer .lane-path,.transfer .lane-arrow{stroke:#ac9bbf}.foundation .lane-path,.foundation .lane-arrow{stroke:#4263eb;stroke-width:3}
.foundation .lane-title{fill:#4263eb}.foundation .lane-detail{fill:#7187c5}
.classical-roots rect{fill:#f4f7fb;stroke:#e0e7f0;stroke-width:1;transition:stroke .15s}.classical-roots path{stroke:#c6d1e2;stroke-width:1;fill:none}.classical-roots circle{fill:#9aabc3}.classical-roots text{fill:#455a77;font-size:11.979px;font-weight:500}.classical-roots.connected rect{stroke:#718ac2}
.learning-root rect{fill:#f4f7fb;stroke:#e0e7f0;stroke-width:1;transition:stroke .15s}.learning-root .root-title{fill:#455a77;font-size:13.021px;font-weight:650}.learning-root .root-detail{fill:#76869f;font-size:10.938px}.learning-root .root-bridge{stroke:#c0cadb;stroke-width:1.2;stroke-dasharray:3 5;fill:none}.learning-root.foundation rect{fill:#f1f5ff;stroke:#dbe3f8}.learning-root.foundation .root-title{fill:#687fae}.learning-root.connected rect{stroke:#718ac2}.learning-root.connected .root-bridge{stroke:#7c81b3}
.axis-break{stroke:#9eafc8;stroke-width:1.2;fill:none}
.milestone line{stroke:#b3c0d4;stroke-width:1}.milestone circle{fill:#fbfcff;stroke:#9dadc4;stroke-width:2}.milestone text{fill:#35465e;font-size:12.5px;font-weight:550;paint-order:stroke;stroke:#fbfcff;stroke-width:3px;stroke-linejoin:round}
.transfer circle{stroke:#a492b8}.transfer text{fill:#746486}.milestone.foundation circle{stroke:#4263eb;fill:#4263eb}.milestone.foundation text{fill:#4263eb;font-weight:800;font-size:13.021px;stroke:#eef3fc;stroke-width:4px}.milestone.foundation line{stroke:#7f99ed}.milestone.foundation.latest text{font-size:12.5px}.milestone.foundation.latest circle{r:4.8px}
.connection{outline:none}.connection-path,.connection-arrow,.legend-dash{stroke:#9ca9bd;stroke-width:1.5;fill:none;stroke-linecap:round;stroke-linejoin:round}.connection-path,.legend-dash{stroke-dasharray:3 4}.connection-hit{stroke:transparent;stroke-width:15;fill:none;pointer-events:stroke}.connection text{fill:#806c9a;font-size:10.938px;font-weight:600;paint-order:stroke;stroke:#fbfcff;stroke-width:5px;stroke-linejoin:round;cursor:default}.connection.active .connection-path,.connection.active .connection-arrow{stroke:#7c4dce;stroke-width:2.5}.connection.active text{fill:#7c4dce;font-weight:800}.research-lane.connected .lane-path,.research-lane.connected .lane-arrow{stroke:#7c81b3;stroke-width:3}.milestone.connected circle{stroke:#7c81b3}.milestone.connected text{font-weight:700}
.milestone text.milestone-caption{fill:#71829c;font-size:10.938px;font-weight:500}
.tabcon-destination rect{fill:#e3f3ee;stroke:#9dcdc0;stroke-width:1}.tabcon-destination path{stroke:#4263eb;stroke-width:2;fill:none;stroke-linecap:round;stroke-linejoin:round}.tabcon-name{fill:#078772;font-size:14.583px;font-weight:800;letter-spacing:-.4px}.tabcon-target{fill:#328e7e;font-size:9.375px}
.map-note{fill:#7c8da7;font-size:9.896px}
@media(prefers-reduced-motion:reduce){.lane-path,.lane-arrow,.classical-roots rect,.learning-root rect{transition:none}}
</style>
