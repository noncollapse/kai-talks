<script setup>
import MathTex from './MathTex.vue'
</script>
<template>
  <svg class="tabcon-intro" viewBox="0 0 876 330" role="img" aria-label="A dataset enters TabCon, which returns both a point estimate and a confidence interval for the regression mean.">
    <g transform="translate(65 114)">
      <rect width="125" height="86" rx="10" fill="white" stroke="#5877ce" stroke-width="2.5" />
      <rect x="9" y="9" width="107" height="14" rx="3" fill="#4263eb" fill-opacity=".65" />
      <g v-for="row in [0,1,2,3]" :key="row">
        <rect v-for="col in [0,1,2,3]" :key="col" :x="11+col*27" :y="32+row*12" width="20" height="6" rx="2" fill="#4263eb" :style="{opacity:.45+((row+col)%3)*.2}" />
      </g>
    </g>
    <text x="127" y="95" text-anchor="middle" fill="#17233e" style="font-size:20px;font-weight:700">Dataset</text>
    <path d="M 205 157 H 321 M 313 151 L 321 157 L 313 163" stroke="#6e86b2" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round" />
    <rect class="tabcon-halo" x="334" y="88" width="160" height="138" rx="28" fill="#eef2ff" />
    <rect x="347" y="101" width="134" height="112" rx="19" fill="#fbfcff" stroke="#4263eb" stroke-width="3" />
    <g stroke="#8299d6" stroke-width="2.3" fill="none">
      <path d="M 374 127 L 414 135 L 454 127 M 374 127 L 414 179 L 454 127 M 374 187 L 414 135 L 454 187 M 374 187 L 414 179 L 454 187" />
    </g>
    <g fill="#4263eb"><circle cx="374" cy="127" r="6"/><circle cx="374" cy="187" r="6"/><circle cx="414" cy="135" r="6"/><circle cx="414" cy="179" r="6"/><circle cx="454" cy="127" r="6"/><circle cx="454" cy="187" r="6"/></g>
    <text x="414" y="75" text-anchor="middle" fill="#17233e" style="font-size:20px;font-weight:700">TabCon</text>
    <path d="M 497 157 C 553 157 550 80 605 80 M 597 74 L 605 80 L 597 86" fill="none" stroke="#6587dc" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
    <path d="M 497 157 C 553 157 550 232 605 232 M 597 226 L 605 232 L 597 238" fill="none" stroke="#6587dc" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
    <text x="725" y="48" text-anchor="middle" fill="#17233e" style="font-size:19px;font-weight:700">Point estimate</text>
    <line x1="651" x2="799" y1="88" y2="88" stroke="#dce4f2" stroke-width="2" />
    <circle class="estimate-output" cx="725" cy="88" r="7" fill="#4263eb" />
    <foreignObject x="645" y="104" width="160" height="40"><div xmlns="http://www.w3.org/1999/xhtml" class="intro-formula estimate-formula"><MathTex tex="\widehat{\boldsymbol{f}}(\boldsymbol{x})" /></div></foreignObject>
    <text x="725" y="196" text-anchor="middle" fill="#17233e" style="font-size:19px;font-weight:700">Confidence interval</text>
    <rect class="interval-glow" x="654" y="224" width="142" height="16" rx="8" fill="#4263eb" fill-opacity=".1" />
    <path d="M 654 232 H 796 M 654 223 V 241 M 796 223 V 241" stroke="#4263eb" stroke-width="4" fill="none" stroke-linecap="round" />
    <foreignObject x="625" y="252" width="200" height="42"><div xmlns="http://www.w3.org/1999/xhtml" class="intro-formula interval-formula"><MathTex tex="[\boldsymbol{L}(\boldsymbol{x}),\,\boldsymbol{U}(\boldsymbol{x})]" /></div></foreignObject>
    <circle class="intro-flow input-flow" r="4" fill="#4263eb" />
    <circle class="intro-flow point-flow" r="4" fill="#4263eb" />
    <circle class="intro-flow interval-flow" r="4" fill="#4263eb" />
  </svg>
</template>
<style scoped>
.tabcon-intro{display:block;width:100%;height:330px;margin-top:10px}
.intro-formula{width:100%;text-align:center;font-size:20px;line-height:1.5}
.estimate-formula{color:#4263eb}.interval-formula{color:#4263eb}
.intro-flow{opacity:0;offset-distance:0%;animation:introFlow 6s linear infinite}
.input-flow{offset-path:path('M 205 157 H 321')}
.point-flow{offset-path:path('M 497 157 C 553 157 550 80 605 80');animation-delay:2s}
.interval-flow{offset-path:path('M 497 157 C 553 157 550 232 605 232');animation-delay:2s}
.tabcon-halo{transform-origin:414px 157px;animation:introModelPulse 6s ease-in-out infinite}
.estimate-output,.interval-glow{animation:introOutputPulse 6s ease-in-out infinite}
@keyframes introFlow{0%{opacity:0;offset-distance:0%}5%{opacity:.9}27%{opacity:.9;offset-distance:100%}33%,100%{opacity:0;offset-distance:100%}}
@keyframes introModelPulse{0%,24%,70%,100%{opacity:.65;transform:scale(1)}38%,48%{opacity:1;transform:scale(1.045)}}
@keyframes introOutputPulse{0%,45%,100%{opacity:.55}65%,80%{opacity:1}}
@media(prefers-reduced-motion:reduce){.intro-flow{display:none}.tabcon-halo,.estimate-output,.interval-glow{animation:none}}
</style>
