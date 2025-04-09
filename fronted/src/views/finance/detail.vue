<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { formRules } from "@/views/guarantee/rule";
import { useRoute } from "vue-router";
import accounting from "accounting";

import { message } from "@/utils/message";
import router from "@/router";
import { useUserStoreHook } from "@/store/modules/user";
import { createLoan, getLoanDetail, updateLoan } from "@/api/loan";
import { BasicTypeEnum, getBasicTree } from "@/api/basic";
import { UploadInstance } from "element-plus";
import { uploadFile } from "@/api/file";
import uploadLine from "@iconify-icons/ri/upload-line";

defineOptions({
  name: "GuaranteeDetail"
});
const loading = ref(false);
const route = useRoute();
const id = route.query?.id;
const creditId = route.query?.creditId;
const isEdited = ref(false);
isEdited.value = !id;
const title = id ? "贷款详情" : "新增贷款";
const showRepay = !!id;
const loanUnits = ref([]);
const loanTypes = ref([]);
const upload = ref<UploadInstance>();
const uploadRef = ref();
const debt_file = ref("");
const originalFormData = ref({
  id: 0,
  credit: creditId,
  creditor: "",
  loan_unit: "",
  name: "",
  type: "",
  loan_amount: 0,
  repay_amount: 0,
  loan_balance: 0,
  contract_rate: 0,
  overall_rate: 0,
  deposit_rate: 0,
  actual_rate: 0,
  is_fixed_rate: false,
  margin_rate: 0,
  guarantee_way: "",
  guarantee_unit: "",
  anti_guarantee_way: "",
  anti_guarantee_unit: "",
  loan_date: "",
  due_date: "",
  interest_start_date: "",
  interest_end_date: "",
  interest: 0,
  actual_interest: 0,
  is_deposit: false,
  agent_user: "",
  debt_file: "",
  sign_date: "",
  remark: ""
});
const formData = ref({ ...originalFormData.value });
const getGuaranteeTypeOptions = ref<any[]>([]);
const getGuaranteeUnitOptions = ref<any[]>([]);
onMounted(() => {
  if (id) {
    loading.value = true;
    getLoanDetail(String(id)).then(res => {
      loading.value = false;
      Object.assign(originalFormData.value, res.data);
      Object.assign(formData.value, res.data);
      debt_file.value = res.data.debt_file
        ? decodeURIComponent(res.data.debt_file.split("/").pop())
        : "";
    });
  }
  getBasicTree(BasicTypeEnum.LOAN_UNIT).then(res => {
    loanUnits.value = res;
  });
  getBasicTree(BasicTypeEnum.LOAN_TYPE).then(res => {
    loanTypes.value = res;
  });
  getGuaranteeUnit();
});

// 使用 Object.assign 合并props和默认值
async function getGuaranteeUnit() {
  getGuaranteeUnitOptions.value = await getBasicTree(BasicTypeEnum.GUARANTEE);
  getGuaranteeTypeOptions.value = await getBasicTree(
    BasicTypeEnum.GUARANTEE_TYPE
  );
}
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
  formData.value.loan_amount = accounting.unformat(formData.value.loan_amount);
  formData.value.repay_amount = accounting.unformat(
    formData.value.repay_amount
  );
  formData.value.loan_balance = accounting.unformat(
    formData.value.loan_balance
  );
  formData.value.interest = accounting.unformat(formData.value.interest);
  formData.value.actual_interest = accounting.unformat(
    formData.value.actual_interest
  );
  formData.value.contract_rate = accounting.unformat(
    formData.value.contract_rate
  );
  formData.value.overall_rate = accounting.unformat(
    formData.value.overall_rate
  );
  formData.value.deposit_rate = accounting.unformat(
    formData.value.deposit_rate
  );
  formData.value.actual_rate = accounting.unformat(formData.value.actual_rate);
  formData.value.margin_rate = accounting.unformat(formData.value.margin_rate);
  if (id) {
    updateLoan({ data: formData.value }, String(id)).then(res => {
      if (res && res.success) {
        isEdited.value = false;
        originalFormData.value = { ...formData.value };
        message("贷款信息修改成功", { type: "success" });
        router.push({ name: "Finance" });
      } else {
        message("贷款信息修改失败!" + res.msg, { type: "error" });
      }
    });
  } else {
    formData.value.loan_balance = formData.value.loan_amount;
    createLoan({ data: formData.value }).then(res => {
      console.log(useUserStoreHook().username);
      if (res && res.success) {
        isEdited.value = false;
        originalFormData.value = { ...formData.value };
        message("贷款信息新增成功", { type: "success" });
        router.push({ name: "Finance" });
      } else {
        message("贷款信息新增失败!" + res.msg, { type: "error" });
      }
    });
  }
};

