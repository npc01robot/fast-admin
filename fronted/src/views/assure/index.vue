<template>
  <el-card>
    <Dialog :visible="visible" :title="title" :id="id" @set-show="setShow" />
    <el-card shadow="never" style="margin-top: 1%">
      <h3>筛选项</h3>
      <el-form :inline="true">
        <el-form-item label="担保单位">
          <el-input placeholder="担保单位" clearable />
        </el-form-item>
        <el-form-item label="被担保单位">
          <el-input placeholder="被担保单位" clearable />
        </el-form-item>
        <el-form-item label="产权关系">
          <el-input placeholder="产权关系" clearable />
        </el-form-item>
        <el-form-item label="担保事项">
          <el-input placeholder="担保事项" clearable />
        </el-form-item>
        <el-form-item label="担保日期">
          <el-date-picker
            type="daterange"
            range-separator="至"
            start-placeholder="担保开始日期"
            end-placeholder="担保结束日期"
            clearable
          />
        </el-form-item>
      </el-form>
    </el-card>
    <el-card style="margin-top: 1%" shadow="never">
      <el-button @click="add">新增</el-button>
      <el-button :icon="Download" circle />
      <el-button :icon="Printer" circle />
      <el-table
        :data="tableData"
        ref="multipleTableRef"
        style="width: 100%; margin-top: 10px"
        @selection-change="handleSelectionChange"
        stripe
        :border="true"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column label="序号" type="index" width="50" />
        <el-table-column prop="name" label="担保单位名称" />
        <el-table-column prop="name" label="被担保单位名称" />
        <el-table-column
          prop="name"
          sortable
          label="担保单位与被担保单位的产权关系"
        />
        <el-table-column prop="name" label="担保事项（简要描述）" />
        <el-table-column prop="name" sortable label="备案金额" />
        <el-table-column prop="name" sortable label="实际担保金额" />
        <el-table-column prop="name" label="担保开始日期" />
        <el-table-column prop="name" label="担保结束日期" />
        <el-table-column prop="name" sortable label="综合成本" />
        <el-table-column prop="name" label="备注" />

        <el-table-column
          prop="name"
          label="操作"
          align="center"
          fixed="right"
          width="200px"
        >
          <template #default="scope">
            <el-button
              type="primary"
              :icon="Edit"
              circle
              @click="edit(scope.row.id)"
            />
            <el-button type="danger" :icon="Delete" circle />
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </el-card>
</template>
<script setup lang="ts">
import { Delete, Edit, Download, Printer } from "@element-plus/icons-vue";
import Dialog from "./dialog.vue";
import { ref } from "vue";
const visible = ref(false);
const title = ref("新增担保");
const id = ref(0);
import { useRoute } from "vue-router";
const route = useRoute();
console.log(route.query.id);
const tableData = [
  {
    name: 1
  }
];
const handleSelectionChange = () => {
  // 处理选择变化
};
const add = () => {
  visible.value = true;
};
const edit = val => {
  id.value = Number(val);
  title.value = "编辑担保";
  visible.value = true;
};

function setShow(val) {
  visible.value = val;
}
</script>
