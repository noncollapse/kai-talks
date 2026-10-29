<script setup>
import MathTex from './MathTex.vue'
const bars = [3, 6, 12, 21, 31, 38, 42, 38, 30, 21, 13, 7, 4]
</script>

<template>
  <div class="why-rl">
    <div class="objective-comparison">
      <section class="objective-card">
        <div class="stage-label">SFT · Learn from residuals</div>
        <h3>Fit the residual distribution</h3>
        <div class="distribution-visual" aria-label="A residual distribution and the observed residual">
          <div class="error-bars"><i v-for="(height, i) in bars" :key="i" :style="{ height: `${height}px` }" /></div>
          <div class="observed-error"><span>Observed residual</span></div>
        </div>
        <div class="objective-name">NLL + CRPS</div>
        <p>Minimizing discrepancies in distribution.</p>
        <div class="method-line"><span>UPDATE</span><b>stochastic gradient</b></div>
      </section>
      <div class="continue-arrow rl-reveal" aria-hidden="true">→</div>
      <section class="objective-card rl-reveal">
        <div class="stage-label">RL · Learn from intervals</div>
        <h3>Optimize the resulting CIs</h3>
        <div class="interval-visual" aria-label="Illustrative confidence intervals around the true mean">
          <div class="true-mean"><span>True mean</span></div>
          <i class="ci ci-wide" /><i class="ci ci-short" /><i class="ci ci-miss" />
        </div>
        <div class="objective-name">Coverage + interval length</div>
        <p>Reward shorter intervals while penalizing deviation from nominal coverage.</p>
        <div class="method-line"><span>UPDATE</span><b>policy gradient</b></div>
      </section>
    </div>
    <div class="detail-message rl-reveal">NLL and CRPS do not directly optimize CI coverage or length.</div>
  </div>
</template>

<style scoped>
.why-rl{width:876px;margin-top:24px}
.objective-comparison{position:relative;display:grid;grid-template-columns:1fr 1fr;gap:48px}
.objective-card{box-sizing:border-box;min-height:318px;border:1px solid #dce4ef;border-radius:12px;background:#fff;padding:20px 23px;text-align:center}
.stage-label{font-size:12px;line-height:18px;letter-spacing:.04em;font-weight:600;color:#71809a;text-transform:uppercase;margin-bottom:10px}
.objective-card h3{font-size:22px;line-height:1.25;letter-spacing:-.4px;margin:0;color:#17233e}
.distribution-visual,.interval-visual{position:relative;height:90px;width:240px;margin:10px auto 5px}
.error-bars{position:absolute;left:18px;right:18px;bottom:7px;display:flex;align-items:flex-end;justify-content:center;gap:5px;border-bottom:1px solid #c4cddd;height:54px}
.error-bars>i{width:11px;background:#8696ee;border-radius:2px 2px 0 0;transform:scaleY(1.15);transform-origin:bottom}
.observed-error{position:absolute;left:149px;top:25px;bottom:5px;border-left:1.5px dashed #64748b}
.observed-error>span{position:absolute;left:-48px;top:-23px;white-space:nowrap;font-size:12px;color:#73819a}
.true-mean{position:absolute;left:126px;top:23px;bottom:5px;border-left:1.5px dashed #64748b}
.true-mean>span{position:absolute;left:-30px;top:-23px;font-size:12px;white-space:nowrap;color:#73819a}
.ci{position:absolute;height:8px;border-left:2px solid #8696ee;border-right:2px solid #8696ee}
.ci:after{content:'';position:absolute;left:0;right:0;top:2px;height:2px;background:#8696ee}
.ci-wide{left:25px;right:20px;top:30px}.ci-short{left:87px;right:56px;top:53px}.ci-miss{left:36px;width:42px;top:76px;border-color:#a9b5c8}.ci-miss:after{background:#a9b5c8}
.objective-name{font-size:20px;line-height:1.4;font-weight:600;color:#4263eb}
.objective-card p{font-size:15px;line-height:1.45!important;min-height:44px;margin:10px 0 15px;color:#64748b}
.method-line{display:flex;align-items:center;justify-content:center;gap:10px;padding-top:12px;border-top:1px solid #e4e9f1}
.method-line>span{font-size:10px;letter-spacing:.06em;color:#96a1b6;font-weight:600}.method-line>b{font-size:14px;font-weight:500;color:#52627d}
.continue-arrow{position:absolute;top:148px;left:416px;width:44px;text-align:center;font-size:28px;line-height:30px;color:#a6b4ca}
.why-rl .detail-message{margin-top:14px}
.rl-reveal{transition:opacity .45s ease}
</style>
