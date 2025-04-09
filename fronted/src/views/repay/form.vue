<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { formRules } from "@/views/guarantee/rule";
import { useRoute } from "vue-router";
import accounting from "accounting";

import { message } from "@/utils/message";
import router from "@/router";
import { useUserStoreHook } from "@/store/modules/user";
import {
  createLoanRepay,
  getLoanDetail,
  getLoanRepayDetail,
  updateLoanRepay
} from "@/api/loan";

defineOptions({
  name: "GuaranteeDetail"
});
const loading = ref(false);
const route = useRoute();
const id = route.query?.id;
const loanId = route.query?.loanId;
const isEdited = ref(false);
isEdited.value = !id;
const title = id ? "还本详情" : "新增还本";
const showRepay = !!id;
const loanDetail = ref<any>({});

const originalFormData = ref({
  id: "",
  loan: loanId,
  repay_date: "",
  repay_amount: "",
  voucher_number: "",
  repay_source: "",
  remark: ""
});
const formData = ref({ ...originalFormData.value });
onMounted(() => {
  if (id) {
    loading.value = true;
    getLoanRepayDetail(String(id)).then(res => {
      Object.assign(originalFormData.value, res.data);
      Object.assign(formData.value, res.data);
      getLoanDetail(String(formData.value.loan)).then(res => {
        loanDetail.value = res.data;
        loading.value = false;
      });
    });
  }
  if (loanId) {
    loading.value = true;

    getLoanDetail(String(loanId)).then(res => {
      loading.value = false;
      loanDetail.value = res.data;
    });
  }
});

// 使用 Object.assign 合并props和默认值

const ruleFormRef = ref();

const onEdit = () => {
  isEdited.value = true;
};

const onCancel = () => {
  isEdited.value = false;
  formData.value = { ...originalFormData.value };
};

const onReset = () => {
  formData.value = { ...originalFormData.value };
};

const onSubmit = () => {
  formData.value.repay_amount = accounting.unformat(
    formData.value.repay_amount
  );
  if (id) {
    updateLoanRepay({ data: formData.value }, String(id)).then(res => {
      if (res && res.success) {
        isEdited.value = false;
        originalFormData.value = { ...formData.value };
        message("还款信息修改成功", { type: "success" });
        router.push({ name: "Repay" });
      } else {
        message("还款信息修改失败!" + res.msg, { type: "error" });
      }
    });
  } else {
    createLoanRepay({ data: formData.value }).then(res => {
      console.log(useUserStoreHook().username);
      if (res && res.success) {
        isEdited.value = false;
        originalFormData.value = { ...formData.value };
        message("还款信息新增成功", { type: "success" });
        router.push({ name: "Repay" });
      } else {
        message("还款信息新增失败!" + res.msg, { type: "error" });
      }
    });
  }
};
</script>

<template>
  <el-card shadow="never">
    <h1>{{ title }}</h1>
    <div style="margin-top: 1rem">
      <el-button
        v-show="!isEdited"
        size="default"
        type="primary"
        @click="onEdit"
        >编辑</el-button
      >
      <el-button
        v-show="isEdited"
        size="default"
        type="primary"
        @click="onSubmit"
        >保存</el-button
      >
      <el-button v-show="isEdited" size="default" @click="onReset"
        >重置</el-button
      >
      <el-button v-show="isEdited && showRepay" size="default" @click="onCancel"
        >取消</el-button
      >
    </div>
    <el-divider />
    <el-form
      ref="ruleFormRef"
      :model="loanDetail"
      :rules="formRules"
      label-width="150px"
      class="form-inline"
      :disabled="!isEdited"
      :inline="true"
    >
      <el-form-item label="贷款名称:">
        {{ loanDetail.name }}
      </el-form-item>
      <el-form-item label="贷款单位:">
        {{ loanDetail.loan_unit }}
      </el-form-item>
      <el-form-item label="贷款类型:">
        {{ loanDetail.type }}
      </el-form-item>
      <el-form-item label="签订日期:">
        {{ loanDetail.sign_date }}
      </el-form-item>
      <el-form-item label="贷款金额:">
        {{ accounting.formatMoney(loanDetail.loan_amount, "￥", 2) }}
      </el-form-item>
      <el-form-item label="已还金额:">
        {{ accounting.formatMoney(loanDetail.repay_amount, "￥", 2) }}
      </el-form-item>
      <el-form-item label="到期金额:">
        {{ accounting.formatMoney(loanDetail.loan_balance, "￥", 2) }}
      </el-form-item>
      <el-form-item label="付息金额:">
        {{ accounting.formatMoney(loanDetail.actual_interest, "￥", 2) }}
      </el-form-item>
      <el-form-item label="已还付息:">
        {{ accounting.formatMoney(loanDetail.repay_interest, "￥", 2) }}
      </el-form-item>
    </el-form>
    <el-divider />
    <el-form
      ref="ruleFormRef"
      :model="formData"
      :rules="formRules"
      label-width="150px"
      class="form-inline"
      :disabled="!isEdited"
      :inline="true"
    >
      <el-form-item label="还款日期:">
        <el-date-picker
          v-model="formData.repay_date"
          type="date"
          placeholder="选择日期"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      <el-form-item label="还款金额:">
        <el-input
          v-model="formData.repay_amount"
          placeholder="请输入还款金额"
          :formatter="value => `${accounting.formatMoney(value, '￥', 2)}`"
        />
      </el-form-item>
      <el-form-item label="会计凭证号:">
        <el-input
          v-model="formData.voucher_number"
          placeholder="请输入会计凭证号"
        />
      </el-form-item>
      <el-form-item label="还款来源:">
        <el-input
          v-model="formData.repay_source"
          placeholder="请输入还款来源"
        />
      </el-form-item>
      <el-form-item label="备注:" style="width: 90%">
        <el-input v-model="formData.remark" type="textarea" />
      </el-form-item>
    </el-form>
  </el-card>
