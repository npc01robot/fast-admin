<script setup lang="ts">
import { onMounted, ref } from "vue";
import { formRules } from "@/views/guarantee/rule";
import { useRoute } from "vue-router";
import { getCreditDetail, postCredit, putCredit } from "@/api/credit";
import { BasicTypeEnum, getBasicTree } from "@/api/basic";
import dayjs from "dayjs";
import uploadLine from "@iconify-icons/ri/upload-line";
import { uploadFile } from "@/api/file";
import { message } from "@/utils/message";
import router from "@/router";
import accounting from "accounting";

defineOptions({
  name: "GuaranteeDetail"
});
const loading = ref(false);
const route = useRoute();
const id = route.query?.id;
console.log(id);
const title = id ? "授信详情" : "新增授信";
const organizationOptions = ref([]);
const uploadRef = ref();
const three_chairman_decision_file = ref("");
const two_chairman_decision_file = ref("");
const group_chairman_decision_file = ref("");
const formData = ref<any>({
  id: 0,
  code: "",
  name: "",
  organization: "",
  amount: 0,
  surplus_amount: 0,
  group_chairman: false,
  group_deputy_chairman: false,
  sub_chairman: false,
  sub_deputy_chairman: false,
  start_date: "",
  end_date: "",
  remark: "",
  three_deputy_chairman_date: "",
  three_chairman_date: "",
  two_deputy_chairman_date: "",
  two_chairman_date: "",
  group_deputy_chairman_date: "",
  group_chairman_date: "",
  three_chairman_decision_file: "",
  two_chairman_decision_file: "",
  group_chairman_decision_file: "",
  title: "",
  create_time: "",
  update_time: ""
});
const newFormInline = formData;
const start_end_date = ref([]);
const ruleFormRef = ref();

onMounted(() => {
  if (id) {
    loading.value = true;
    getCreditDetail(String(id)).then(res => {
      loading.value = false;
      Object.assign(formData.value, res.data);

      three_chairman_decision_file.value = formData.value
        .three_chairman_decision_file
        ? decodeURIComponent(
            formData.value.three_chairman_decision_file.split("/").pop()
          )
        : "";
      two_chairman_decision_file.value = formData.value
        .two_chairman_decision_file
        ? decodeURIComponent(
            formData.value.two_chairman_decision_file.split("/").pop()
          )
        : "";
      group_chairman_decision_file.value = formData.value
        .group_chairman_decision_file
        ? decodeURIComponent(
            formData.value.group_chairman_decision_file.split("/").pop()
          )
        : "";
      start_end_date.value = [
        new Date(formData.value.start_date),
        new Date(formData.value.end_date)
      ];
      console.log(formData.value);
    });
  }
  getOrganizationOptions();
});

const onSubmit = () => {
  newFormInline.value.amount = accounting.unformat(newFormInline.value.amount);
  newFormInline.value.surplus_amount = accounting.unformat(
    newFormInline.value.surplus_amount
  );
  if (id) {
    putCredit({ data: newFormInline.value }, String(id)).then(res => {
      if (res.success) {
        message("更新成功", { type: "success" });
        router.push({ name: "Credit" });
      } else {
        message("更新失败", { type: "error" });
      }
    });
  } else {
    newFormInline.value.surplus_amount = newFormInline.value.amount;
    postCredit({ data: newFormInline.value }).then(res => {
      if (res.success) {
        message("保存成功", { type: "success" });
        router.push({ name: "Credit" });
      } else {
        message("保存失败", { type: "error" });
      }
    });
  }
};

function handleDateChange(val: any) {
  start_end_date.value = val;
  newFormInline.value.start_date = dayjs(val[0]).format("YYYY-MM-DD");
  newFormInline.value.end_date = dayjs(val[1]).format("YYYY-MM-DD");
}

async function getOrganizationOptions() {
  organizationOptions.value = await getBasicTree(BasicTypeEnum.CREDIT);
}

function handleThreeUpload(file: any) {
  const reader = new FileReader();
  const base64String = ref<string | ArrayBuffer>("");
  reader.onload = e => {
    base64String.value = e.target.result;
    uploadFile({
      data: { base64: base64String.value, filename: file.name }
    }).then(res => {
      console.log(res);
      if (res.code === 0) {
        newFormInline.value.three_chairman_decision_file = res.data.file_path;
        three_chairman_decision_file.value = file.name;
        message("上传文件成功", { type: "success" });
        uploadRef.value.clearFiles();
      } else {
        message("上传文件失败", { type: "error" });
      }
    });
  };
  reader.readAsDataURL(file.raw);
}

