<template>
  <el-dialog
    :model-value="props.visible"
    :title="props.title"
    width="30%"
    draggable
    :before-close="handleClose"
  >
    <el-form :inline="true">
      <el-form-item label="担保单位">
        <el-input
          v-model="drawForm.loan_amount"
          placeholder="担保单位"
          clearable
        />
      </el-form-item>
      <el-form-item label="被担保单位">
        <el-input
          v-model="drawForm.contract_rate"
          placeholder="被担保单位"
          clearable
        />
      </el-form-item>
    </el-form>
    <el-form :inline="true">
      <el-form-item label="产权关系">
        <el-input
          v-model="drawForm.loan_amount"
          placeholder="产权关系"
          clearable
        />
      </el-form-item>
      <el-form-item label="备案金额">
        <el-input v-model="drawForm.contract_rate" placeholder="备案金额" />
      </el-form-item>
    </el-form>
    <el-form :inline="true">
      <el-form-item label="实际担保金额">
        <el-input v-model="drawForm.contract_rate" placeholder="实际担保金额" />
      </el-form-item>
      <el-form-item label="综合成本">
        <el-input v-model="drawForm.contract_rate" placeholder="综合成本" />
      </el-form-item>
    </el-form>

    <el-form :inline="true">
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
    <el-form>
      <el-form-item label="担保事项">
        <el-input
          v-model="drawForm.contract_rate"
          placeholder="担保事项"
          clearable
          textarea
        />
      </el-form-item>
    </el-form>
    <el-form>
      <el-form-item label="备注">
        <el-input
          v-model="drawForm.contract_rate"
          placeholder="备注"
          clearable
          textarea
        />
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
const drawForm = reactive({
  loan_amount: "",
  contract_rate: "",
  allin_rate: "",
  cost_rate: "",
  actual_rate: "",
  guaranty_style: "",
  start_time: "",
  end_time: "",
  allocation: "",
  director_sign: "",
  funds_user: ""
});

const comfire = () => {
  console.log(drawForm);
};
const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: "新增担保"
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
