<script setup lang="ts">
import { useAgGrid } from "@/views/aggrid/hook";
import { AppServerSideGrid } from "@/views/components/ag-grid";
const { componentRef, options } = useAgGrid();
</script>

<template>
  <div class="main">
    <AppServerSideGrid ref="componentRef" :options="options" />
  </div>
</template>

<style scoped lang="scss"></style>
