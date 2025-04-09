<script setup lang="ts">
import { ref } from "vue";
import { useBasic } from "./utils/hook";
import { PureTableBar } from "@/components/RePureTableBar";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";

import Delete from "@iconify-icons/ep/delete";
import EditPen from "@iconify-icons/ep/edit-pen";
import Refresh from "@iconify-icons/ep/refresh";
import AddFill from "@iconify-icons/ri/add-circle-line";
import Download from "@iconify-icons/ep/download";
import Upload from "@iconify-icons/ri/upload-line";

defineOptions({
  name: "SystemDept"
});

const props = defineProps({
  title: {
    type: String,
    default: "担保单位管理"
  },
  type: {
    type: Number,
    default: 1
  }
});
const formRef = ref();
const tableRef = ref();
const {
  form,
  loading,
  columns,
  dataList,
  uploadRef,
  onSearch,
  resetForm,
  openDialog,
  handleDelete,
  handleSelectionChange,
  downloadTemplate,
  handleApplicationFileChange
} = useBasic({ title: props.title, type: props.type });
</script>

<template>
  <div class="main">
    <el-form
      ref="formRef"
      :inline="true"
      :model="form"
      class="search-form bg-bg_color w-[99/100] pl-8 pt-[12px] overflow-auto"
    >
      <el-form-item :label="props.title" prop="name">
        <el-input
          v-model="form.name"
          :placeholder="`请输入${props.title}`"
          clearable
          class="!w-[180px]"
        />
      </el-form-item>
      <el-form-item label="状态：" prop="status">
        <el-select
          v-model="form.status"
          placeholder="请选择状态"
          clearable
          class="!w-[180px]"
        >
          <el-option label="启用" :value="true" />
          <el-option label="停用" :value="false" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button
          type="primary"
          :icon="useRenderIcon('ri:search-line')"
          :loading="loading"
          @click="onSearch"
        >
          搜索
        </el-button>
        <el-button :icon="useRenderIcon(Refresh)" @click="resetForm(formRef)">
          重置
        </el-button>
      </el-form-item>
    </el-form>

    <PureTableBar
      :title="`${props.title}管理`"
      :columns="columns"
      :tableRef="tableRef?.getTableRef()"
      @refresh="onSearch"
    >
      <template #buttons>
        <el-button
          type="primary"
          :icon="useRenderIcon(AddFill)"
          @click="openDialog()"
        >
          新增{{ props.title }}
        </el-button>
        <el-button
          type="primary"
          :icon="useRenderIcon(Download)"
          @click="downloadTemplate()"
        >
          下载模板
        </el-button>

        <el-upload
          ref="uploadRef"
          accept=".xls,.xlsx"
          action="#"
          :limit="1"
          :auto-upload="false"
          :show-file-list="false"
          :on-change="handleApplicationFileChange"
          style="margin-left: 12px"
        >
          <el-button type="primary" :icon="useRenderIcon(Upload)">
            导入数据
          </el-button>
        </el-upload>
      </template>
      <template v-slot="{ size, dynamicColumns }">
        <pure-table
          ref="tableRef"
          adaptive
          :adaptiveConfig="{ offsetBottom: 45 }"
          align-whole="center"
          row-key="id"
          showOverflowTooltip
          table-layout="auto"
          default-expand-all
          :loading="loading"
          :size="size"
          :data="dataList"
          :columns="dynamicColumns"
          :header-cell-style="{
            background: 'var(--el-fill-color-light)',
            color: 'var(--el-text-color-primary)'
          }"
          @selection-change="handleSelectionChange"
        >
          <template #operation="{ row }">
            <el-button
              class="reset-margin"
              link
              type="primary"
              :size="size"
              :icon="useRenderIcon(EditPen)"
              @click="openDialog('修改', row)"
            >
              修改
            </el-button>
            <el-button
              class="reset-margin"
              link
              type="primary"
              :size="size"
              :icon="useRenderIcon(AddFill)"
              @click="
                openDialog('新增', { parent: row.id, type: props.type } as any)
              "
            >
              新增
            </el-button>
            <el-popconfirm
              :title="`是否确认删除名称为${row.name}的这条数据`"
              @confirm="handleDelete(row)"
            >
              <template #reference>
                <el-button
                  class="reset-margin"
                  link
                  type="primary"
                  :size="size"
                  :icon="useRenderIcon(Delete)"
                >
                  删除
                </el-button>
              </template>
            </el-popconfirm>
          </template>
        </pure-table>
      </template>
    </PureTableBar>
  </div>
</template>

<style lang="scss" scoped>
:deep(.el-table__inner-wrapper::before) {
  height: 0;
}

.main-content {
  margin: 24px 24px 0 !important;
}

.search-form {
  :deep(.el-form-item) {
    margin-bottom: 12px;
  }
}
</style>
