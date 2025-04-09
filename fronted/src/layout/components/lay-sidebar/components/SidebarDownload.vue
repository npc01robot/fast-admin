<script setup lang="ts">
import Download from "@iconify-icons/ep/download";
import { reactive, ref, toRaw } from "vue";
import type { ComponentSize } from "element-plus";
import { exportList, exportType } from "@/api/file";
import { hasAuth } from "@/router/utils";

const form = reactive({
  type: "",
  status: "",
  page: 1,
  page_size: 10,
  all: false
});
const isShow = ref(false);
const statuses = [
  { label: "待处理", value: 0 },
  { label: "处理完成", value: 1 },
  { label: "处理中", value: 2 },
  { label: "处理异常", value: 3 }
];

const types = ref<any[]>([]);
const tableData = ref<any[]>([]);
const total = ref(0);
const pageCount = ref(0);

const size = ref<ComponentSize>("default");
const background = ref(false);
const disabled = ref(false);

const handleSizeChange = (val: number) => {
  form.page_size = val;
  onSearch();
};
const handleCurrentChange = (val: number) => {
  form.page = val;
  onSearch();
};
async function onSearch(showAll: boolean = false) {
  form.all = showAll;
  await exportList({ params: form }).then(res => {
    tableData.value = res.data.list;
    pageCount.value = res.data.pageCount;
    form.page = res.data.page;
    total.value = res.data.total;
  });
}
async function getType() {
  await exportType().then(res => {
    types.value = res.data;
  });
  console.log(types.value);
}

function loadData() {
  isShow.value = isShow.value ? false : true;
  onSearch();
  getType();
}

const download = (url: string) => {
  window.open(url, "_blank");
};
</script>

<template>
  <span class="fullscreen-icon navbar-bg-hover" @click="loadData()">
    <IconifyIconOffline :icon="Download" />
  </span>
  <el-dialog v-model="isShow" title="下载列表" width="50%">
    <span>任务状态：</span>
    <el-select
      v-model="form.status"
      placeholder="请选择"
      size="large"
      style="width: 240px"
    >
      <el-option
        v-for="item in statuses"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
    <span style="margin-left: 40px">任务类型：</span>
    <el-select
      v-model="form.type"
      placeholder="请选择"
      size="large"
      style="width: 240px"
    >
      <el-option
        v-for="item in types"
        :key="item.value"
        :label="item.label"
        :value="item.value"
      />
    </el-select>
    <el-button type="primary" style="margin-left: 40px" @click="onSearch()"
      >查询</el-button
    >
    <Auth>
      <el-button
        v-if="hasAuth('btn_show')"
        type="primary"
        style="margin-left: 40px"
        @click="onSearch(true)"
        >查询全部</el-button
      >
    </Auth>
    <el-table :data="tableData" height="400" style="width: 100%">
      <el-table-column
        prop="module"
        label="任务类型"
        width="180"
        align="center"
      />
      <el-table-column
        prop="status"
        label="任务状态"
        width="180"
        align="center"
      >
        <template v-slot="scope">{{
          scope.row.status === 0
            ? "待处理"
            : scope.row.status === 1
              ? "处理完成"
              : scope.row.status === 2
                ? "处理中"
                : "处理异常"
        }}</template>
      </el-table-column>
      <el-table-column prop="create_time" label="创建时间" align="center">
        <template v-slot="scope">{{
          scope.row.create_time
            ? scope.row.create_time.replace(/T/g, " ").split(".")[0]
            : ""
        }}</template>
      </el-table-column>
      <el-table-column
        prop="complete_result"
        label="处理结果"
        width="180"
        align="center"
      >
        <template v-slot="scope">{{
          scope.row.error_msg ? scope.row.error_msg : scope.row.complete_result
        }}</template>
      </el-table-column>
      <el-table-column
        prop="complete_path"
        label="处理结果下载"
        width="180"
        align="center"
      >
        <template v-slot="scope">
          <el-button type="primary" @click="download(scope.row.complete_path)"
            >下载</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      v-model:current-page="form.page"
      v-model:page-size="form.page_size"
      style="margin-top: 20px; justify-content: flex-end"
      :page-sizes="[10, 30, 50, 100]"
      :size="size"
      :disabled="disabled"
      :background="background"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
    <!--  table  -->
  </el-dialog>
</template>

<style scoped>
.demo-pagination-block + .demo-pagination-block {
  margin-top: 20px;
}

.demo-pagination-block .demonstration {
  margin-bottom: 16px;
}
</style>