const submitUpload = (file: any) => {
  const reader = new FileReader();
  const base64String = ref<string | ArrayBuffer>("");
  reader.onload = e => {
    base64String.value = e.target.result;
    uploadFile({
      data: { base64: base64String.value, filename: file.name }
    }).then(res => {
      console.log(res);
      if (res.code === 0) {
        formData.value.debt_file = res.data.file_url;
        debt_file.value = file.name;
        message("上传文件成功", { type: "success" });
        uploadRef.value.clearFiles();
      } else {
        message("上传文件失败", { type: "error" });
      }
    });
  };
  reader.readAsDataURL(file.raw);
};

function downloadFile(url: string) {
  window.open(url, "_blank");
}
</script>

<template>
  <el-card shadow="never" style="height: 100%">
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
      :model="formData"
      :rules="formRules"
      label-width="150px"
      class="form-inline"
      :disabled="!isEdited"
      :inline="true"
    >
      <el-form-item label="贷款单位名称" prop="loan_unit">
        <el-cascader
          v-model="formData.loan_unit"
          :options="loanUnits"
          :props="{
            label: 'name',
            value: 'name',
            emitPath: false
          }"
          clearable
          filterable
          placeholder="请选择贷款单位名称"
          style="width: 100%"
        />
      </el-form-item>
      <el-form-item label="贷款名称">
        <el-input v-model="formData.name" />
      </el-form-item>
      <el-form-item label="贷款类型" prop="type">
        <el-cascader
          v-model="formData.type"
          :options="loanTypes"
          :props="{
            label: 'name',
            value: 'name',
            emitPath: false
          }"
          clearable
          filterable
          placeholder="请选择贷款单位名称"
          style="width: 100%"
        />
      </el-form-item>
      <el-form-item label="贷款金额">
        <el-input
          v-model="formData.loan_amount"
          :formatter="value => `${accounting.formatMoney(value, '￥', 2)}`"
        />
      </el-form-item>
      <el-form-item v-show="id" label="已还金额">
        <el-input
          v-model="formData.repay_amount"
          :formatter="value => `${accounting.formatMoney(value, '￥', 2)}`"
          editable="false"
        />
      </el-form-item>
      <el-form-item v-show="id" label="贷款余额">
        <el-input
          v-model="formData.loan_balance"
          :formatter="value => `${accounting.formatMoney(value, '￥', 2)}`"
          editable="false"
        />
      </el-form-item>
      <el-form-item label="合同利率">
        <el-input
          v-model="formData.contract_rate"
          :formatter="
            value =>
              `${accounting.formatMoney(value, {
                symbol: '%',
                precision: 4,
                format: '%v%'
              })}`
          "
        />
      </el-form-item>
      <el-form-item label="综合利率">
        <el-input
          v-model="formData.overall_rate"
          :formatter="
            value =>
              `${accounting.formatMoney(value, {
                symbol: '%',
                precision: 4,
                format: '%v%'
              })}`
          "
        />
      </el-form-item>
      <el-form-item label="已做配存业务利率">
        <el-input
          v-model="formData.deposit_rate"
          :formatter="
            value =>
              `${accounting.formatMoney(value, {
                symbol: '%',
                precision: 4,
                format: '%v%'
              })}`
          "
        />
      </el-form-item>
      <el-form-item label="实际利率">
        <el-input
          v-model="formData.actual_rate"
          :formatter="
            value =>
              `${accounting.formatMoney(value, {
                symbol: '%',
                precision: 4,
                format: '%v%'
              })}`
          "
        />
      </el-form-item>
      <el-form-item label="是否固定利率">
        <el-switch v-model="formData.is_fixed_rate" />
      </el-form-item>
      <el-form-item label="保证金比例">
        <el-input
          v-model="formData.margin_rate"
          :formatter="
            value =>
              `${accounting.formatMoney(value, {
                symbol: '%',
                precision: 4,
                format: '%v%'
              })}`
          "
        />
      </el-form-item>
      <el-form-item label="担保单位">
        <el-cascader
          v-model="formData.guarantee_unit"
          :options="getGuaranteeUnitOptions"
          :props="{
            label: 'name',
            value: 'name',
            emitPath: false
          }"
          clearable
          filterable
          placeholder="请选择担保单位名称"
          style="width: 100%"
        />
      </el-form-item>
      <el-form-item label="担保方式">
        <el-cascader
          v-model="formData.guarantee_way"
          :options="getGuaranteeTypeOptions"
          :props="{
            label: 'name',
            value: 'name',
            emitPath: false
          }"
          clearable
          filterable
          placeholder="请选择担保方式名称"
          style="width: 100%"
        />
      </el-form-item>
      <el-form-item label="反担保单位">
        <el-cascader
          v-model="formData.anti_guarantee_unit"
          :options="getGuaranteeUnitOptions"
          :props="{
            label: 'name',
            value: 'name',
            emitPath: false
          }"
          clearable
          filterable
          placeholder="请选择反担保单位名称"
          style="width: 100%"
        />
      </el-form-item>
      <el-form-item label="反担保方式">
        <el-cascader
          v-model="formData.anti_guarantee_way"
          :options="getGuaranteeTypeOptions"
          :props="{
            label: 'name',
            value: 'name',
            emitPath: false
          }"
          clearable
          filterable
          placeholder="请选择反担保方式名称"
          style="width: 100%"
        />
      </el-form-item>
      <el-form-item label="贷款借款日">
        <el-date-picker
          v-model="formData.loan_date"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      <el-form-item label="贷款到期日">
        <el-date-picker v-model="formData.due_date" value-format="YYYY-MM-DD" />
      </el-form-item>
      <el-form-item label="利息">
        <el-input
          v-model="formData.interest"
          :formatter="value => `${accounting.formatMoney(value, '￥', 2)}`"
        />
      </el-form-item>
      <el-form-item label="实际付息">
        <el-input
          v-model="formData.actual_interest"
          :formatter="value => `${accounting.formatMoney(value, '￥', 2)}`"
        />
      </el-form-item>
      <el-form-item label="是否配存业务">
        <el-switch v-model="formData.is_deposit" />
      </el-form-item>
      <el-form-item label="经办人">
        <el-input v-model="formData.agent_user" />
      </el-form-item>
      <el-form-item label="签订时间">
        <el-date-picker
          v-model="formData.sign_date"
          type="date"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      <el-form-item label="备注" style="width: 90%">
        <el-input v-model="formData.remark" type="textarea" />
      </el-form-item>
      <el-form-item label="债务文件">
        <el-upload
          ref="uploadRef"
          accept=".pdf,.doc,.docx"
          action="#"
          :limit="1"
          :auto-upload="false"
          :show-file-list="false"
          :on-change="submitUpload"
        >
          <el-button v-if="!debt_file" plain>
            <IconifyIconOffline :icon="uploadLine" />
            <span class="ml-2">上传文件</span>
          </el-button>
          <el-button v-else plain>
            {{ debt_file }}
          </el-button>
        </el-upload>
        <el-button
          v-if="formData.debt_file"
          plain
          style="margin-left: 1rem; border-color: #409eff; color: #409eff"
          @click="downloadFile(formData.debt_file)"
        >
          下载源文件
        </el-button>
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

.el-date-picker {
  width: 400px;
}
</style>
