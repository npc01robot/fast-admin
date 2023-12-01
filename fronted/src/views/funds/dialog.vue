<template>
  <el-dialog
    :modal="props.visible"
    :title="props.title"
    width="30%"
    draggable
    :before-close="handleClose"
  >
    <el-form :inline="true">
      <el-form-item label="贷款单位名称">
        <el-input
          v-model="fundsForm.name"
          placeholder="贷款单位名称"
          clearable
        />
      </el-form-item>
      <el-form-item label="贷款类型">
        <el-select v-model="fundsForm.label" multiple placeholder="贷款类型">
          <el-option label="是" value="true" />
          <el-option label="否" value="false" />
        </el-select>
      </el-form-item>
    </el-form>
    <el-form :inline="true">
      <el-form-item label="授信金融机构">
        <el-input
          v-model="fundsForm.credit_name"
          placeholder="授信金融机构"
          clearable
        />
      </el-form-item>
      <el-form-item label="授信总金额">
        <el-input
          v-model="fundsForm.credit_sum"
          placeholder="授信总金额"
          clearable
        />
      </el-form-item>
      <el-form-item label="剩余可用授信额度">
        <el-input
          v-model="fundsForm.credit_avail"
          placeholder="剩余可用授信额度"
          clearable
        />
      </el-form-item>
      <el-form-item label="授信日期">
        <el-date-picker
          v-model="fundsForm.date"
          type="daterange"
          range-separator="至"
          start-placeholder="授信开始日期"
          end-placeholder="授信结束日期"
        />
      </el-form-item>
    </el-form>
    <el-form :inline="true">
      <el-form-item label="贷款单位是否已上会">
        <el-select
          v-model="fundsForm.loan_unit"
          placeholder="贷款单位是否已上会"
        >
          <el-option label="是" value="true" />
          <el-option label="否" value="false" />
        </el-select>
      </el-form-item>
      <el-form-item label="集团党委会是否审议">
        <el-select
          v-model="fundsForm.party_group"
          placeholder="集团党委会是否审议"
        >
          <el-option label="是" value="true" />
          <el-option label="否" value="false" />
        </el-select>
      </el-form-item>
      <el-form-item label="集团董事会是否审议">
        <el-select
          v-model="fundsForm.director_group"
          placeholder="集团董事会是否审议"
        >
          <el-option label="是" value="true" />
          <el-option label="否" value="false" />
        </el-select>
      </el-form-item>
      <el-form-item label="是否已签署董事会决议">
        <el-select
          v-model="fundsForm.director_sign"
          placeholder="是否已签署董事会决议"
        >
          <el-option label="是" value="true" />
          <el-option label="否" value="false" />
        </el-select>
      </el-form-item>
    </el-form>
    <el-form>
      <el-form-item label="备注" prop="desc" style="width: 55%">
        <el-input v-model="fundsForm.desc" type="textarea" />
      </el-form-item>
    </el-form>
    <el-form>
      <el-form-item style="margin-left: 45%">
        <el-button type="primary" @click="comfire"> 提交 </el-button>
        <el-button @click="handleClose">取消</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script setup lang="ts">
import { reactive } from "vue";
const fundsForm = reactive({
  name: "",
  label: "",
  credit_name: "",
  credit_sum: "",
  credit_avail: "",
  date: "",
  loan_unit: "",
  party_group: "",
  director_group: "",
  director_sign: "",
  desc: ""
});

const comfire = () => {
  console.log(fundsForm);
};
const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: "新增融资"
  },
  id: {
    type: Number,
    default: 0
  }
});

const emits = defineEmits(["set-show"]);

function handleClose() {
  //关闭对话框时并向子组件传参
  emits("set-show", false);
}
</script>
