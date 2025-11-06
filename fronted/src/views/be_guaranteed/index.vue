<script setup lang="ts">
import { useBeGuaranteed } from "@/views/be_guaranteed/hook";
import { AppServerSideGrid } from "@/components/ReAgGrid";
const { componentRef, options } = useBeGuaranteed();
</script>

<template>
  <div class="main">
    <AppServerSideGrid ref="componentRef" :options="options" />
  </div>
</template>

<style scoped lang="scss"></style>
