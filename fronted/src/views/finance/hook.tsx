import { onMounted, onUnmounted, reactive, ref } from "vue";
import type { GridOptions } from "ag-grid-community";
import EventEmitter from "eventemitter3";
import type { ServerSideGridOptions } from "@/views/components/ag-grid/server-type";
import type { ToolButton } from "@/views/components/ag-grid/server-type";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import { getParams } from "@/views/components/ag-grid/utils";
import { deleteLoan, getLoanList } from "@/api/loan";
import { columnType } from "@/views/components/ag-grid/columnType";
import { useMultiTagsStoreHook } from "@/store/modules/multiTags";
import router from "@/router";
import { message } from "@/utils/message";
import { BasicTypeEnum, getBasicList } from "@/api/basic";
import { handleColumTree } from "@/utils/tree";
import Download from "@iconify-icons/ep/download";
import { exportCredit } from "@/api/credit";

export function useFinanceHook() {
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

  const cacheOrgnizationTree = ref<any>({});
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
      },
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
    columnDefs: [
      { field: "id" },
      {
        field: "name",
        headerName: "贷款单位名称",
        type: "loan_unit"
      },
      { field: "type", headerName: "贷款类型", type: "loan_type" },
      {
        field: "credit_organization",
        headerName: "授信金融机构",
        type: "bank"
      },
      { field: "credit_amount", headerName: "授信总金额", type: "number" },
      { field: "loan_balance", headerName: "贷款余额", type: "number" },
      { field: "contract_rate", headerName: "合同利率", type: "percent" },
      { field: "overall_rate", headerName: "综合成本", type: "percent" },
      { field: "loan_date", headerName: "借款日", type: "date", width: 150 },
      { field: "due_date", headerName: "到期日", type: "date", width: 150 }
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
          name: "融资详情",
          disabled: !node?.data?.id,
          action: () => {
            openNew(node.data.id);
          }
        },

        {
          name: "还款计划",
          disabled: !node?.data?.id,
          action: () => {
            openRepayPlan(String(node.data.id));
          }
        },
        {
          name: "付息计划",
          disabled: !node?.data?.id,
          action: () => {
            openInterestPlan(String(node.data.id));
          }
        },
        {
          name: "新增还款",
          disabled: !node?.data?.id,
          action: () => {
            openRepayNew(String(node.data.id));
          }
        },
        {
          name: "新增付息",
          disabled: !node?.data?.id,
          action: () => {
            openInterestNew(String(node.data.id));
          }
        },
        {
          name: "删除所选",
          disabled: !node?.data?.id,
          action: () => {
            deleteRow(String(node.data.id));
          }
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

  function openNew(id?: string) {
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
      query: { id }
    });
  }

  function openRepayPlan(id: string) {
    router.push({
      name: "Repay",
      query: { id }
    });
  }

  function openInterestPlan(id: string) {
    router.push({
      name: "Interest",
      query: { id }
    });
  }

  function deleteRow(id: string) {
    deleteLoan(id).then(res => {
      if (!res || res.success) {
        message("删除成功", { type: "success" });
        api.reload();
      } else {
        message("删除失败", { type: "error" });
      }
    });
  }

  function openRepayNew(id: string) {
    router.push({
      name: "RepayDetail",
      query: { loanId: id }
    });
  }

  function openInterestNew(id: string) {
    router.push({
      name: "InterestDetail",
      query: { loanId: id }
    });
  }
  async function loadRows(params) {
    return getLoanList({ params: params }).then(res => {
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
    gridName: "融资情况",
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
