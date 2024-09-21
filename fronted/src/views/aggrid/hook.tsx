import { onBeforeMount, ref, shallowRef } from "vue";
import { getGrid } from "@/api/aggrid";

export function useAgGrid() {
  const pagination = true;
  const paginationPageSize = ref(10);
  const paginationPageSizeSelector = [10, 20, 30, 50];
  const paginationNumberFormatter = ref(null);
  const gridApi = shallowRef();
  const columnDefs = ref([
    { field: "id" },
    { field: "name" },
    { field: "age" },
    { field: "email" }
  ]);
  const rowData = ref([]);
  const gridOptions = {
    // 其他配置...
    localeText: {
      // 设置中文翻译
      page: "页",
      more: "更多",
      to: "至",
      of: "共",
      next: "下一个",
      last: "最后一个",
      first: "第一个",
      previous: "上一个",
      loadingOoo: "加载中...",
      // 更多翻译...
      noRowsToShow: "没有数据显示",
      // 列标题翻译
      selectAll: "全选"
    },
    defaultColDef: {
      filter: true,
      width: 150,
      resizable: true,
      hide: false
    }
  };

  async function onSearch() {
    // 处理搜索逻辑
    const data = await getGrid();
    rowData.value = data.data.list;
    paginationPageSize.value = data.data.pageSize;
    paginationNumberFormatter.value = data.data.total;
  }

  onBeforeMount(() => {
    onSearch();
  });

  const onGridReady = params => {
    gridApi.value = params.api;
  };

  return {
    pagination,
    paginationPageSize,
    paginationPageSizeSelector,
    gridOptions,
    rowData,
    columnDefs,
    onSearch,
    onGridReady
  };
}
