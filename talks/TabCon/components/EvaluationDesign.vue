<template>
  <div class="evaluation-design">
    <div class="benchmark-groups"><span>Synthetic evaluation</span><span>Real features + simulated responses</span></div>
    <div class="benchmark-cards">
      <section>
        <div class="benchmark-number">1</div>
        <h3>In-distribution</h3>
        <p class="benchmark-purpose">New datasets from the training DGPs.</p>
        <div class="benchmark-summary">Generalization to new datasets from the same DGPs.</div>
      </section>
      <section>
        <div class="benchmark-number">2</div>
        <h3>Out-of-distribution</h3>
        <p class="benchmark-purpose">New datasets from DGPs unseen during training.</p>
        <div class="benchmark-summary">Generalization beyond the training DGPs.</div>
      </section>
      <section>
        <div class="benchmark-number">3</div>
        <h3>Stress test</h3>
        <ul><li>Heavy-tailed noise</li><li>Heteroskedastic noise</li><li>Discontinuous functions</li><li>Outliers</li><li class="ellipsis-item">…</li></ul>
        <div class="benchmark-summary">Robustness to challenging DGPs.</div>
      </section>
      <section>
        <div class="benchmark-number">4</div>
        <h3>CC18</h3>
        <p class="benchmark-purpose">13 real-world feature datasets with a simulated regression mean.</p>
        <div class="benchmark-summary">Evaluation on DGPs based on real-world data.</div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.evaluation-design{width:876px;margin-top:24px}
.benchmark-groups{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-bottom:10px;color:#7b879c;font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.benchmark-groups>span{border-bottom:1px solid #dbe2ef;padding-bottom:7px}
.benchmark-groups>span:first-child{grid-column:span 3}
.benchmark-groups>span:last-child{letter-spacing:0}
.benchmark-cards{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.benchmark-cards section{box-sizing:border-box;position:relative;height:294px;border:1px solid #dfe5ee;border-radius:14px;background:white;padding:20px 15px}
.benchmark-number{position:absolute;right:12px;top:12px;font-family:Manrope,sans-serif;font-size:11px;font-weight:700;color:#a1acbd}
.benchmark-cards h3{font-family:Manrope,sans-serif;font-size:20px;line-height:1.2;font-weight:800;letter-spacing:-.4px;min-height:48px;padding-right:8px;margin:0 0 13px;color:#17233e}
.benchmark-cards .benchmark-purpose,.benchmark-cards ul{font-family:'DM Sans',sans-serif;font-size:13px;font-weight:400;line-height:1.45;color:#53647e;margin:0}
.benchmark-cards ul{padding:0;list-style:none}
.benchmark-cards li{position:relative;padding-left:10px;margin:0 0 8px}
.benchmark-cards li::before{content:'';position:absolute;left:0;top:7px;width:3px;height:3px;border-radius:50%;background:#8a98ac}
.benchmark-summary{position:absolute;box-sizing:border-box;left:15px;right:15px;bottom:16px;height:56px;border-top:1px solid #edf0f5;padding-top:10px;font-family:'DM Sans',sans-serif;font-size:10px;font-weight:400;line-height:1.5;color:#7f8da3}
</style>

<style scoped>
.benchmark-cards li{display:flex;align-items:baseline;gap:7px;padding-left:0;line-height:1.45}
.benchmark-cards li::before{position:static;flex:0 0 3px;align-self:center}
.benchmark-cards .ellipsis-item{line-height:1}
.benchmark-cards section:last-child h3{margin-bottom:8px}
</style>
