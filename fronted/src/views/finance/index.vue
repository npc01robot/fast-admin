<script setup lang="ts">
import { AppServerSideGrid } from "@/views/components/ag-grid";
import { useFinanceHook } from "@/views/finance/hook";
const { componentRef, options } = useFinanceHook();
</script>

<template>
  <div class="main">
    <AppServerSideGrid ref="componentRef" :options="options" />
  </div>
</template>

<style scoped lang="scss"></style>
