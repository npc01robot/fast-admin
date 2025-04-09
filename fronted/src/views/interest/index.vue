<script setup lang="ts">
import { AppServerSideGrid } from "@/views/components/ag-grid";
import { useRepayInterest } from "@/views/interest/hook";
const { componentRef, options } = useRepayInterest();
</script>

<template>
  <div class="main">
    <AppServerSideGrid ref="componentRef" :options="options" />
  </div>
</template>

<style scoped lang="scss"></style>