function handleTwoUpload(file: any) {
  const reader = new FileReader();
  const base64String = ref<string | ArrayBuffer>("");
  reader.onload = e => {
    base64String.value = e.target.result;
    uploadFile({
      data: { base64: base64String.value, filename: file.name }
    }).then(res => {
      console.log(res);
      if (res.code === 0) {
        newFormInline.value.two_chairman_decision_file = res.data.file_path;
        two_chairman_decision_file.value = file.name;
        message("上传文件成功", { type: "success" });
        uploadRef.value.clearFiles();
      } else {
        message("上传文件失败", { type: "error" });
      }
    });
  };
  reader.readAsDataURL(file.raw);
}

function handleGroupUpload(file: any) {
  const reader = new FileReader();
  const base64String = ref<string | ArrayBuffer>("");
  reader.onload = e => {
    base64String.value = e.target.result;
    uploadFile({
      data: { base64: base64String.value, filename: file.name }
    }).then(res => {
      console.log(res);
      if (res.code === 0) {
        newFormInline.value.group_chairman_decision_file = res.data.file_path;
        group_chairman_decision_file.value = file.name;
        message("上传文件成功", { type: "success" });
        uploadRef.value.clearFiles();
      } else {
        message("上传文件失败", { type: "error" });
      }
    });
  };
  reader.readAsDataURL(file.raw);
}

function downloadFile(type: string) {
  const url =
    type === "three_chairman_decision_file"
      ? newFormInline.value.three_chairman_decision_file
      : type === "two_chairman_decision_file"
        ? newFormInline.value.two_chairman_decision_file
        : newFormInline.value.group_chairman_decision_file;
  window.open(url);
}

function onReset() {
  newFormInline.value = {
    id: 0,
    code: "",
    name: "",
    organization: "",
    amount: 0,
    surplus_amount: 0,
    group_chairman: "",
    group_deputy_chairman: false,
    sub_chairman: "",
    sub_deputy_chairman: false,
    start_date: "",
    end_date: "",
    remark: "",
    three_deputy_chairman_date: "",
    three_chairman_date: "",
    two_deputy_chairman_date: "",
    two_chairman_date: "",
    group_deputy_chairman_date: "",
    group_chairman_date: "",
    three_chairman_decision_file: "",
    two_chairman_decision_file: "",
    group_chairman_decision_file: "",
    title: ""
  };
}
</script>

