<script setup>
import { useSlideContext } from '@slidev/client'
import MathTex from './MathTex.vue'
const { $clicks } = useSlideContext()
const bars = [3, 6, 12, 21, 31, 38, 42, 38, 30, 21, 13, 7, 4]
</script>

<template>
  <div class="why-rl">
    <div class="shared-architecture"><span>IN BOTH STAGES</span><b>Top-2 task routing</b><i />Frozen backbone + three frozen experts</div>
    <div class="objective-comparison">
      <section class="objective-card">
        <div class="stage-label">SFT · Learn from errors</div>
        <h3>Fit the error distribution</h3>
        <div class="distribution-visual" aria-label="An error distribution and the observed error">
          <div class="error-bars"><i v-for="(height, i) in bars" :key="i" :style="{ height: `${height}px` }" /></div>
          <div class="observed-error"><span>Observed error</span></div>
        </div>
        <div class="objective-name"><MathTex tex="\mathrm{NLL}+\mathrm{CRPS}" /></div>
        <p>Score how well the mixture<br>explains the simulated errors.</p>
        <div class="method-line"><span>UPDATE</span><b>Straight-through gradient</b></div>
      </section>
      <div class="continue-arrow rl-reveal" :class="{ concealed: $clicks < 1 }" aria-hidden="true">→</div>
      <section class="objective-card rl-reveal" :class="{ concealed: $clicks < 1 }">
        <div class="stage-label">RL · Learn from intervals</div>
        <h3>Optimize the resulting CIs</h3>
        <div class="interval-visual" aria-label="Illustrative confidence intervals around the true mean">
          <div class="true-mean"><span>True mean</span></div>
          <i class="ci ci-wide" /><i class="ci ci-short" /><i class="ci ci-miss" />
        </div>
        <div class="objective-name">Coverage + interval length</div>
        <p>Reward useful precision<br>and penalize coverage failures.</p>
        <div class="method-line"><span>UPDATE</span><b>Sample routing actions → RLOO</b></div>
      </section>
    </div>
    <div class="why-rl-message rl-reveal" :class="{ concealed: $clicks < 2 }"><b>Why continue with RL?</b><span>NLL and CRPS do not directly optimize CI coverage or length.</span></div>
  </div>
</template>

<style scoped>
.why-rl{width:876px;margin-top:17px}
.shared-architecture{display:flex;align-items:center;justify-content:center;gap:13px;height:34px;background:#eef1f8;border-radius:8px;color:#73819a;font-size:11px}.shared-architecture>span{font-size:8px;font-weight:800;letter-spacing:.07em;color:#7c4dce}.shared-architecture>b{color:#17233e;font-size:12px}.shared-architecture>i{height:13px;width:1px;background:#cbd4e4}
.objective-comparison{position:relative;display:grid;grid-template-columns:1fr 1fr;gap:48px;margin-top:15px}
.objective-card{box-sizing:border-box;height:282px;border:1px solid #dce4f2;border-radius:15px;background:#fff;padding:18px 23px;text-align:center}
.stage-label{font-size:10px;letter-spacing:.07em;font-weight:800;color:#7c4dce;text-transform:uppercase;margin-bottom:9px}
.objective-card h3{font-size:23px;font-weight:800;line-height:1.25;letter-spacing:-.5px;margin:0;color:#17233e}
.distribution-visual,.interval-visual{position:relative;height:72px;width:220px;margin:8px auto 3px}
.error-bars{position:absolute;left:17px;right:17px;bottom:6px;display:flex;align-items:flex-end;justify-content:center;gap:4px;border-bottom:1px solid #b8c5da;height:46px}.error-bars>i{width:10px;background:#8696ee;border-radius:2px 2px 0 0}
.observed-error{position:absolute;left:139px;top:21px;bottom:4px;border-left:1.5px dashed #17233e}.observed-error>span{position:absolute;left:-39px;top:-18px;white-space:nowrap;font-size:10px;color:#73819a}
.true-mean{position:absolute;left:116px;top:20px;bottom:3px;border-left:1.5px dashed #17233e}.true-mean>span{position:absolute;left:-25px;top:-17px;font-size:10px;white-space:nowrap;color:#73819a}
.ci{position:absolute;height:8px;border-left:2px solid #8696ee;border-right:2px solid #8696ee}.ci:after{content:'';position:absolute;left:0;right:0;top:2px;height:2px;background:#8696ee}.ci-wide{left:30px;right:20px;top:25px}.ci-short{left:83px;right:56px;top:42px}.ci-miss{left:36px;width:42px;top:59px;border-color:#a9b5c8}.ci-miss:after{background:#a9b5c8}
.objective-name{font-size:19px;line-height:1.5;font-weight:700;color:#4263eb}.objective-name>.math-tex-inline{font-size:22px}
.objective-card p{font-size:13px;line-height:1.5!important;margin:8px 0 14px;color:#73819a}
.method-line{display:flex;align-items:center;justify-content:center;gap:9px;padding-top:11px;border-top:1px solid #e8edf5}.method-line>span{font-size:8px;letter-spacing:.06em;color:#96a1b6;font-weight:700}.method-line>b{font-size:11px;font-weight:600;color:#7c4dce}
.continue-arrow{position:absolute;top:123px;left:416px;width:44px;text-align:center;font-size:28px;line-height:30px;color:#a6b4ca}
.why-rl-message{display:flex;align-items:center;gap:20px;background:#eef2ff;border-radius:10px;padding:14px 18px;border-left:3px solid #4263eb;margin-top:16px}.why-rl-message>b{font-size:14px;color:#4263eb;white-space:nowrap}.why-rl-message>span{font-size:14px;color:#17233e}
.rl-reveal{transition:opacity .45s ease}.rl-reveal.concealed{opacity:0;pointer-events:none}
@media(prefers-reduced-motion:reduce){.rl-reveal{transition:none}}
</style>
