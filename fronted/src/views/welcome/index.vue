<script setup lang="ts">
import { ref } from "vue";
import ReCol from "@/components/ReCol";
import { useDark } from "./utils";
import WelcomeTable from "./components/table/index.vue";
import { ReNormalCountTo } from "@/components/ReCountTo";
import { ChartBar, ChartLine, ChartPie } from "./components/charts";
import { chartData, pieData, barChartData } from "./data";

defineOptions({
  name: "Welcome"
});
const isLoading = ref(false);
const { isDark } = useDark();
</script>

<template>
  <div>
    <el-row :gutter="24" justify="space-around">
      <re-col
        v-for="(item, index) in chartData"
        :key="item.dataKey"
        v-motion
        class="mb-[18px]"
        :value="6"
        :md="12"
        :sm="12"
        :xs="24"
        :initial="{
          opacity: 0,
          y: 100
        }"
        :enter="{
          opacity: 1,
          y: 0,
          transition: {
            delay: 80 * (index + 1)
          }
        }"
      >
        <el-card class="line-card" shadow="never">
          <div class="flex justify-between">
            <span class="text-md font-medium">
              {{ item.name }}
            </span>
            <div
              class="w-8 h-8 flex justify-center items-center rounded-md"
              :style="{
                backgroundColor: isDark ? 'transparent' : item.bgColor
              }"
            >
              <IconifyIconOffline
                :icon="item.icon"
                :color="item.color"
                width="18"
              />
            </div>
          </div>
          <div class="flex justify-between items-start mt-3">
            <div class="w-1/2">
              <ReNormalCountTo
                :duration="item.duration"
                :fontSize="'1.6em'"
                :startVal="100"
                :endVal="item.value"
              />
              <p class="font-medium text-green-500">{{ item.percent }}</p>
            </div>
            <ChartLine class="!w-1/2" :color="item.color" :data="item.data" />
          </div>
        </el-card>
      </re-col>

      <re-col
        v-for="(item, index) in pieData"
        :key="item.dataKey"
        v-motion
        class="mb-[18px]"
        :value="6"
        :md="12"
        :sm="12"
        :xs="24"
        :initial="{
          opacity: 0,
          y: 100
        }"
        :enter="{
          opacity: 1,
          y: 0,
          transition: {
            delay: 80 * (index + 1)
          }
        }"
      >
        <el-card class="pie-card" shadow="never">
          <div class="flex justify-between items-start mt-3">
            <ChartPie
              :data="item.data"
              :title="item.title"
              :amount="item.amount"
            />
          </div>
        </el-card>
      </re-col>
      <re-col
        v-motion
        class="mb-[18px]"
        :value="24"
        :xs="24"
        :initial="{
          opacity: 0,
          y: 100
        }"
        :enter="{
          opacity: 1,
          y: 0,
          transition: {
            delay: 400
          }
        }"
      >
        <el-card class="bar-card" shadow="never">
          <div class="flex justify-between">
            <span class="text-md font-medium">还款付息</span>
          </div>
          <div class="flex justify-between items-start mt-3">
            <ChartBar
              :date="barChartData.date"
              :interest="barChartData.interest"
              :repay="barChartData.repay"
            />
          </div>
        </el-card>
      </re-col>
      <re-col
        v-motion
        class="mb-[18px]"
        :value="24"
        :xs="24"
        :initial="{
          opacity: 0,
          y: 100
        }"
        :enter="{
          opacity: 1,
          y: 0,
          transition: {
            delay: 560
          }
        }"
      >
        <el-card shadow="never" class="h-[580px]">
          <div class="flex justify-between">
            <span class="text-md font-medium">即将到期融资</span>
          </div>
          <WelcomeTable class="mt-3" />
        </el-card>
      </re-col>
    </el-row>
  </div>
</template>

<style lang="scss" scoped>
:deep(.echarts-tooltip) {
  z-index: 9999 !important;
}
:deep(.el-card) {
  --el-card-border-color: none;
  overflow: visible !important; // 关键：取消 overflow: hidden 的默认行为
  position: relative; // 为子元素层级提供参考
  z-index: 1; // 卡片本身层级较低，不影响 tooltip
  /* 解决概率进度条宽度 */
  .el-progress--line {
    width: 85%;
  }

  /* 解决概率进度条字体大小 */
  .el-progress-bar__innerText {
    font-size: 15px;
  }

  /* 隐藏 el-scrollbar 滚动条 */
  .el-scrollbar__bar {
    display: none;
  }

  /* el-timeline 每一项上下、左右边距 */
  .el-timeline-item {
    margin: 0 6px;
  }
}

.main-content {
  margin: 20px 20px 0 !important;
}
</style>