<template>
  <el-card shadow="never">
    <h1 v-if="id" class="form-title">{{ title }} / {{ newFormInline.code }}</h1>
    <h1 v-else class="form-title">{{ title }}</h1>
    <div style="margin-top: 1rem">
      <el-button size="default" type="primary" @click="onSubmit"
        >保存</el-button
      >
      <el-button size="default" @click="onReset">重置</el-button>
    </div>
    <el-divider />
    <el-form
      ref="ruleFormRef"
      :model="newFormInline"
      :rules="formRules"
      label-width="150px"
      :inline="true"
    >
      <el-form-item label="授信名称：" prop="name">
        <el-input v-model="newFormInline.name" placeholder="请输入授信名称" />
      </el-form-item>
      <el-form-item label="金融机构：" prop="organization">
        <el-cascader
          v-model="newFormInline.organization"
          :options="organizationOptions"
          :props="{
            label: 'name',
            value: 'name',
            emitPath: false
          }"
          clearable
          filterable
          placeholder="请选择授信金融机构"
          style="width: 100%"
        />
      </el-form-item>
      <el-form-item label="授信金额：" prop="amount">
        <el-input
          v-model="newFormInline.amount"
          placeholder="请输入授信金额(万元)"
          :formatter="value => `${accounting.formatMoney(value, '￥', 2)}`"
        />
      </el-form-item>
      <el-form-item v-show="id" label="剩余金额：" prop="surplus_amount">
        <el-input
          v-model="newFormInline.surplus_amount"
          :formatter="value => `${accounting.formatMoney(value, '￥', 2)}`"
          editable="false"
        />
      </el-form-item>
      <el-form-item label="集团董事会：" prop="group_chairman">
        <el-select
          v-model="newFormInline.group_chairman"
          placeholder="集团董事会"
        >
          <el-option label="是" :value="true" />
          <el-option label="否" :value="false" />
        </el-select>
      </el-form-item>
      <el-form-item label="集团党委会：" prop="group_deputy_chairman">
        <el-select
          v-model="newFormInline.group_deputy_chairman"
          placeholder="集团党委会是否决议"
        >
          <el-option label="是" :value="true" />
          <el-option label="否" :value="false" />
        </el-select>
      </el-form-item>

      <el-form-item label="子公司董事会：" prop="sub_chairman">
        <el-select
          v-model="newFormInline.sub_chairman"
          placeholder="子公司董事会"
        >
          <el-option label="是" :value="true" />
          <el-option label="否" :value="false" />
        </el-select>
      </el-form-item>
      <el-form-item label="子公司党委会：" prop="sub_deputy_chairman">
        <el-select
          v-model="newFormInline.sub_deputy_chairman"
          placeholder="子公司党委会是否决议"
        >
          <el-option label="是" :value="true" />
          <el-option label="否" :value="false" />
        </el-select>
      </el-form-item>

      <el-form-item label="授信起始日期：">
        <el-date-picker
          v-model="start_end_date"
          type="daterange"
          start-placeholder="授信开始日期"
          end-placeholder="授信结束日期"
          placeholder="请选择授信起始日期"
          @change="handleDateChange"
        />
      </el-form-item>
      <el-form-item label="备注：" prop="remark" style="width: 100%">
        <el-input
          v-model="newFormInline.remark"
          type="textarea"
          placeholder="请输入备注"
        />
      </el-form-item>
      <el-divider />
      <h3 style="margin-top: 1rem; margin-bottom: 0.5rem">三级</h3>
      <el-form-item label="公司党委会：" prop="three_deputy_chairman_date">
        <el-date-picker
          v-model="newFormInline.three_deputy_chairman_date"
          type="date"
          placeholder="决议日期"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      <el-form-item label="公司董事会：" prop="three_chairman_date">
        <el-date-picker
          v-model="newFormInline.three_chairman_date"
          type="date"
          placeholder="决议日期"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      <el-form-item
        label="董事会决议文件："
        prop="three_chairman_decision_file"
        style="width: 35%"
      >
        <el-upload
          ref="uploadRef"
          accept=".pdf,.doc,.docx"
          action="#"
          :limit="1"
          :auto-upload="false"
          :show-file-list="false"
          :on-change="handleThreeUpload"
        >
          <el-button v-if="!three_chairman_decision_file" plain>
            <IconifyIconOffline :icon="uploadLine" />
            <span class="ml-2">上传文件</span>
          </el-button>
          <el-button v-else plain>
            {{ three_chairman_decision_file }}
          </el-button>
        </el-upload>
        <el-button
          v-if="three_chairman_decision_file"
          plain
          style="margin-left: 1rem; border-color: #409eff; color: #409eff"
          @click="downloadFile('three_chairman_decision_file')"
        >
          下载源文件
        </el-button>
      </el-form-item>
      <h3 style="margin-top: 1rem; margin-bottom: 0.5rem">二级</h3>
      <el-form-item label="公司党委会：" prop="two_deputy_chairman_date">
        <el-date-picker
          v-model="newFormInline.two_deputy_chairman_date"
          type="date"
          placeholder="决议日期"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      <el-form-item label="公司董事会：" prop="two_chairman_date">
        <el-date-picker
          v-model="newFormInline.two_chairman_date"
          type="date"
          placeholder="决议日期"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      <el-form-item
        label="董事会决议文件："
        prop="two_chairman_decision_file"
        style="width: 35%"
      >
        <el-upload
          ref="uploadRef"
          accept=".pdf,.doc,.docx"
          action="#"
          :limit="1"
          :auto-upload="false"
          :show-file-list="false"
          :on-change="handleTwoUpload"
        >
          <el-button v-if="!two_chairman_decision_file" plain>
            <IconifyIconOffline :icon="uploadLine" />
            <span class="ml-2">上传文件</span>
          </el-button>
          <el-button v-else plain>
            {{ two_chairman_decision_file }}
          </el-button>
        </el-upload>
        <el-button
          v-if="two_chairman_decision_file"
          plain
          style="margin-left: 1rem; border-color: #409eff; color: #409eff"
          @click="downloadFile('two_chairman_decision_file')"
        >
          下载源文件
        </el-button>
      </el-form-item>
      <h3 style="margin-top: 1rem; margin-bottom: 0.5rem">集团</h3>
      <el-form-item label="集团党委会：" prop="group_deputy_chairman_date">
        <el-date-picker
          v-model="newFormInline.group_deputy_chairman_date"
          type="date"
          placeholder="决议日期"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      <el-form-item label="集团董事会：" prop="group_chairman_date">
        <el-date-picker
          v-model="newFormInline.group_chairman_date"
          type="date"
          placeholder="决议日期"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      <el-form-item
        label="董事会决议文件："
        prop="group_chairman_decision_file"
        style="width: 35%"
      >
        <el-upload
          ref="uploadRef"
          accept=".pdf,.doc,.docx"
          action="#"
          :limit="1"
          :auto-upload="false"
          :show-file-list="false"
          :on-change="handleGroupUpload"
        >
          <el-button v-if="!group_chairman_decision_file" plain>
            <IconifyIconOffline :icon="uploadLine" />
            <span class="ml-2">上传文件</span>
          </el-button>
          <el-button v-else plain>
            {{ group_chairman_decision_file }}
          </el-button>
        </el-upload>
        <el-button
          v-if="group_chairman_decision_file"
          plain
          style="margin-left: 1rem; border-color: #409eff; color: #409eff"
          @click="downloadFile('group_chairman_decision_file')"
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
  font-size: 2rem;
  font-weight: 800;
  line-height: 3rem;
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
.el-col {
  margin-right: 1rem;
}
.el-form-item {
  width: 400px;
}
</style>
