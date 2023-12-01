<template>
  <el-card shadow="never">
    <Dialog :visible="visible" :title="title" :id="id" @set-show="setShow" />
    <el-card shadow="never">
      <h3>筛选项</h3>
      <el-form :inline="true">
        <el-form-item label="贷款单位名称">
          <el-input placeholder="贷款单位名称" clearable />
        </el-form-item>
        <el-form-item label="贷款类型">
          <el-select multiple placeholder="贷款类型">
            <el-option label="是" value="true" />
            <el-option label="否" value="false" />
          </el-select>
        </el-form-item>
        <el-form-item label="授信金融机构">
          <el-input placeholder="授信金融机构" clearable />
        </el-form-item>
        <el-form-item label="内部报批进度">
          <el-select multiple placeholder="内部报批进度">
            <el-option label="是" value="true" />
            <el-option label="否" value="false" />
          </el-select>
        </el-form-item>
        <el-form-item label="授信日期">
          <el-date-picker
            type="daterange"
            range-separator="至"
            start-placeholder="授信开始日期"
            end-placeholder="授信结束日期"
            clearable
          />
        </el-form-item>
      </el-form>
    </el-card>
    <el-card shadow="never" style="margin-top: 1%">
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
        <el-table-column prop="name" label="贷款单位名称" align="center" />
        <el-table-column prop="name" label="贷款类型" align="center">
          <template #default="scope">
            <el-tag>{{ scope.row.name }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="授信金融机构" align="center" />
        <el-table-column label="授信情况" align="center">
          <el-table-column prop="name" label="授信总金额" align="center" />
          <el-table-column prop="name" label="授信开始日期" align="center" />
          <el-table-column prop="name" label="授信到期日期" align="center" />
        </el-table-column>
        <el-table-column label="内部报批进度" align="center">
          <el-table-column
            prop="name"
            label="贷款单位是否已上会"
            align="center"
          />
          <el-table-column
            prop="name"
            label="集团党委会是否审议"
            align="center"
          />
          <el-table-column
            prop="name"
            label="集团董事会是否审议"
            align="center"
          />
          <el-table-column
            prop="name"
            label="是否已签署董事会决议"
            align="center"
          />
        </el-table-column>
        <el-table-column prop="name" label="剩余可用授信额度" align="center" />
        <el-table-column prop="name" label="备    注" align="center" />
        <el-table-column
          prop="name"
          label="操作"
          align="center"
          fixed="right"
          width="200px"
        >
          <template #default="scope">
            <el-button
              type="success"
              :icon="Search"
              circle
              @click="
                router.push({ name: 'drawing', query: { id: scope.row.id } })
              "
            />
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
import {
  Delete,
  Edit,
  Search,
  Download,
  Printer
} from "@element-plus/icons-vue";
import { ref } from "vue";
import { useRouter } from "vue-router";
import Dialog from "./dialog.vue";
const visible = ref(false);
const title = ref("新增融资");
const id = ref(0);
const router = useRouter();
const tableData = [
  {
    id: 1,
    name: "1",
    label: "1",
    credit_name: "1",
    credit_sum: "1",
    credit_avail: "1",
    date: "1",
    loan_unit: "1",
    party_group: "1",
    director_group: "1",
    director_sign: "1",
    desc: "1"
  }
];
const add = () => {
  visible.value = true;
};
const edit = val => {
  id.value = Number(val);
  title.value = "编辑融资";
  visible.value = true;
};

const handleSelectionChange = () => {
  // 处理选择变化
};
function setShow(val) {
  visible.value = val;
}
</script>
