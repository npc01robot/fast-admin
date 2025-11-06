<script setup lang="ts">
import { ref, computed } from "vue";
import { useDark, useECharts } from "@pureadmin/utils";
import { any } from "vue-types";

const props = defineProps({
  title: {
    type: String,
    default: ""
  },
  subtext: {
    type: String,
    default: ""
  },
  name: {
    type: String,
    default: ""
  },
  data: {
    type: Array as () => any[],
    default: () => []
  },
  amount: {
    type: Number,
    default: 0
  }
});

const { isDark } = useDark();

const theme = computed(() => (isDark.value ? "dark" : "light"));

const chartRef = ref();
const { setOptions } = useECharts(chartRef, {
  theme,
  renderer: "svg"
});

setOptions({
  container: ".pie-card",
  title: {
    text: props.title,
    subtext: props.subtext,
    left: "center"
  },
  tooltip: {
    trigger: "item",
    position: ["40%","85%"],
    formatter: function (params) {
      if (props.amount === 0) {
        return `${params.name}: ${params.value} (${params.percent.toFixed(2)}%)`;
      } else {
        return `${params.name}: ${params.value} (${params.percent.toFixed(2)}%)<br/>占融资总额 (${((params.value / props.amount) * 100).toFixed(2)}%)`;
      }
    }
  },
  // legend: {
  //   orient: "vertical",
  //   left: "left"
  // },
  series: [
    {
      name: props.name,
      type: "pie",
      radius: "55%",
      data: props.data,
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0
        }
      }
    }
  ]
});
</script>

<template>
  <div ref="chartRef" style="width: 100%; height: 365px" />
</template>
