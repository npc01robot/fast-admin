<script setup lang="ts">
import { AppTinyGrid } from "@/views/components/ag-grid";
import { useCompositeCostHook } from "@/views/composite_cost/hook";
const { componentRef, options } = useCompositeCostHook();
</script>

<template>
  <div class="main">
    <AppTinyGrid ref="componentRef" :options="options" />
  </div>
</template>

<style scoped lang="scss"></style>
