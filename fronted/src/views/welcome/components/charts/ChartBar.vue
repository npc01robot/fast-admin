<script setup lang="ts">
import { useDark, useECharts } from "@pureadmin/utils";
import { type PropType, ref, computed, watch, nextTick } from "vue";

const props = defineProps({
  repay: {
    type: Array as PropType<Array<number>>,
    default: () => []
  },
  interest: {
    type: Array as PropType<Array<number>>,
    default: () => []
  },
  date: {
    type: Array as PropType<Array<string>>,
    default: () => []
  }
});

const { isDark } = useDark();

const theme = computed(() => (isDark.value ? "dark" : "light"));

const chartRef = ref();
const { setOptions } = useECharts(chartRef, {
  theme
});

watch(
  () => props,
  async () => {
    await nextTick(); // 确保DOM更新完成后再执行
    setOptions({
      container: ".bar-card",
      color: ["#41b6ff", "#e85f33"],
      tooltip: {
        trigger: "axis",
        axisPointer: {
          type: "none"
        }
      },
      grid: {
        top: "20px",
        left: "50px",
        right: 0
      },
      legend: {
        data: ["还款", "付息"],
        textStyle: {
          color: "#606266",
          fontSize: "0.875rem"
        },
        bottom: 0
      },
      xAxis: [
        {
          type: "category",
          data: props.date,
          axisLabel: {
            fontSize: "0.875rem"
          },
          axisPointer: {
            type: "shadow"
          }
        }
      ],
      yAxis: [
        {
          type: "value",
          axisLabel: {
            fontSize: "0.875rem"
          },
          splitLine: {
            show: false // 去网格线
          }
          // name: "单位: 个"
        }
      ],
      series: [
        {
          name: "还款",
          type: "bar",
          barWidth: 10,
          itemStyle: {
            color: "#41b6ff",
            borderRadius: [10, 10, 0, 0]
          },
          data: props.repay
        },
        {
          name: "付息",
          type: "bar",
          barWidth: 10,
          itemStyle: {
            color: "#e86033ce",
            borderRadius: [10, 10, 0, 0]
          },
          data: props.interest
        }
      ]
    });
  },
  {
    deep: true,
    immediate: true
  }
);
</script>

<template>
  <div ref="chartRef" style="width: 100%; height: 365px" />
</template>
