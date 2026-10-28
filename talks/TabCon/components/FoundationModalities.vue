<script setup>
const base = import.meta.env.BASE_URL
</script>

<template>
  <div class="modalities">
    <section class="modality">
      <div class="modality-heading">Vision foundation models</div>
      <img :src="`${base}figs/vision-foundation-cute.png`" alt="A curious kitten and a friendly camera looking at a butterfly photo" />
      <p>Image generation, segmentation, and more.</p>
    </section>
    <section class="modality">
      <div class="modality-heading">Language foundation models</div>
      <img :src="`${base}figs/language-foundation-cute.png`" alt="A friendly robot chatting with a kitten through speech bubbles" />
      <p>Dialogue, summarization, translation, and more.</p>
    </section>
  </div>
</template>

<style scoped>
.modalities{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:20px}
.modality{border:1px solid #dfe5f1;border-radius:18px;padding:20px 24px;background:white}
.modality-heading{font-size:22px;font-weight:800;color:#17233e;margin-bottom:12px}
.modality img{display:block;width:100%;height:180px;object-fit:contain;border-radius:12px}
.modality p{font-size:16px;line-height:1.5;color:#58677e;margin:14px 0 0}
</style>
