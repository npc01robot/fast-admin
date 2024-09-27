import { onMounted, onUnmounted, reactive, ref } from "vue";
import { getGrid } from "@/api/aggrid";
import type { GridOptions } from "ag-grid-community";
import EventEmitter from "eventemitter3";
import type { ServerSideGridOptions } from "@/views/components/ag-grid/server-type";
import type { ToolButton } from "@/views/components/ag-grid/server-type";
export function useAgGrid() {
  const pageSize = ref(30);
  const pageCount = ref(0);
  const componentRef = ref<ServerSideGridElement<any>>();
  type _GridType = typeof componentRef.value;
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
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

  const gridOptions: GridOptions<any> = {
    columnDefs: [
      { field: "id" },
      {
        field: "name",
        mainMenuItems: [
          {
            name: "A Custom Item",
            action: () => {
              console.log("A Custom Item selected");
            },
            icon: '<img src="https://www.ag-grid.com/example-assets/lab.png" style="width: 14px;" />'
          },
          {
            name: "Another Custom Item",
            action: () => {
              console.log("Another Custom Item selected");
            },
            checked: true
          },
          "resetColumns"
        ]
      },
      { field: "description" },
      { field: "created_at" },
      { field: "updated_at" },
      {
        field: "is_deleted",
        valueFormatter: params => {
          if (params.value) {
            return "已删除";
          } else {
            return "未删除";
          }
        },
        filter: "agSetColumnFilter",
        filterParams: {
          valueFormatter: params => {
            return params.value.label;
          },
          keyCreator: params => params.value.value,
          closeOnApply: true,
          excelMode: "windows",
          buttons: ["apply", "reset"],
          values: [
            { label: "未删除", value: false },
            { label: "已删除", value: true }
          ]
        }
      }
    ],
    pagination: true,
    paginationPageSize: pageSize.value,
    paginationPageSizeSelector: [10, 20, 30, 50],
    // onGridReady: onGridReady
    getContextMenuItems: params => {
      const node = params.node;
      return [
        {
          name: "物流商详情",
          disabled: !node?.data?.id,
          icon: "detail"
        },
        {
          name: "启用所选",
          icon: "enable"
          // action: bulkEnable
        },
        {
          name: "禁用所选",
          icon: "disable"
          // action: bulkDisable
        },
        {
          name: "删除所选",
          icon: "trash"
          // action: bulkDelete
        }
      ];
    }
  };

  const buttons: Array<ToolButton | string> = [
    {
      name: "create",
      icon: "new",
      label: "新增"
      // hidden: !ican.add,
      // action: openNew
    },
    {
      name: "logs",
      label: "操作日志"
      // action: showLogs
    }
  ];

  async function loadRows(params) {
    return getGrid({ params: params }).then(res => {
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
    gridName: "sysconfig",
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
