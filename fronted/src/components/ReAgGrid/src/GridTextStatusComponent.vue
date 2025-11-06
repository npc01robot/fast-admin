<template>
  <div
    class="ag-status-name-value ag-status-panel"
    :class="{ 'ag-hidden': hidden }"
  >
    <span v-if="params?.label" ref="eLabel" class="ag-status-name"
      >{{ params?.label }}:&nbsp;</span
    >
    <span ref="eValue" class="ag-status-name-value-value">{{ value }}</span>
  </div>
</template>

<script setup lang="ts">
import { IStatusPanelParams } from "ag-grid-community";
import { ComputedRef, Ref, computed, defineProps } from "vue";

const props = defineProps({
  params: {
    type: Object as () => IStatusPanelParams & {
      label: string | Ref<string> | ComputedRef<string>;
      value: number | string | Ref<string> | ComputedRef<string>;
      hidden?: boolean | Ref<boolean> | ComputedRef<boolean>;
    },
    required: true
  }
});

const value = computed(() => {
  let val = props.params.value as any;
  return val?.value ?? val;
});
const hidden = computed(() => {
  let hidden = props.params.hidden as any;
  return hidden?.value ?? hidden;
});
</script>
