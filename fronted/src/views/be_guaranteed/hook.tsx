import { onMounted, onUnmounted, reactive, ref } from "vue";
import type { GridOptions } from "ag-grid-community";
import EventEmitter from "eventemitter3";
import type { ServerSideGridOptions } from "@/views/components/ag-grid/server-type";
import type { ToolButton } from "@/views/components/ag-grid/server-type";
import {
  deleteBeGuaranteed,
  exportBeGuarantee,
  getBeGuaranteedList
} from "@/api/guarantee";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import AddFill from "@iconify-icons/ep/plus";
import router from "@/router";
import { useMultiTagsStoreHook } from "@/store/modules/multiTags";
import { message } from "@/utils/message";
import { columnType } from "@/views/components/ag-grid/columnType";
import { BasicTypeEnum, getBasicList } from "@/api/basic";
import { handleColumTree } from "@/utils/tree";
import Download from "@iconify-icons/ep/download";
import { getParams } from "@/views/components/ag-grid/utils";
export function useBeGuaranteed() {
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
  const cacheGuaranteeTree = ref<any>([]);
  const gridOptions: GridOptions<any> = {
    columnTypes: {
      ...columnType,
      guarantee_unit: {
        valueFormatter: params => {
          return params.value.name;
        },
        filter: "agSetColumnFilter",
        filterParams: {
          treeList: true,
          values: params => {
            getBasicList({ params: { type: BasicTypeEnum.GUARANTEE } }).then(
              res => {
                cacheGuaranteeTree.value = handleColumTree(res.data);
                params.success(res.data);
              }
            );
          },
          treeListPathGetter: data => {
            const path = cacheGuaranteeTree.value[data.id];
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
    defaultColDef: {
      suppressHeaderMenuButton: true
    },
    columnDefs: [
      { field: "id" },
      {
        field: "guarantee_unit",
        headerName: "担保单位",
        type: "guarantee_unit"
      },
      {
        field: "be_guaranteed_unit",
        headerName: "被担保单位名称",
        type: "guarantee_unit"
      },
      { field: "ownership", headerName: "产权关系" },
      { field: "item", headerName: "担保事项" },
      { field: "sasac_record_amount", headerName: "备案金额", type: "number" },
      { field: "amount", headerName: "担保金额", type: "number" },
      { field: "start_date", headerName: "起始日期", type: "date" },
      { field: "end_date", headerName: "终止日期", type: "date" },
      { field: "remark", headerName: "备注" }
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
          action: () => {
            deleteSelected(String(node.data.id));
          }
        }
      ];
    }
  };

  const buttons: Array<ToolButton | string> = [
    {
      name: "create",
      icon: useRenderIcon(AddFill),
      label: "新增",
      // hidden: !ican.add,
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

  const exportAll = () => {
    const params = getParams(options, true);
    console.log(params);
    return exportBeGuarantee({ params: params }).then(() => {
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
    return exportBeGuarantee({ params: params }).then(() => {
      message("正在导出，请稍后", { type: "success" });
    });
  };
  function openNew(id?: string) {
    useMultiTagsStoreHook().handleTags("push", {
      path: `/guarantee/beGuaranteed/detail`,
      name: "BeGuaranteeDetail",
      meta: {
        title: `被担保详情`,
        dynamicLevel: 1
      }
    });
    router.push({
      path: "/guarantee/beGuaranteed/detail",
      query: { id }
    });
  }

  function deleteSelected(id: string) {
    deleteBeGuaranteed(id).then(res => {
      if (!res || res.success) {
        message("删除成功", { type: "success" });
        api.reload();
      } else {
        message("删除失败", { type: "error" });
      }
    });
  }
  async function loadRows(params) {
    return getBeGuaranteedList({ params: params }).then(res => {
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
    gridName: "被担保明细",
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
