<template>
  <div class="evaluation-design">
    <div class="benchmark-groups"><span>Synthetic evaluation</span><span>Real features + simulated responses</span></div>
    <div class="benchmark-cards">
      <section>
        <div class="benchmark-number">01</div>
        <h3>Standard</h3>
        <p class="benchmark-purpose">Generalization across broadly sampled tasks.</p>
        <div class="benchmark-detail"><b>ID</b><p>New datasets from the training generator family.</p></div>
        <div class="benchmark-detail"><b>OOD</b><p>Held-out function families.</p></div>
        <div class="benchmark-summary">Many task factors vary together.</div>
      </section>
      <section>
        <div class="benchmark-number">02</div>
        <h3>Stress-test</h3>
        <p class="benchmark-purpose">A separate suite that isolates one difficulty at a time.</p>
        <ul><li>Abrupt or quantized functions</li><li>Heavy tails, outliers, unequal noise</li><li>Categorical and missing features</li></ul>
        <div class="benchmark-summary">Shared generator; controlled settings.</div>
      </section>
      <section>
        <div class="benchmark-number">03</div>
        <h3>CC18</h3>
        <p class="benchmark-purpose">13 real feature datasets with a known regression mean.</p>
        <div class="benchmark-detail"><b>Inputs</b><p>Observed OpenML-CC18 covariates.</p></div>
        <div class="benchmark-detail"><b>Responses</b><p>Simulated from a known function.</p></div>
        <div class="benchmark-summary">Realistic inputs; available ground truth.</div>
      </section>
    </div>
    <div class="evaluation-target"><b>Same evaluation target</b><span>Coverage of the true regression mean, together with interval width.</span></div>
  </div>
</template>

<style scoped>
.evaluation-design{width:876px;margin-top:24px}
.benchmark-groups{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-bottom:10px;color:#7b879c;font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.benchmark-groups>span:first-child{grid-column:span 2;border-bottom:1px solid #dbe2ef;padding-bottom:7px}.benchmark-groups>span:last-child{border-bottom:1px solid #dbe2ef;padding-bottom:7px}
.benchmark-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.benchmark-cards section{box-sizing:border-box;position:relative;height:276px;border:1px solid #dfe5ee;border-radius:14px;background:white;padding:20px 19px}
.benchmark-number{position:absolute;right:19px;top:25px;font-size:11px;font-weight:700;letter-spacing:.06em;color:#a1acbd}
.benchmark-cards h3{font-size:27px;line-height:1.2;font-weight:800;letter-spacing:-.7px;margin:0 0 13px;color:#17233e}
.benchmark-cards .benchmark-purpose{font-size:14px;line-height:1.45;color:#53647e;margin:0 0 18px;min-height:41px}
.benchmark-detail{display:grid;grid-template-columns:65px 1fr;gap:6px;font-size:12px;line-height:1.45;margin-top:12px}.benchmark-detail b{font-weight:700;color:#33415b}.benchmark-detail p{font-size:12px;line-height:1.45;margin:0;color:#657792}
.benchmark-cards ul{margin:0;padding:0;list-style:none;font-size:12px;line-height:1.45;color:#657792}.benchmark-cards li{position:relative;padding-left:10px;margin:8px 0}.benchmark-cards li::before{content:'';position:absolute;left:0;top:7px;width:3px;height:3px;border-radius:50%;background:#8a98ac}
.benchmark-summary{position:absolute;left:19px;right:19px;bottom:16px;border-top:1px solid #edf0f5;padding-top:10px;font-size:10px;line-height:1.5;color:#7f8da3}
.evaluation-target{margin-top:19px;display:flex;align-items:center;gap:17px;background:#eef1f7;border-radius:10px;padding:15px 18px;font-size:13px;line-height:1.4;color:#657792}.evaluation-target b{color:#17233e;font-size:13px;white-space:nowrap}
</style>
