<script setup>
import { useSlideContext } from '@slidev/client'
const { $clicks } = useSlideContext()
const attention = [
  [.10,.15,.40,.25,.10],
  [.35,.30,.10,.15,.10],
  [.10,.10,.15,.25,.40],
  [.15,.35,.25,.15,.10],
]
</script>

<template>
  <div class="attention-map">
    <svg class="attention-links" viewBox="0 0 876 380" aria-hidden="true">
      <defs><marker id="attention-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7" fill="#a5b1c9" /></marker></defs>
      <g fill="none" stroke="#a5b1c9" stroke-width="1.7" marker-end="url(#attention-arrow)">
        <path class="reveal" :class="{waiting:$clicks<1}" d="M180 174H202V128H226" />
        <path class="reveal" :class="{waiting:$clicks<2}" d="M202 174V296H226" />
        <path class="reveal" :class="{waiting:$clicks<2}" d="M618 128H666" />
        <path class="reveal" :class="{waiting:$clicks<2}" d="M618 296H642V217H666" />
        <path class="reveal" :class="{waiting:$clicks<3}" d="M773 270V292" />
      </g>
      <circle class="reveal" :class="{waiting:$clicks<2}" cx="202" cy="174" r="3" fill="#a5b1c9" />
    </svg>
    <section class="query-set"><span class="small-label">From frozen TabPFN</span><h3>Query embeddings</h3>
      <div class="encoder-chip">Shared trainable encoder</div>
      <span class="token-label">Encoded query tokens</span>
      <div class="embedding-rows"><div v-for="row in 5" :key="row"><span>h<sub>{{row}}</sub></span><i v-for="cell in 6" :key="cell" :style="{opacity:.25+((row*3+cell)%7)/10}" /></div></div>
      <small>One token per query point</small>
    </section>
    <section class="attention-pool reveal" :class="{waiting:$clicks<1}"><span class="small-label">Learned attention pooling</span><h3>Which query points matter?</h3>
      <div class="attention-grid"><div class="grid-label">Learned<br>queries</div><span v-for="q in 5" :key="`q${q}`">h<sub>{{q}}</sub></span><div class="grid-label">Pooled<br>summary</div>
        <template v-for="(weights,j) in attention" :key="j"><b class="query-label">a<sub>{{j+1}}</sub></b><i v-for="(weight,q) in weights" :key="q" :style="{background:`rgba(124,77,206,${.12+weight*1.8})`}" /><b class="summary-token">u<sub>{{j+1}}</sub></b></template>
      </div>
      <p>Four learned, weighted averages of the query tokens.</p>
    </section>
    <section class="query-statistics reveal" :class="{waiting:$clicks<2}">
      <span class="small-label">Across all query tokens · coordinate by coordinate</span>
      <div><b>Mean(h)</b><span>average</span><b>Std(h)</b><span>variation</span></div>
    </section>
    <section class="task-summary reveal" :class="{waiting:$clicks<2}"><span class="small-label">Concatenate six vectors</span><h3>Query-set<br>summary</h3><div class="summary-tokens"><b v-for="i in 4" :key="i">u<sub>{{i}}</sub></b></div><div class="summary-tokens summary-statistics"><b>Mean(h)</b><b>Std(h)</b></div><small>Statistics of the query tokens,<br>alongside attention summaries.</small></section>
    <span class="routing-mlp-label reveal" :class="{waiting:$clicks<3}">Routing network</span>
    <section class="expert-scores reveal" :class="{waiting:$clicks<3}"><span class="small-label">Scores for the three experts</span><div><b>G</b><i style="height:20px;background:#4263eb"/><b>E</b><i style="height:32px;background:#7c4dce"/><b>S</b><i style="height:10px;background:#0b9687"/></div></section>
    <div class="attention-caption">Attention learns what to emphasize. Mean + std retain the overall average and variation.</div>
  </div>
</template>

