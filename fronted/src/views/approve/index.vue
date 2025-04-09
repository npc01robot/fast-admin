<script setup lang="ts">
import { AppServerSideGrid } from "@/views/components/ag-grid";
import { useApprove } from "@/views/approve/hook";
const { componentRef, options } = useApprove();
</script>

<template>
  <div class="main">
    <AppServerSideGrid ref="componentRef" :options="options" />
  </div>
</template>

<style scoped lang="scss"></style>
