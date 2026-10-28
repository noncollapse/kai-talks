<script setup>
const base = import.meta.env.BASE_URL
</script>

<template>
  <div class="prior-product">
    <div class="prior-product-copy">
      <h2>TabPFN-3.5</h2>
      <div class="prior-channels"><span>Python</span><span>API</span></div>
    </div>
    <a href="https://priorlabs.ai/tabpfn-3-5" class="prior-demo">
      <img :src="`${base}figs/priorlabs-tabpfn-product.jpg`" alt="Official TabPFN-3.5 product demo: a customer table and a Predict button for churn prediction" />
      <small>From Prior Labs’ official product demo</small>
    </a>
  </div>
  <div class="prior-milestones">
    <a href="https://www.balderton.com/news/prior-labs-raises-e9m-to-revolutionise-how-businesses-interact-with-their-tabular-data/">
      <strong>€9M</strong><b>Pre-seed funding</b><span>February 2025 · led by Balderton</span>
    </a>
    <a href="https://news.sap.com/2026/07/sap-completes-prior-labs-acquisition/">
      <strong>€1B+</strong><b>Committed by SAP</b><span>Investment over four years</span>
    </a>
    <a href="https://news.sap.com/2026/07/sap-completes-prior-labs-acquisition/">
      <strong class="prior-sap">SAP</strong><b>Acquisition completed</b><span>17 July 2026 · operates independently</span>
    </a>
  </div>
</template>

<style scoped>
.prior-product{display:grid;grid-template-columns:270px 1fr;gap:28px;align-items:center;margin-top:30px}
.prior-product-label{font-size:11px;letter-spacing:.1em;font-weight:800;color:#8490a4}
.prior-product h2{font-size:36px;letter-spacing:-1.2px;font-weight:800;margin:10px 0 8px;color:#17233e}
.prior-product-copy p{font-size:19px;color:#64748b;margin:0 0 22px}
.prior-channels{display:flex;gap:8px}.prior-channels span{font-size:12px;color:#4263eb;background:#eef2ff;padding:6px 10px;border-radius:6px}
.prior-demo{display:block;border:0!important;text-decoration:none!important;min-width:0}
.prior-demo img{display:block;width:100%;border-radius:13px;background:#000;box-shadow:0 14px 30px #17233e18}
.prior-demo small{display:block;text-align:right;font-size:9px;color:#8490a4;margin-top:8px}
.prior-milestones{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px;margin-top:36px}
.prior-milestones a{display:flex;flex-direction:column;border:0!important;border-top:1px solid #dce4f2!important;padding-top:17px;text-decoration:none!important}
.prior-milestones strong{font-family:Manrope,sans-serif;font-size:42px;line-height:1.1;font-weight:800;letter-spacing:-1.5px;color:#4263eb}
.prior-milestones a:nth-child(2) strong{color:#0b9687}.prior-milestones .prior-sap{color:#17233e}
.prior-milestones b{font-size:17px;color:#17233e;margin-top:11px;font-weight:700}
.prior-milestones span{font-size:11px;color:#8490a4;margin-top:7px}
</style>
