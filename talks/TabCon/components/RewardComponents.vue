<script setup>
const groups = [
  {
    title: ['Interval', 'precision'],
    rewards: [
      {
        title: 'Interval length', code: 'WIL', icon: 'width',
        emphasis: '',
        description: 'Reward shorter intervals than those produced by Global Head.',
      },
      {
        title: 'Interval score', code: 'WIS', icon: 'score',
        emphasis: '',
        description: 'Penalize how far the ground truth falls outside the interval.',
      },
    ],
  },
  {
    title: ['Coverage', 'calibration'],
    rewards: [
      {
        title: 'Coverage', code: 'CS', icon: 'coverage',
        emphasis: '',
        description: 'Penalize deviations from the nominal level.',
      },
      {
        title: 'Tail balance', icon: 'tails',
        emphasis: '',
        description: 'Penalize highly asymmetric CIs, where lower and upper endpoints correspond to unbalanced tail probabilities.',
      },
    ],
  },
  {
    title: ['Extra', 'safeguards'],
    rewards: [
      {
        title: 'Severe undercoverage', code: 'CVaR', icon: 'risk',
        emphasis: '',
        description: 'Apply a conditional value-at-risk penalty to undercoverage violations.',
      },
      {
        title: 'Excess width', icon: 'budget',
        emphasis: '',
        description: 'Extra penalty for intervals that are excessively long relative to Global Head.',
      },
    ],
  },
]
</script>

<template>
  <div class="reward-components">
    <section v-for="group in groups" :key="group.title[0]" class="reward-group">
      <div class="reward-pair">
        <article v-for="reward in group.rewards" :key="reward.title" class="reward-item">
          <div class="item-heading">
            <svg class="reward-icon" viewBox="0 0 40 32" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <g v-if="reward.icon === 'width'"><path d="M3 8H37M3 5V11M37 5V11" opacity=".3"/><path d="M11 24H29M11 20V28M29 20V28"/></g>
              <g v-else-if="reward.icon === 'score'"><path d="M3 17H23M3 12V22M23 12V22"/><path d="M24 17H34" stroke-dasharray="2 3" opacity=".45"/><circle cx="36" cy="17" r="2.3" fill="currentColor" stroke="none"/></g>
              <g v-else-if="reward.icon === 'coverage'" fill="currentColor" stroke="none"><circle cx="7" cy="9" r="2.4"/><circle cx="20" cy="9" r="2.4"/><circle cx="33" cy="9" r="2.4"/><circle cx="7" cy="23" r="2.4"/><circle cx="20" cy="23" r="2.4"/><circle cx="33" cy="23" r="2.4" fill="none" stroke="currentColor" stroke-width="1.5" opacity=".35"/></g>
              <g v-else-if="reward.icon === 'tails'"><path d="M12 17H28M12 12V22M28 12V22"/><circle cx="4" cy="17" r="2.2" fill="currentColor" stroke="none"/><circle cx="36" cy="17" r="2.2" fill="currentColor" stroke="none"/></g>
              <g v-else-if="reward.icon === 'risk'"><path d="M3 28H37" opacity=".3"/><path d="M8 27V22M17 27V18M26 27V11" stroke-width="4" opacity=".3"/><path d="M35 27V4" stroke-width="4"/></g>
              <g v-else><path d="M5 8H25M5 5V11M25 5V11" opacity=".3"/><path d="M25 3V29" stroke-dasharray="2 3" opacity=".4"/><path d="M5 23H36M5 19V27M36 19V27"/></g>
            </svg>
            <h3>{{ reward.title }}</h3>
          </div>
          <p v-if="reward.code === 'WIL'">Reward <strong>shorter intervals</strong> than those produced by Global Head.</p>
          <p v-else-if="reward.code === 'WIS'">Penalize how <strong>far</strong> the <strong>ground truth falls outside</strong> the interval.</p>
          <p v-else-if="reward.code === 'CS'">Penalize <strong>deviations</strong> from the <strong>nominal level</strong>.</p>
          <p v-else-if="reward.icon === 'tails'">Penalize <strong>highly asymmetric</strong> CIs, where lower and upper endpoints correspond to unbalanced tail probabilities.</p>
          <p v-else-if="reward.code === 'CVaR'">Apply a <strong>conditional value-at-risk</strong> penalty to undercoverage violations.</p>
          <p v-else-if="reward.icon === 'budget'">Extra penalty for intervals that are <strong>excessively long</strong> relative to Global Head.</p>
          <p v-else><strong>{{ reward.emphasis }}</strong> {{ reward.description }}</p>
        </article>
      </div>
    </section>
  </div>
</template>

<style scoped>
.reward-components{width:876px;margin-top:26px;display:flex;flex-direction:column;gap:15px}
.reward-group{display:grid;grid-template-columns:150px 1fr;gap:20px;align-items:center;min-width:0}
.group-heading{padding-left:2px}.group-number{display:block;font-size:10px;font-weight:700;letter-spacing:.1em;color:#99a4b4;margin-bottom:8px}
.reward-components h2{font-size:22px;line-height:1.18;font-weight:800;letter-spacing:-.6px;margin:0;color:#17233e}.reward-components h2>span{display:block}
.reward-pair{height:111px;display:grid;grid-template-columns:1fr 1fr;background:#fff;border:1px solid #e3e7ee;border-radius:14px;box-shadow:0 4px 15px #17233e04;overflow:hidden}
.reward-item{box-sizing:border-box;min-width:0;padding:15px 18px}.reward-item+.reward-item{border-left:1px solid #edf0f4}
.item-heading{display:flex;align-items:center;gap:8px;margin-bottom:10px;min-width:0}
.reward-icon{width:29px;height:24px;flex:none;color:#47566e;margin-right:2px}
.reward-components h3{font-size:18px;line-height:1.25;font-weight:800;letter-spacing:-.35px;margin:0;color:#17233e;white-space:nowrap}
.reward-code{margin-left:auto;font-size:10px;line-height:1.2;font-weight:700;letter-spacing:.03em;color:#98a2b2}
.reward-components p{font-size:13px;line-height:1.5;margin:0;color:#6b7a91}
.reward-components strong{font-weight:600;color:#33415b}
</style>

<style scoped>
.reward-components{width:820px;max-width:100%;margin:36px auto 0;gap:15px}
.reward-group{display:block}
.reward-pair{height:111px}
</style>
