import { onMounted, onUnmounted, reactive, ref } from "vue";
import type { GridOptions } from "ag-grid-community";
import EventEmitter from "eventemitter3";
import type { ServerSideGridOptions } from "@/views/components/ag-grid/server-type";
import type { ToolButton } from "@/views/components/ag-grid/server-type";
import { useDomIcon, useRenderIcon } from "@/components/ReIcon/src/hooks";
import AddFill from "@iconify-icons/ep/plus";
import { deleteCredit, exportCredit, getCreditList } from "@/api/credit";
import { useMultiTagsStoreHook } from "@/store/modules/multiTags";
import router from "@/router";
import { message } from "@/utils/message";
import { handleColumTree } from "@/utils/tree";
import { BasicTypeEnum, getBasicList } from "@/api/basic";
import AddCircleFill from "@iconify-icons/ri/add-circle-fill";
import EditFill from "@iconify-icons/ri/file-edit-fill";
import DeleteFill from "@iconify-icons/ri/delete-bin-fill";
import { columnType } from "@/views/components/ag-grid/columnType";
import Download from "@iconify-icons/ep/download";
import { getParams } from "@/views/components/ag-grid/utils";
export function useApprove() {
  const pageSize = ref(30);
  const pageCount = ref(0);
  const componentRef = ref<ServerSideGridElement<any>>();
  type _GridType = typeof componentRef.value;

  let api: NonNullable<_GridType>;

  const emit = new EventEmitter<"modelUpdated">();
  onMounted(() => {
    api = componentRef.value!;
  });
  onUnmounted(() => {
    emit.removeAllListeners();
  });
  const vm = reactive({
    loading: false
  });
  const cacheOrgnizationTree = ref();
  const gridOptions: GridOptions<any> = {
    columnDefs: [
      { field: "code", headerName: "授信编号" },
      { field: "name", headerName: "授信名称" },
      { field: "organization", headerName: "授信金融机构", type: "bank" },
      { field: "amount", headerName: "授信金额", type: "number" },
      {
        field: "surplus_amount",
        headerName: "剩余金额",
        type: "number"
      },
      {
        field: "group_chairman",
        headerName: "集团董事会",
        type: "bool"
      },
      {
        field: "group_deputy_chairman",
        headerName: "集团党委会",
        type: "bool"
      },
      {
        field: "sub_chairman",
        headerName: "子公司董事会",
        type: "bool"
      },
      {
        field: "sub_deputy_chairman",
        headerName: "子公司党委会",
        type: "bool"
      },
      { field: "start_date", headerName: "起始日期", type: "date" },
      { field: "end_date", headerName: "终止日期", type: "date" },
      { field: "remark", headerName: "备注" }
    ],
    columnTypes: {
      ...columnType,
      bank: {
        valueFormatter: params => {
          return params.value.name;
        },
        filter: "agSetColumnFilter",
        filterParams: {
          treeList: true,
          values: params => {
            getBasicList({ params: { type: BasicTypeEnum.CREDIT } }).then(
              res => {
                cacheOrgnizationTree.value = handleColumTree(res.data);
                params.success(res.data);
              }
            );
          },
          treeListPathGetter: data => {
            const path = cacheOrgnizationTree.value[data.id];
            if (path) {
              return path.map(item => item.name);
            }
            return [data.name];
          },
          valueFormatter: params => params.value.name,
          keyCreator: params => params.value.name,
          closeOnApply: true,
          excelMode: "windows",
          buttons: ["apply", "reset"]
        }
      }
    },
    selection: {
      mode: "multiRow",
      selectAll: "all",
      checkboxes: true,
      enableClickSelection: true,
      enableMultiSelectWithClick: true
    },
    rowModelType: "serverSide",
    defaultColDef: {
      suppressHeaderMenuButton: true
    },
    getContextMenuItems: params => {
      const node = params.node;
      return [
        {
          name: "授信详情",
          disabled: !node?.data?.id,
          icon: useDomIcon(EditFill),
          action: () => {
            openNew(node.data.id);
          }
        },
        {
          name: "新增贷款",
          disabled: !node?.data?.id || node.data.surplus_amount === "0.00",
          icon: useDomIcon(AddCircleFill),
          action: () => {
            openLoan(String(node.data.id));
          }
        },
        {
          name: "删除所选",
          disabled: !node?.data?.id,
          icon: useDomIcon(DeleteFill),
          action: deleteNode(node.data.id)
        }
      ];
    },
    pagination: true,
    paginationPageSize: pageSize.value,
    // onGridReady: onGridReady
    paginationPageSizeSelector: [10, 20, 30, 50]
  };

  const buttons: Array<ToolButton | string> = [
    {
      name: "create",
      icon: useRenderIcon(AddFill),
      label: "新增",
      action: () => {
        openNew();
      }
    },
    {
      name: "download",
      icon: useRenderIcon(Download),
      label: "导出所选",
      action: () => {
        exportSelected();
      }
    },
    {
      name: "downloadAll",
      icon: useRenderIcon(Download),
      label: "导出全部",
      action: () => {
        exportAll();
      }
    }
  ];

  const openNew = (id?: number) => {
    useMultiTagsStoreHook().handleTags("push", {
      path: `/approve/detail`,
      name: "CreditDetail",
      meta: {
        title: `授信管理详情`,
        dynamicLevel: 1
      }
    });
    router.push({
      path: "/approve/detail",
      query: { id }
    });
  };

  const deleteNode = (id: number) => () => {
    deleteCredit(id).then(res => {
      if (!res || res.success) {
        message("删除成功", { type: "success" });
        api.reload();
      } else {
        message("删除失败", { type: "error" });
      }
    });
  };

  const openLoan = (id: string) => {
    useMultiTagsStoreHook().handleTags("push", {
      path: `/finance/detail`,
      name: "FinanceDetail",
      meta: {
        title: `融资详情`,
        dynamicLevel: 1
      }
    });
    router.push({
      path: "/finance/detail",
      query: { creditId: id }
    });
  };

  const exportAll = () => {
    const params = getParams(options, true);
    console.log(params);
    return exportCredit({ params: params }).then(() => {
      message("正在导出，请稍后", { type: "success" });
    });
  };

  const exportSelected = () => {
    const selectedStatus: any = options.api.getServerSideSelectionState();
    let selectedIds = [];
    if (selectedStatus.selectAll) {
      options.api.forEachNode(node => selectedIds.push(node.data.id));
    } else {
      selectedIds = options.api.getSelectedNodes().map(node => node.data.id);
    }
    const params = getParams(options, true);
    params["ids"] = selectedIds.join(",");
    return exportCredit({ params: params }).then(() => {
      message("正在导出，请稍后", { type: "success" });
    });
  };

  async function loadRows(params) {
    return getCreditList({ params: params }).then(res => {
      const rowData = res.data.list;
      const rowCount = res.data.total;
      pageSize.value = res.data.pageSize;
      pageCount.value = res.data.pageCount;
      vm.loading = false;
      return {
        rowData,
        rowCount
      };
    });
  }

  const options: ServerSideGridOptions<any> = {
    gridName: "授信审批",
    gridOptions: gridOptions,
    buttons: buttons,
    loadRows: loadRows
  };
  console.log(options);

  return {
    componentRef,
    options
  };
}
