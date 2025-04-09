import dayjs from "dayjs";
import editForm from "../form.vue";
import { handleTree } from "@/utils/tree";
import { message } from "@/utils/message";
import { addDialog } from "@/components/ReDialog";
import { reactive, ref, onMounted, h } from "vue";
import type { FormItemProps } from "../utils/types";
import { cloneDeep, isAllEmpty, deviceDetection } from "@pureadmin/utils";
import { usePublicHooks } from "@/views/system/hooks";
import {
  delBasic,
  exportBasicTemplate,
  getBasicList,
  importBasic,
  postBasic,
  putBasic
} from "@/api/basic";

export function useBasic(props) {
  const form = reactive({
    name: "",
    status: null
  });
  const props_type = props.type;
  const props_title = props.title;

  const formRef = ref();
  const dataList = ref([]);
  const loading = ref(true);
  const { tagStyle } = usePublicHooks();
  const uploadRef = ref();
  const columns: TableColumnList = [
    {
      label: "名称",
      prop: "name",
      width: 180,
      align: "left"
    },
    {
      label: "排序",
      prop: "sort",
      minWidth: 70
    },
    {
      label: "状态",
      prop: "status",
      minWidth: 100,
      cellRenderer: ({ row, props }) => (
        <el-tag size={props.size} style={tagStyle.value(row.status ? 1 : 0)}>
          {row.status === true ? "启用" : "停用"}
        </el-tag>
      )
    },
    {
      label: "创建时间",
      minWidth: 200,
      prop: "createTime",
      formatter: ({ createTime }) =>
        dayjs(createTime).format("YYYY-MM-DD HH:mm:ss")
    },
    {
      label: "更新时间",
      minWidth: 200,
      prop: "updateTime",
      formatter: ({ updateTime }) =>
        dayjs(updateTime).format("YYYY-MM-DD HH:mm:ss")
    },
    {
      label: "创建人",
      minWidth: 120,
      prop: "creator"
    },
    {
      label: "备注",
      prop: "remark",
      minWidth: 320
    },
    {
      label: "操作",
      fixed: "right",
      width: 210,
      slot: "operation"
    }
  ];

  function handleSelectionChange(val) {
    console.log("handleSelectionChange", val);
  }

  function resetForm(formEl) {
    if (!formEl) return;
    formEl.resetFields();
    onSearch();
  }

  async function onSearch() {
    loading.value = true;
    const { data } = await getBasicList({ params: { type: props_type } }); // 这里是返回一维数组结构，前端自行处理成树结构，返回格式要求：唯一id加父节点parentId，parentId取父节点id
    let newData = data;

    if (!isAllEmpty(form.name)) {
      // 前端搜索部门名称
      newData = newData.filter(item => item.name.includes(form.name));
    }
    if (!isAllEmpty(form.status)) {
      // 前端搜索状态
      newData = newData.filter(item => item.status === form.status);
    }
    dataList.value = handleTree(newData); // 处理成树结构
    loading.value = false;
  }

  function formatHigherDeptOptions(treeList) {
    // 根据返回数据的status字段值判断追加是否禁用disabled字段，返回处理后的树结构，用于上级部门级联选择器的展示（实际开发中也是如此，不可能前端需要的每个字段后端都会返回，这时需要前端自行根据后端返回的某些字段做逻辑处理）
    if (!treeList || !treeList.length) return;
    const newTreeList = [];
    for (let i = 0; i < treeList.length; i++) {
      treeList[i].disabled = treeList[i].status === 0;
      formatHigherDeptOptions(treeList[i].children);
      newTreeList.push(treeList[i]);
    }
    return newTreeList;
  }

  function openDialog(title = "新增", row?: FormItemProps) {
    addDialog({
      title: `${title}${row ? `：${props_title}` : ""}`,
      props: {
        formInline: {
          higherDeptOptions: formatHigherDeptOptions(cloneDeep(dataList.value)),
          parent: row?.parent ?? null,
          name: row?.name ?? "",
          type: props_type,
          sort: row?.sort ?? 0,
          status: row?.status ?? true,
          remark: row?.remark ?? ""
        }
      },
      width: "40%",
      draggable: true,
      fullscreen: deviceDetection(),
      fullscreenIcon: true,
      closeOnClickModal: false,
      contentRenderer: () => h(editForm, { ref: formRef }),
      beforeSure: (done, { options }) => {
        const FormRef = formRef.value.getRef();
        const curData = options.props.formInline as FormItemProps;
        function chores() {
          message(
            `您${title}了${row ? `：${props_title}` : ""}名称为${curData.name}的这条数据`,
            {
              type: "success"
            }
          );
          done(); // 关闭弹框
          onSearch(); // 刷新表格数据
        }
        FormRef.validate(valid => {
          if (valid) {
            console.log("curData", curData);
            // 表单规则校验通过
            if (title === "新增") {
              // 实际开发先调用新增接口，再进行下面操作
              // 新增部门接口
              postBasic({ data: curData })
                .then(res => {
                  if (res.success) {
                    chores();
                  }
                })
                .catch(() => {
                  message(`新增${row ? `：${props_title}` : ""}失败`, {
                    type: "error"
                  });
                });
            } else {
              // 实际开发先调用修改接口，再进行下面操作
              putBasic({ data: curData }, row.id)
                .then(res => {
                  if (res.success) {
                    chores();
                  }
                })
                .catch(() => {
                  message(`修改${row ? `：${props_title}` : ""}失败`, {
                    type: "error"
                  });
                });
              chores();
            }
          }
        });
      }
    });
  }

  function handleDelete(row) {
    delBasic(row.id).then(res => {
      if (!res || res.success) {
        message(
          `您删除了${row ? `：${props_title}` : ""}名称为${row.name}的这条数据`,
          { type: "success" }
        );
        onSearch();
      } else {
        message(`删除${row ? `：${props_title}` : ""}失败`, { type: "error" });
      }
    });
  }

  function downloadTemplate() {
    // 下载模板文件
    // 实际开发中，这里可以调用后端接口下载模板文件，然后前端打开下载窗口
    exportBasicTemplate({ params: { type: props_type } }).then(res => {
      console.log("res", res);
      const url = res.data.url;
      window.open(url);
    });
  }

  onMounted(() => {
    onSearch();
  });
  function handleApplicationFileChange(file: any) {
    const reader = new FileReader();
    const base64String = ref<string | ArrayBuffer>("");
    reader.onload = e => {
      base64String.value = e.target.result;
      importBasic({
        data: { base64: base64String.value, type: props_type }
      }).then(res => {
        if (res.code === 0) {
          message("上传文件成功", { type: "success" });
        } else {
          message("上传文件失败", { type: "error" });
        }
      });
    };
    uploadRef.value.clearFiles(); // 清空已选文件
    reader.readAsDataURL(file.raw);
    onSearch();
  }

  return {
    form,
    loading,
    columns,
    dataList,
    uploadRef,
    /** 搜索 */
    onSearch,
    /** 重置 */
    resetForm,
    /** 新增、修改部门 */
    openDialog,
    /** 删除部门 */
    handleDelete,
    handleSelectionChange,
    downloadTemplate,
    handleApplicationFileChange
  };
}
