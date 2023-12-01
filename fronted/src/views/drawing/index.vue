<template>
  <el-card>
    <Dialog :visible="visible" :title="title" :id="id" @set-show="setShow" />
    <el-card shadow="never">
      <h3>融资情况</h3>
      <el-form :inline="true">
        <el-form-item label="贷款单位名称">
          <el-input
            disabled
            v-model="input1"
            placeholder="贷款单位名称"
            clearable
          />
        </el-form-item>
        <el-form-item label="贷款类型">
          <el-select disabled v-model="input1" multiple placeholder="贷款类型">
            <el-option label="是" value="true" />
            <el-option label="否" value="false" />
          </el-select>
        </el-form-item>
      </el-form>
      <el-form :inline="true">
        <el-form-item label="授信金融机构">
          <el-input
            disabled
            v-model="input1"
            placeholder="授信金融机构"
            clearable
          />
        </el-form-item>
        <el-form-item label="授信总金额">
          <el-input
            disabled
            v-model="input1"
            placeholder="授信总金额"
            clearable
          />
        </el-form-item>
        <el-form-item label="剩余可用授信额度">
          <el-input
            disabled
            v-model="input1"
            placeholder="剩余可用授信额度"
            clearable
          />
        </el-form-item>
        <el-form-item label="授信日期">
          <el-date-picker
            disabled
            v-model="input1"
            type="daterange"
            range-separator="至"
            start-placeholder="授信开始日期"
            end-placeholder="授信结束日期"
          />
        </el-form-item>
      </el-form>
      <el-form :inline="true">
        <el-form-item label="贷款单位是否已上会">
          <el-select disabled v-model="input1" placeholder="贷款单位是否已上会">
            <el-option label="是" value="true" />
            <el-option label="否" value="false" />
          </el-select>
        </el-form-item>
        <el-form-item label="集团党委会是否审议">
          <el-select disabled v-model="input1" placeholder="集团党委会是否审议">
            <el-option label="是" value="true" />
            <el-option label="否" value="false" />
          </el-select>
        </el-form-item>
        <el-form-item label="集团董事会是否审议">
          <el-select disabled v-model="input1" placeholder="集团董事会是否审议">
            <el-option label="是" value="true" />
            <el-option label="否" value="false" />
          </el-select>
        </el-form-item>
        <el-form-item label="是否已签署董事会决议">
          <el-select
            disabled
            v-model="input1"
            placeholder="是否已签署董事会决议"
          >
            <el-option label="是" value="true" />
            <el-option label="否" value="false" />
          </el-select>
        </el-form-item>
      </el-form>
      <el-form>
        <el-form-item label="备注" prop="desc" style="width: 55%">
          <el-input disabled v-model="input1" type="textarea" />
        </el-form-item>
      </el-form>
    </el-card>
    <el-card shadow="never" style="margin-top: 1%">
      <h3>筛选项</h3>
      <el-form :inline="true">
        <el-form-item label="担保方式">
          <el-input placeholder="担保方式" clearable />
        </el-form-item>
        <el-form-item label="资金实际使用人">
          <el-input placeholder="资金实际使用人" clearable />
        </el-form-item>
        <el-form-item label="是否配存业务">
          <el-select placeholder="是否配存业务">
            <el-option label="是" value="true" />
            <el-option label="否" value="false" />
          </el-select>
        </el-form-item>
        <el-form-item label="贷款日期">
          <el-date-picker
            type="daterange"
            range-separator="至"
            start-placeholder="贷款借款日"
            end-placeholder="贷款到期日"
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
        <el-table-column prop="name" sortable label="贷款金额" />
        <el-table-column prop="name" sortable label="合同利率" />
        <el-table-column
          prop="name"
          sortable
          label="综合利率（与银行商谈总成本）"
        />
        <el-table-column prop="name" sortable label="已做配存业务成本利率" />
        <el-table-column prop="name" sortable label="实际利率" />
        <el-table-column prop="name" label="担保方式" />
        <el-table-column prop="name" label="贷款借款日" />
        <el-table-column prop="name" label="贷款到期日" />
        <el-table-column prop="name" label="是否配存业务" />
        <el-table-column prop="name" label="资金实际使用人" />
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
const title = ref("新增贷款");
const id = ref(0);
const input1 = ref("1");
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
  title.value = "编辑贷款";
  visible.value = true;
};

function setShow(val) {
  visible.value = val;
}
</script>
