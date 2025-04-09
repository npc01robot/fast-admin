import { onMounted, onUnmounted, reactive, ref } from "vue";
import type { GridOptions } from "ag-grid-community";
import EventEmitter from "eventemitter3";
import type { ServerSideGridOptions } from "@/views/components/ag-grid/server-type";
import type { ToolButton } from "@/views/components/ag-grid/server-type";
import router from "@/router";
import { message } from "@/utils/message";
import { columnType } from "@/views/components/ag-grid/columnType";
import { deleteLoanRepay, exportLoanRepay, getLoanRepayList } from "@/api/loan";
import { useRoute } from "vue-router";
import { BasicTypeEnum, getBasicList } from "@/api/basic";
import { handleColumTree } from "@/utils/tree";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Download from "@iconify-icons/ep/download";
import { getParams } from "@/views/components/ag-grid/utils";

export function useRepayInterest() {
  const route = useRoute();
  const id = route.query?.id;
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
  const cacheLoanUnitTree = ref<any>({});
  const cacheLoanTypeTree = ref<any>({});
  const gridOptions: GridOptions<any> = {
    defaultColDef: {
      suppressHeaderMenuButton: true
    },
    columnTypes: {
      ...columnType,
      loan_unit: {
        valueFormatter: params => {
          return params.value.name;
        },
        filter: "agSetColumnFilter",
        filterParams: {
          treeList: true,
          values: params => {
            getBasicList({ params: { type: BasicTypeEnum.LOAN_UNIT } }).then(
              res => {
                cacheLoanUnitTree.value = handleColumTree(res.data);
                params.success(res.data);
              }
            );
          },
          treeListPathGetter: data => {
            const path = cacheLoanUnitTree.value[data.id];
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
      },
      loan_type: {
        valueFormatter: params => {
          return params.value.name;
        },
        filter: "agSetColumnFilter",
        filterParams: {
          treeList: true,
          values: params => {
            getBasicList({ params: { type: BasicTypeEnum.LOAN_TYPE } }).then(
              res => {
                cacheLoanTypeTree.value = handleColumTree(res.data);
                params.success(res.data);
              }
            );
          },
          treeListPathGetter: data => {
            const path = cacheLoanTypeTree.value[data.id];
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
    columnDefs: [
      { field: "id" },
      {
        field: "loan_unit",
        headerName: "债务单位",
        type: "loan_unit"
      },
      {
        headerName: "债务名称",
        field: "loan_name",
        cellRenderer: function (params) {
          return params.data.debt_file
            ? `<a href="${params.data.debt_file}" style="color: #1890ff;" target="_blank">${params.value}</a>`
            : params.value;
        }
      },
      { field: "loan_type", headerName: "债务类型", type: "loan_type" },
      { field: "due_date", headerName: "到期日", type: "date", width: 150 },
      { field: "due_amount", headerName: "到期金额", type: "number" },
      { field: "loan_interest_amount", headerName: "债务利息", type: "number" },
      { field: "loan_amount", headerName: "债务金额", type: "number" },
      {
        field: "repay_amount",
        headerName: "还本金额",
        type: "number"
      },
      {
        field: "repay_date",
        headerName: "还本日期",
        type: "date",
        width: 150
      },
      { field: "sign_date", headerName: "签订时间", type: "date", width: 150 }
    ],
    pagination: true,
    paginationPageSize: pageSize.value,
    paginationPageSizeSelector: [10, 20, 30, 50],
    selection: {
      mode: "multiRow",
      selectAll: "all",
      checkboxes: true,
      enableClickSelection: true,
      enableMultiSelectWithClick: true
    },
    // onGridReady: onGridReady
    getContextMenuItems: params => {
      const node = params.node;
      return [
        {
          name: "详情",
          disabled: !node?.data?.id,
          action: () => {
            openNew(String(node.data.id));
          }
        },
        {
          name: "删除所选",
          disabled: !node?.data?.id,
          action: deleteSelected(String(node.data.id))
        }
      ];
    }
  };

  const buttons: Array<ToolButton | string> = [
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
    return exportLoanRepay({ params: params }).then(() => {
      message("正在导出，请稍后", { type: "success" });
    });
  };
  const exportAll = () => {
    const params = getParams(options, true);
    console.log(params);
    return exportLoanRepay({ params: params }).then(() => {
      message("正在导出，请稍后", { type: "success" });
    });
  };

  function openNew(id?: string) {
    router.push({
      path: "/repay-interest/repay/detail",
      query: { id }
    });
  }

  async function loadRows(params) {
    if (id) {
      params["loan"] = id;
    }
    return getLoanRepayList({ params: params }).then(res => {
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
    gridName: "还本付息",
    gridOptions: gridOptions,
    buttons: buttons,
    loadRows: loadRows
  };
  console.log(options);

  const deleteSelected = (id: string) => () => {
    deleteLoanRepay(id).then(res => {
      if (!res || res.success) {
        message("删除成功", { type: "success" });
        api.reload();
      } else {
        message("删除失败", { type: "error" });
      }
    });
  };

  return {
    componentRef,
    options
  };
}
