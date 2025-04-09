<script setup lang="ts">
import { onMounted, ref } from "vue";
import { formRules } from "@/views/guarantee/rule";
import { useRoute } from "vue-router";
import {
  getBeGuaranteedDetail,
  getGuaranteeDetail,
  postBeGuaranteed,
  putBeGuaranteed
} from "@/api/guarantee";
import { message } from "@/utils/message";
import router from "@/router";
import accounting from "accounting";
import uploadLine from "@iconify-icons/ri/upload-line";
import { uploadFile } from "@/api/file";
import { BasicTypeEnum, getBasicTree } from "@/api/basic";

defineOptions({
  name: "BeGuaranteeDetail"
});
const loading = ref(false);
const route = useRoute();
const id = route.query?.id;
const isEdited = ref(false);
isEdited.value = !id;
const title = id ? "被担保详情" : "新增被担保";
const showRepay = !!id;

const originalFormData = ref({
  id: 0,
  guarantee_unit: "",
  guarantee_parent: "",
  nature: "",
  ownership: "",
  item: "",
  method: "",
  start_date: "",
  end_date: "",
  amount: "",
  application_file: "",
  be_guaranteed_unit: "",
  group_date: "",
  group_decision_file: "",
  sasac_record_amount: "",
  sasac_record_file: "",
  receipt_date: "",
  receipt_amount: "",
  remark: ""
});
const uploadRef = ref();
const application_file = ref("");
const group_decision_file = ref("");
const sasac_record_file = ref("");
const formData = ref<any>({ ...originalFormData.value });
const getGuaranteeUnitOptions = ref<any[]>([]);
const getGuaranteeTypeOptions = ref<any[]>([]);
onMounted(() => {
  if (id) {
    loading.value = true;
    getBeGuaranteedDetail(String(id)).then(res => {
      loading.value = false;
      Object.assign(originalFormData.value, res.data);
      Object.assign(formData.value, res.data);
      application_file.value = formData.value.application_file
        ? decodeURIComponent(formData.value.application_file.split("/").pop())
        : "";
      group_decision_file.value = formData.value.group_decision_file
        ? decodeURIComponent(
            formData.value.group_decision_file.split("/").pop()
          )
        : "";
      sasac_record_file.value = formData.value.sasac_record_file
        ? decodeURIComponent(formData.value.sasac_record_file.split("/").pop())
        : "";
    });
  }
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
  formData.value.sasac_record_amount = accounting.unformat(
    formData.value.sasac_record_amount
  );
  formData.value.receipt_amount = accounting.unformat(
    formData.value.receipt_amount
  );
  formData.value.amount = accounting.unformat(formData.value.amount);
  if (id) {
    putBeGuaranteed({ data: formData.value }, String(id)).then(res => {
      if (res && res.success) {
        isEdited.value = false;
        originalFormData.value = { ...formData.value };
        message("被担保信息修改成功", { type: "success" });
        router.push({ name: "BeGuaranteed" });
      } else {
        message("被担保信息修改失败", { type: "error" });
      }
    });
  } else {
    postBeGuaranteed({ data: formData.value }).then(res => {
      if (res && res.success) {
        isEdited.value = false;
        originalFormData.value = { ...formData.value };
        message("被担保信息新增成功", { type: "success" });
        router.push({ name: "BeGuaranteed" });
      } else {
        message("被担保信息新增失败", { type: "error" });
      }
    });
  }
};

function handleApplicationFileChange(file: any) {
  const reader = new FileReader();
  const base64String = ref<string | ArrayBuffer>("");
  reader.onload = e => {
    base64String.value = e.target.result;
    uploadFile({
      data: { base64: base64String.value, filename: file.name }
    }).then(res => {
      console.log(res);
      if (res.code === 0) {
        formData.value.application_file = res.data.file_path;
        application_file.value = file.name;
        message("上传文件成功", { type: "success" });
        uploadRef.value.clearFiles();
      } else {
        message("上传文件失败", { type: "error" });
      }
    });
  };
  reader.readAsDataURL(file.raw);
}

function handleGroupDecisionFileChange(file: any) {
  const reader = new FileReader();
  const base64String = ref<string | ArrayBuffer>("");
  reader.onload = e => {
    base64String.value = e.target.result;
    uploadFile({
      data: { base64: base64String.value, filename: file.name }
    }).then(res => {
      console.log(res);
      if (res.code === 0) {
        formData.value.group_decision_file = res.data.file_path;
        group_decision_file.value = file.name;
        message("上传文件成功", { type: "success" });
        uploadRef.value.clearFiles();
      } else {
        message("上传文件失败", { type: "error" });
      }
    });
  };
  reader.readAsDataURL(file.raw);
}

function handleSasacRecordFileChange(file: any) {
  const reader = new FileReader();
  const base64String = ref<string | ArrayBuffer>("");
  reader.onload = e => {
    base64String.value = e.target.result;
    uploadFile({
      data: { base64: base64String.value, filename: file.name }
    }).then(res => {
      console.log(res);
      if (res.code === 0) {
        formData.value.sasac_record_file = res.data.file_path;
        sasac_record_file.value = file.name;
        message("上传文件成功", { type: "success" });
        uploadRef.value.clearFiles();
      } else {
        message("上传文件失败", { type: "error" });
      }
    });
  };
  reader.readAsDataURL(file.raw);
}

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
          placeholder="请选择担保单位"
          style="width: 100%"
        />
      </el-form-item>
      <el-form-item label="担保单位母公司">
        <el-cascader
          v-model="formData.guarantee_parent"
          :options="getGuaranteeUnitOptions"
          :props="{
            label: 'name',
            value: 'name',
            emitPath: false
          }"
          clearable
          filterable
          placeholder="请选择担保单位母公司"
          style="width: 100%"
        />
      </el-form-item>
      <el-form-item label="单位性质">
        <el-input v-model="formData.nature" />
      </el-form-item>
      <el-form-item label="产权关系">
        <el-input v-model="formData.ownership" />
      </el-form-item>
      <el-form-item label="担保事项">
        <el-input v-model="formData.item" />
      </el-form-item>
      <el-form-item label="担保方式">
        <el-cascader
          v-model="formData.method"
          :options="getGuaranteeTypeOptions"
          :props="{
            label: 'name',
            value: 'name',
            emitPath: false
          }"
          clearable
          filterable
          placeholder="请选择担保方式"
          style="width: 100%"
        />
      </el-form-item>
      <el-form-item label="被担保开始日期">
        <el-date-picker
          v-model="formData.start_date"
          type="date"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      <el-form-item label="被担保结束日期">
        <el-date-picker
          v-model="formData.end_date"
          type="date"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      <el-form-item label="担保金额">
        <el-input
          v-model="formData.amount"
          :formatter="value => `${accounting.formatMoney(value, '￥', 2)}`"
        />
      </el-form-item>
      <el-form-item label="被担保单位">
        <el-cascader
          v-model="formData.be_guaranteed_unit"
          :options="getGuaranteeUnitOptions"
          :props="{
            label: 'name',
            value: 'name',
            emitPath: false
          }"
          clearable
          filterable
          placeholder="请选择被担保单位"
          style="width: 100%"
        />
      </el-form-item>
      <el-form-item label="集团董事会日期">
        <el-date-picker
          v-model="formData.group_date"
          type="date"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      <el-form-item label="国资委备案金额">
        <el-input
          v-model="formData.sasac_record_amount"
          :formatter="value => `${accounting.formatMoney(value, '￥', 2)}`"
        />
      </el-form-item>
      <el-form-item label="收函日期">
        <el-date-picker
          v-model="formData.receipt_date"
          type="date"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      <el-form-item label="收函金额">
        <el-input
          v-model="formData.receipt_amount"
          :formatter="value => `${accounting.formatMoney(value, '￥', 2)}`"
        />
      </el-form-item>
      <el-form-item label="备注" style="width: 90%">
        <el-input v-model="formData.remark" type="textarea" />
      </el-form-item>

      <el-form-item label="申请担保函">
        <el-upload
          ref="uploadRef"
          accept=".pdf,.doc,.docx"
          action="#"
          :limit="1"
          :auto-upload="false"
          :show-file-list="false"
          :on-change="handleApplicationFileChange"
        >
          <el-button v-if="!application_file" plain>
            <IconifyIconOffline :icon="uploadLine" />
            <span class="ml-2">上传文件</span>
          </el-button>
          <el-button v-else plain>
            {{ application_file }}
          </el-button>
        </el-upload>
        <el-button
          v-if="application_file"
          plain
          style="margin-left: 1rem; border-color: #409eff; color: #409eff"
          @click="downloadFile(formData.value.application_file)"
        >
          下载源文件
        </el-button>
      </el-form-item>
      <el-form-item label="集团董事会决议">
        <el-upload
          ref="uploadRef"
          accept=".pdf,.doc,.docx"
          action="#"
          :limit="1"
          :auto-upload="false"
          :show-file-list="false"
          :on-change="handleGroupDecisionFileChange"
        >
          <el-button v-if="!group_decision_file" plain>
            <IconifyIconOffline :icon="uploadLine" />
            <span class="ml-2">上传文件</span>
          </el-button>
          <el-button v-else plain>
            {{ group_decision_file }}
          </el-button>
        </el-upload>
        <el-button
          v-if="group_decision_file"
          plain
          style="margin-left: 1rem; border-color: #409eff; color: #409eff"
          @click="downloadFile(formData.value.group_decision_file)"
        >
          下载源文件
        </el-button>
      </el-form-item>
      <el-form-item label="国资委备案表">
        <el-upload
          ref="uploadRef"
          accept=".excel,.pdf,.doc,.docx,.csv"
          action="#"
          :limit="1"
          :auto-upload="false"
          :show-file-list="false"
          :on-change="handleSasacRecordFileChange"
        >
          <el-button v-if="!sasac_record_file" plain>
            <IconifyIconOffline :icon="uploadLine" />
            <span class="ml-2">上传文件</span>
          </el-button>
          <el-button v-else plain>
            {{ sasac_record_file }}
          </el-button>
        </el-upload>
        <el-button
          v-if="sasac_record_file"
          plain
          style="margin-left: 1rem; border-color: #409eff; color: #409eff"
          @click="downloadFile(formData.value.sasac_record_file)"
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
</style>
