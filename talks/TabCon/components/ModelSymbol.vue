<script setup>
defineProps({ color:{type:String,default:'#4263eb'} })
</script>
<template>
  <svg class="model-symbol" viewBox="0 0 110 86" :style="{color}" aria-hidden="true">
    <rect x="19" y="4" width="84" height="62" rx="9" fill="currentColor" :style="{opacity:.13}" stroke="currentColor"/>
    <rect x="12" y="11" width="84" height="62" rx="9" fill="white" stroke="currentColor" stroke-opacity=".45"/>
    <rect x="5" y="18" width="84" height="62" rx="9" fill="white" stroke="currentColor" stroke-width="1.5"/>
    <g fill="none" stroke="currentColor" stroke-opacity=".45" stroke-width="1.4"><path d="M21 32L47 37L73 32M21 32L47 62L73 32M21 67L47 37L73 67M21 67L47 62L73 67"/></g>
    <g fill="currentColor"><circle cx="21" cy="32" r="3.5"/><circle cx="21" cy="67" r="3.5"/><circle cx="47" cy="37" r="3.5"/><circle cx="47" cy="62" r="3.5"/><circle cx="73" cy="32" r="3.5"/><circle cx="73" cy="67" r="3.5"/></g>
  </svg>
</template>
<style scoped>.model-symbol{display:block;width:100%;height:100%}</style>
