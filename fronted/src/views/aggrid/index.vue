<script setup lang="ts">
import { useAgGrid } from "@/views/aggrid/hook";
import { AgGridVue } from "ag-grid-vue3";
import "ag-grid-community/styles/ag-grid.css"; // Mandatory CSS required by the Data Grid
import "ag-grid-community/styles/ag-theme-quartz.css"; // Optional Theme applied to the Data Grid

const {
  pagination,
  paginationPageSize,
  paginationPageSizeSelector,
  gridOptions,
  rowData,
  columnDefs,
  onSearch,
  onGridReady
} = useAgGrid();
</script>

<template>
  <div class="main">
    <ag-grid-vue
      :columnDefs="columnDefs"
      :rowData="rowData"
      :pagination="true"
      :paginationPageSizeSelector="paginationPageSizeSelector"
      :paginationPageSize="paginationPageSize"
      style="height: 500px"
      class="ag-theme-quartz"
      :gridOptions="gridOptions"
      @grid-ready="onGridReady"
    />
  </div>
</template>

<style scoped lang="scss"></style>
