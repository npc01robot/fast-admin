<script setup lang="ts">
import { AppServerSideGrid } from "@/views/components/ag-grid";
import { useGuarantee } from "@/views/guarantee/hook";
const { componentRef, options } = useGuarantee();
</script>

<template>
  <div class="main">
    <AppServerSideGrid ref="componentRef" :options="options" />
  </div>
</template>

<style scoped lang="scss"></style>
