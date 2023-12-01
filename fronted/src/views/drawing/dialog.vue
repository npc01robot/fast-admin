<template>
  <el-dialog
    :model-value="props.visible"
    :title="props.title"
    width="30%"
    draggable
    :before-close="handleClose"
  >
    <el-form :inline="true">
      <el-form-item label="贷款金额">
        <el-input
          v-model="drawForm.loan_amount"
          placeholder="贷款金额"
          clearable
        />
      </el-form-item>
      <el-form-item label="合同利率">
        <el-input
          v-model="drawForm.contract_rate"
          placeholder="合同利率"
          clearable
        />
      </el-form-item>
    </el-form>
    <el-form :inline="true">
      <el-form-item label="综合利率">
        <el-input
          v-model="drawForm.loan_amount"
          placeholder="综合利率"
          clearable
        />
      </el-form-item>
      <el-form-item label="成本利率">
        <el-input
          v-model="drawForm.contract_rate"
          placeholder="成本利率"
          clearable
        />
      </el-form-item>
    </el-form>
    <el-form :inline="true">
      <el-form-item label="实际利率">
        <el-input
          v-model="drawForm.contract_rate"
          placeholder="实际利率"
          readonly
        />
      </el-form-item>
    </el-form>
    <el-form :inline="true">
      <el-form-item label="担保方式">
        <el-select v-model="drawForm.contract_rate" placeholder="担保方式">
          <el-option label="是" value="true" />
          <el-option label="否" value="false" />
        </el-select>
      </el-form-item>
      <el-form-item label="是否配存业务">
        <el-select v-model="drawForm.contract_rate" placeholder="担保方式">
          <el-option label="是" value="true" />
          <el-option label="否" value="false" />
        </el-select>
      </el-form-item>
    </el-form>

    <el-form :inline="true">
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
    <el-form :inline="true">
      <el-form-item label="资金实际使用人">
        <el-input
          v-model="drawForm.contract_rate"
          placeholder="资金实际使用人"
          clearable
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
    default: "新增贷款"
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
