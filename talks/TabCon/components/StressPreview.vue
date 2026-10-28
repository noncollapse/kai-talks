<script setup>
import summary from '../figures/data/stress_tradeoff_summary.json'

const figureVersion = summary.figure_sha256?.slice(0, 12) || summary.additional_results_source_sha256?.slice(0, 12) || 'base'
const figureUrl = `${import.meta.env.BASE_URL}figs/stress-opening-tradeoff.svg?v=${figureVersion}`
const coverage = (summary.methods.TabCon.mean_coverage * 100).toFixed(1)
const reduction = (summary.tabcon_length_reduction_vs_tabpfn_pi * 100).toFixed(0)
const tasks = (summary.settings * summary.tasks_per_setting).toLocaleString('en-US')
</script>

<template>
  <div class="stress-preview">
    <img class="stress-radar" :src="figureUrl" alt="Mean interval length versus signed coverage deviation from the 95% target, evaluated against the saved latent oracle across ten stress settings. Negative values indicate average undercoverage and positive values indicate average overcoverage. Each point shows one method's means across settings; setting-level variation is not displayed." />
    <div class="stress-highlights">
      <div><strong>{{ coverage }}<small>%</small></strong><span>TabCon average coverage<br><b>95% nominal level</b></span></div>
      <div><strong>{{ reduction }}<small>%</small></strong><span>Shorter average intervals<br><b>vs. native TabPFN prediction intervals</b></span></div>
      <div><strong>50<small>×</small></strong><span>Faster inference<br><b>vs. classical bootstrap<br>with just 50 samples</b></span></div>
      <div class="stress-scope"><strong>{{ tasks }}</strong><span>Datasets<br><b>{{ summary.settings }} settings</b></span></div>
    </div>
  </div>
</template>

<style scoped>
.stress-preview{width:100%}
.stress-radar{display:block;width:100%;height:auto;margin:0}
.stress-highlights{display:grid;grid-template-columns:1fr 1.35fr 1.25fr .8fr;gap:14px;border-top:1px solid #dce4f2;padding:9px 7px 0;margin-top:-2px}
.stress-highlights>div{display:flex;align-items:center;gap:13px}
.stress-highlights strong{font-family:Manrope,sans-serif;font-size:30px;letter-spacing:-1.3px;font-weight:800;color:#4263eb;white-space:nowrap}
.stress-highlights small{font-size:18px;letter-spacing:-.5px}
.stress-highlights span{font-size:12px;line-height:1.5;color:#34455f}
.stress-highlights b{font-size:9.5px;font-weight:500;color:#7b8ba3}
.stress-scope strong{color:#52657f;font-size:25px;letter-spacing:-.8px}
</style>
