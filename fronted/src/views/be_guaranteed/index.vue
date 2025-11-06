<script setup lang="ts">
import { AppServerSideGrid } from "@/views/components/ag-grid";
import { useBeGuaranteed } from "@/views/be_guaranteed/hook";
const { componentRef, options } = useBeGuaranteed();
</script>

<template>
  <div class="main">
    <AppServerSideGrid ref="componentRef" :options="options" />
  </div>
</template>

<style scoped lang="scss"></style>