</template>
<style lang="scss" scoped>
.form-page {
  padding: 1rem;
  --page-width: 1200px;

  &.with-toolbar {
    padding-top: 0;
  }
}

.toolbar {
  display: flex;
  margin-bottom: 0.5rem;
  padding: 5px;
  gap: 5px;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 0 0 4px 4px;
  max-width: var(--page-width);
  box-shadow: 1px 2px 2px rgba(0, 0, 0, 0.2);
  position: sticky;
  top: 0;
  z-index: 20;

  &:empty {
    visibility: hidden;
  }
}

.form-section {
  background-color: #fff;
  max-width: var(--page-width);
  margin: 0;
  padding: 1.5rem;
  border-radius: 4px;
  box-shadow: 2px 4px 4px rgba(0, 0, 0, 0.3);
}

.form-loading {
  padding: 2rem;
  font-size: 2.5rem;
  border-radius: 0 0 4px 4px;
  width: var(--page-width);

  &.ready {
    border-radius: 4px;
  }
}

.form-title {
  font-size: 1.3125rem;
  font-weight: 600;
  line-height: 1rem;
  margin: 0;
  padding: 0;
}

.form-title ~ .form-title {
  margin-top: 1rem;
}

.form-divider hr {
  border: none;
  border-top: var(--bs-border);
  margin: 0;
  padding: 0;
}

.grid {
  display: grid;
  gap: 1rem;
}

.grid-cols-12 {
  grid-template-columns: repeat(12, minmax(0, 1fr));
}

.col-span-12 {
  grid-column: span 12 / span 12;
}

.col-span-8 {
  grid-column: span 8 / span 8;
}

.col-span-6 {
  grid-column: span 6 / span 6;
}

.col-span-4 {
  grid-column: span 4 / span 4;
}

.col-span-3 {
  grid-column: span 3 / span 3;
}

.col-span-2 {
  grid-column: span 2 / span 2;
}

.col-span-1 {
  grid-column: span 1 / span 1;
}

.form-group {
  display: flex;
  flex-flow: column;
}

.form-group.required label:before {
  content: "*";
  color: red;
  font-family: Tahoma;
}

label {
  font-weight: 600;
}

.col-form-label {
  width: 100%;
  margin-bottom: 8px;
}

.tips {
  font-size: 0.75rem;
  color: var(--bs-secondary);
  margin-top: 5px;
}

.flex-column {
  display: flex;
  flex-flow: column;
  gap: 1rem;
}

.field-group {
  position: relative;
  padding: 1.5rem;
  border-radius: 4px;
  margin-top: 0.5rem;
  margin-bottom: 1rem;
  box-shadow: var(--bs-box-shadow);

  &:before {
    content: attr(label);
    position: absolute;
    left: 1rem;
    top: -1rem;
    background-color: #fff;
    padding: 0.5rem;
  }
}

.info-grid {
  max-width: 600px;

  &.is-continue {
    max-width: 850px;
  }

  height: var(--grid-height, 200px);

  :deep(.text-right) {
    text-align: right;
  }
}

.remote-table {
  td {
    padding: 5px;
    height: 30px;
  }

  td:first-of-type {
    text-align: center;
  }
}

.extra-grid {
  height: 250px;

  :deep(.thead-cell) {
    text-align: center;
  }
}

.el-form-item {
  width: 400px;
}
</style>