<style scoped>
.attention-map{position:relative;width:876px;height:384px;margin-top:20px}
.attention-links{position:absolute;left:0;top:0;width:876px;height:380px;pointer-events:none}
.attention-map section{position:absolute;border:1px solid #dce3f1;border-radius:14px;background:white;text-align:center;padding:18px 12px}
.attention-map h3{font-size:20px;line-height:1.3;font-weight:800;margin:9px 0 0}
.small-label{display:block;font-size:10px;line-height:1.35;color:#7d8ba4}
.query-set{left:0;top:40px;width:180px;height:272px;background:#f2f5fa!important}
.attention-map .query-set h3{font-size:16px}
.embedding-rows{margin:9px 0 12px}.embedding-rows>div{display:flex;gap:4px;align-items:center;justify-content:center;height:14px;line-height:1.2;margin:5px 0}.embedding-rows span{font-size:11px;width:20px;color:#6d7f9b}.embedding-rows i{height:12px;width:13px;border-radius:3px;background:#6d88c9}
.encoder-chip{font-size:10px;line-height:1.4;color:#4263eb;background:#e8edfa;border-radius:7px;padding:6px 3px;margin-top:12px}
.token-label{display:block;margin-top:12px;font-size:10px;line-height:1.35;font-weight:700;color:#4263eb}.query-set small{display:block;font-size:9px;line-height:1.35;color:#7d8ba4}
.attention-pool{left:230px;top:6px;width:388px;height:244px;padding:14px 12px!important;border-color:#d8c9ed!important;background:#fbf8ff!important}
.attention-pool .small-label{color:#7c4dce;font-weight:700}
.attention-pool h3{font-size:18px;color:#7c4dce;margin-top:6px}
.attention-grid{display:grid;grid-template-columns:52px repeat(5,34px) 48px;justify-content:center;gap:5px 7px;align-items:center;margin-top:12px}
.attention-grid>span{font-size:11px;color:#8c7d9f}.grid-label{font-size:8px;color:#8c7d9f;line-height:1.35}.query-label{font-size:13px;color:#7c4dce}.attention-grid i{height:22px;border-radius:4px}.summary-token{font-size:12px;line-height:1.4;border-radius:5px;background:#e9def8;color:#7c4dce;padding:3px 4px}
.attention-pool p{font-size:10px;color:#8a76a3;margin:9px 0 0;line-height:1.5}
.query-statistics{left:230px;top:262px;width:388px;height:68px;padding:9px 12px!important;background:#f5f1fb!important;border-color:#d8c9ed!important}
.query-statistics>div{display:flex;align-items:center;justify-content:center;gap:9px;margin-top:6px}.query-statistics b{font-size:11px;line-height:1.4;color:#7c4dce;background:#e9def8;border-radius:6px;padding:5px 8px}.query-statistics>div>span{font-size:10px;color:#7f6998}.query-statistics>div>b:nth-of-type(2){margin-left:12px}
.task-summary{left:670px;top:48px;width:206px;height:222px;background:#f5f1fb!important}
.summary-tokens{display:flex;justify-content:center;gap:7px;margin-top:13px}.summary-tokens b{color:#7c4dce;background:#e9def8;padding:5px 8px;border-radius:6px;font-size:12px;line-height:1.4}.summary-statistics{margin-top:7px}
.task-summary small{display:block;font-size:9px;line-height:1.45;color:#8d7b9f;margin-top:10px}
.routing-mlp-label{position:absolute;left:782px;top:273px;font-size:10px;color:#7c4dce}
.expert-scores{left:670px;top:296px;width:206px;height:84px;padding:10px!important}.expert-scores>div{display:flex;justify-content:center;align-items:flex-end;gap:8px;margin-top:8px}.expert-scores b{font-size:10px;color:#7c89a1;line-height:1}.expert-scores i{display:block;width:16px;border-radius:3px 3px 0 0}
.attention-caption{position:absolute;left:0;top:346px;width:618px;border-left:3px solid #7c4dce;padding:8px 11px;background:#f3edfb;border-radius:0 8px 8px 0;font-size:12px;line-height:1.45;color:#7c4dce}
</style>
