<template>
  <div class="wrapper">
    <PureTableBar
      :title="options.gridName"
      :showColumn="false"
      @refresh="reload"
      @showColumn="showColumnChooser"
    >
      <template #buttons>
        <el-button
          v-for="button in buttons"
          :key="button.label"
          type="primary"
          :color="button.color"
          :disabled="button.disabled"
          :icon="useRenderIcon(button.icon)"
          @click="clickButton(button)"
        >
          {{ button.label }}
        </el-button>
      </template>
      <StGrid
        class="grid"
        :name="options.gridName"
        :grid-options="gridOptions"
      />
    </PureTableBar>
  </div>
</template>

<script setup lang="ts" generic="RowData">
import type {
  CellValueChangedEvent,
  ColDef,
  FilterChangedEvent,
  FilterModel,
  GetContextMenuItemsParams,
  GridApi,
  GridOptions,
  GridReadyEvent,
  IServerSideGetRowsParams,
  IServerSideSelectionState,
  RowDataTransaction,
  SelectionChangedEvent
} from "ag-grid-community";
import dayjs from "dayjs";
import {
  computed,
  defineComponent,
  onActivated,
  onDeactivated,
  reactive,
  shallowReactive,
  watch
} from "vue";
import StGrid from "./StGrid.vue";
import GridTextStatusComponent from "./GridTextStatusComponent.vue";
import { ServerSideGridOptions } from "@/views/components/ag-grid/server-type";
import {
  ToolButton,
  ToolButtonImpl
} from "@/views/components/ag-grid/tiny-type";
import { PureTableBar } from "@/components/RePureTableBar";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import AddFill from "@iconify-icons/ri/add-circle-line";

let api: GridApi | null = null;

// 内置功能按钮
const providedButtons = reactive({
  saveChanged: {
    label: "保存",
    icon: "save",
    color: "primary",
    get disabled() {
      return changedRows.size === 0;
    },
    action: saveChanged
  }
});
const defaultGridOptions: GridOptions<RowData> = {
  popupParent: document.body,
  cacheBlockSize: 30,
  suppressScrollOnNewData: true,
  rowModelType: "serverSide",
  rowSelection: "multiple",
  serverSideDatasource: {
    getRows: getRows
  },
  suppressCopyRowsToClipboard: true,
  components: {
    GridTextStatusComponent
  },
  defaultColDef: {
    menuTabs: ["filterMenuTab"],
    sortable: false
  },
  columnTypes: {
    datetime: {
      width: 140,
      valueFormatter: params => {
        return params.value
          ? dayjs(params.value).format("YYYY-MM-DD HH:mm")
          : "";
      },
      filter: "agDateColumnFilter",
      filterParams: {
        buttons: ["apply", "reset"],
        closeOnApply: true,
        defaultOption: "inRange",
        filterOptions: ["lessThan", "greaterThan", "inRange"],
        maxNumConditions: 1
      }
    }
  },
  statusBar: {
    statusPanels: [
      {
        statusPanel: "GridTextStatusComponent",
        align: "left",
        statusPanelParams: {
          label: "Rows",
          hidden: computed(() => vm.loading),
          value: computed(() => `${vm.rowCount ?? "-"}`)
        }
      },
      {
        statusPanel: "GridTextStatusComponent",
        align: "left",
        statusPanelParams: {
          label: "Selected",
          hidden: computed(() => !vm.selectedCount),
          value: computed(() => vm.selectedCount)
        }
      }
    ]
  }
};

const props = defineProps<{ options: ServerSideGridOptions<RowData> }>();
const options = props.options;
const _expose = {
  reload,
  saveChanged,
  getFilterParams,
  /**
   * 返回选中的行数
   */
  get selectedCount() {
    return vm.selectedCount;
  },
  /**
   * 返回当前总行数
   */
  get rowCount() {
    return vm.rowCount;
  }
};
defineExpose(_expose);

const changedRows = shallowReactive(new Set<RowData>());
const vm = reactive({
  keyword: "",
  ready: false,
  loading: false,
  rowCount: 0,
  selectedCount: 0,
  /**
   * 是否有过滤条件
   */
  filtered: false,
  searchParam: options.searchParam ?? "search",
  get changed() {
    return !!changedRows.size;
  }
});

watch(
  () => vm.loading,
  loading => {
    api?.setGridOption("loading", loading);
  }
);

function replaceFunc<T extends Function>(prev: T | undefined, next: T): T {
  const cb = arg => {
    next(arg);
    prev?.(arg);
  };
  return cb as any as T;
}

const gridOptions = computed(() => {
  const opts = options.gridOptions;
  opts.onGridReady = replaceFunc(opts.onGridReady, onGridReady);
  opts.onCellValueChanged = replaceFunc(
    opts.onCellValueChanged,
    onCellValueChanged
  );
  Object.getOwnPropertyNames(defaultGridOptions).forEach(key => {
    if (key in opts === false) {
      opts[key] = defaultGridOptions[key];
    } else if (key === "columnTypes") {
      opts[key] = { ...defaultGridOptions[key], ...opts[key] };
    } else if (key === "defaultColDef") {
      opts[key] = { ...defaultGridOptions[key], ...opts[key] };
    }
  });
  const columnDefs = opts.columnDefs ?? [];
  if (!columnDefs.find((n: ColDef) => n.colId === vm.searchParam)) {
    columnDefs.push({
      colId: vm.searchParam,
      hide: true,
      lockVisible: true,
      headerName: "搜索关键词",
      filter: "agTextColumnFilter"
    });
  }
  opts.getContextMenuItems = proxyGetContextMenuItems.bind(
    null,
    opts.getContextMenuItems?.bind(opts)
  );
  return opts;
});
const showColumnChooser = () => {
  api?.showColumnChooser();
};
function isTrue(value?: boolean | (() => boolean)) {
  return typeof value === "function" ? value() : value;
}
function copyButton(
  baseBtn: ToolButton,
  providedBtn: ToolButton
): ToolButtonImpl {
  const btn = { ...providedBtn, ...baseBtn };
  // disabled和hidden需要叠加
  btn.disabled = isTrue(providedBtn.disabled) || isTrue(baseBtn.disabled);
  btn.hidden = isTrue(providedBtn.hidden) || isTrue(baseBtn.hidden);
  if (!baseBtn.action || typeof baseBtn.action === "string") {
    btn.action = providedBtn.action;
  }
  return btn as any;
}

const buttons = computed(() => {
  return (
    options.buttons?.map(btn => {
      if (typeof btn === "string" || typeof btn.action === "string") {
        const name = typeof btn === "string" ? btn : (btn.action as string);
        const refBtn = providedButtons[name];
        if (refBtn) {
          refBtn.name = name;
          let base = typeof btn === "string" ? {} : btn;
          return copyButton(base, refBtn);
        } else {
          throw new Error(`未知的按钮：${name}`);
        }
      }
      return copyButton(btn, {});
    }) ?? []
  ).filter(n => !n.hidden);
});

function cleanUp() {
  changedRows.clear();
  api?.setServerSideSelectionState({
    selectAll: false,
    toggledNodes: []
  });
}
async function reload() {
  cleanUp();
  props.options.onReload?.();
  api?.refreshServerSide({ purge: true });
}

async function reset() {
  vm.keyword = "";
  options.keyword = "";
  api?.setFilterModel({});
  api!.onFilterChanged();
}

// 搜索关键词
function search() {
  cleanUp();
  options.keyword = (vm.keyword ?? "").trim();
  api?.setColumnFilterModel(
    vm.searchParam,
    options.keyword
      ? { filterType: "text", type: "equals", filter: vm.keyword }
      : null
  );
  api?.onFilterChanged();
}

function hookApi(api: GridApi<RowData>) {
  api.applyTransaction = proxyApplyTransaction.bind(
    null,
    api.applyTransaction.bind(api)
  );
  api.setGridOption = proxySetGridOptions.bind(
    null,
    api.setGridOption.bind(api)
  );
}
function proxyApplyTransaction(
  applyTransaction: CallableFunction,
  transaction: RowDataTransaction<RowData>
) {
  transaction.add?.forEach(row => changedRows.add(row));
  transaction.update?.forEach(row => changedRows.add(row));
  transaction.remove?.forEach(row => changedRows.delete(row));
  return applyTransaction(transaction);
}
function proxySetGridOptions(cb, key, val) {
  if (key === "rowData") {
    changedRows.clear();
  }
  return cb(key, val);
}
function proxyGetContextMenuItems(
  cb,
  params: GetContextMenuItemsParams<RowData>
) {
  if (!cb) return params.defaultItems;
  const node = params.node;
  if (node && !node.isSelected()) {
    const range = params.api.getCellRanges();
    const selectionIndexs = new Set<number>();
    if (range?.length) {
      for (let r of range) {
        if (!r.startRow || !r.endRow) continue;
        let start = r.startRow!.rowIndex;
        let end = r.endRow.rowIndex;
        if (start > end) [start, end] = [end, start];
        for (let i = start; i <= end; i++) {
          selectionIndexs.add(i);
        }
      }
    }
    if (selectionIndexs.size) {
      params.api.deselectAll();
      for (let i of Array.from(selectionIndexs)) {
        const row = params.api.getDisplayedRowAtIndex(i)!;
        row.setSelected(true);
      }
    } else {
      node.setSelected(true, true);
    }
  }
  const items = cb(params);
  return items;
}
async function onGridReady(event: GridReadyEvent<RowData>) {
  api = event.api;
  hookApi(api);
  options.api = api;
  vm.ready = true;
  api.addEventListener("selectionChanged", (event: SelectionChangedEvent) => {
    const state =
      event.api.getServerSideSelectionState() as IServerSideSelectionState;
    if (state.selectAll) {
      vm.selectedCount = vm.rowCount - state.toggledNodes.length;
    } else {
      vm.selectedCount = state.toggledNodes.length;
    }
  });
  api.addEventListener("filterChanged", (event: FilterChangedEvent) => {
    event.api.setServerSideSelectionState({
      selectAll: false,
      toggledNodes: []
    });
  });
}
function onCellValueChanged(event: CellValueChangedEvent<RowData>) {
  const data = event.data;
  changedRows.add(data);
}

/**
 * 点击按钮
 * @param btn
 */
function clickButton(btn: ToolButton) {
  if (typeof btn.action === "function") {
    btn.action(btn);
  }
}

/**
 * 保存变更数据
 */
async function saveChanged() {
  vm.loading = true;
  const data = Array.from(changedRows);
  const success = await options.saveChanged?.(data);
  vm.loading = false;
  if (success) {
    await reload();
  }
}

function getFilterParams(): Record<string, any> {
  const model = api?.getFilterModel();
  const params = _getFilterParams(model as FilterModel);
  return params;
}

/**
 * 加载数据
 */
async function getRows(params: IServerSideGetRowsParams) {
  const args: any = {};
  if (Object.keys(params.request.filterModel ?? {}).length) {
    const extend = _getFilterParams(params.request.filterModel as FilterModel);
    Object.assign(args, extend);
    vm.filtered = true;
  } else {
    vm.filtered = false;
  }

  if (params.request.sortModel?.length) {
    args["ordering"] = params.request.sortModel
      .map(n => (n.sort === "asc" ? "" : "-") + n.colId)
      .join(",");
  }

  const pageSize =
    (params.request.endRow ?? 30) - (params.request.startRow ?? 0);
  const page = (params.request.startRow ?? 0) / pageSize + 1;
  args["page"] = page;
  args["page_size"] = pageSize;
  args["offset"] = params.request.startRow ?? 0;
  args["limit"] = pageSize;

  const result = await options.loadRows(args, params);
  params.success(result);
  vm.rowCount = result.rowCount ?? result.rowData.length;
}

function _getFilterParams(filterModel: FilterModel) {
  const params = {} as any;
  const get_date = (date: string | null, fillTime = false) => {
    if (!date) return null;
    if (fillTime) {
      date = date.replace("00:00:00", "23:59:59");
    }
    return date + "+08:00";
  };
  for (let [key, filter] of Object.entries(filterModel)) {
    switch (filter.filterType) {
      case "set":
        params[key] = filter.values;
        break;
      case "date":
        switch (filter.type) {
          case "lessThan":
            params[`${key}_before`] = get_date(filter.dateFrom);
            break;
          case "greaterThan":
            params[`${key}_after`] = get_date(filter.dateFrom);
            break;
          case "inRange":
            params[`${key}_after`] = get_date(filter.dateFrom);
            params[`${key}_before`] = get_date(filter.dateTo, true);
            break;
        }
        break;
      case "text":
        switch (filter.type) {
          case "equals":
            params[key] = filter.filter;
            break;
        }
    }
  }
  return params;
}
</script>

<style scoped>
.wrapper {
  flex: 1 1 100%;
  display: flex;
  flex-flow: column;
  width: 100%;
  height: var(--client-height);
}

.search {
  display: flex;
  flex: 0 0 auto;
  padding: 5px;
  align-items: center;
  background-color: #f7f7f7;
  border: var(--bs-border);
  border-bottom: 0;
}

.search-inline {
  display: flex;
  flex: 0 1 100%;
  gap: 10px;
}

.keyword {
  flex: 0 1 500px;
}

.grid {
  flex: 1 1 100%;
  width: 100%;
  height: 100%;
}

.grid :deep(.data-changed .ag-cell-value) {
  display: inline-flex;
  align-items: center;
  gap: 2px;

  :deep(&:after) {
    content: "";
    display: inline-block;
    width: 5px;
    height: 5px;
    background-color: var(--bs-theme);
    border-radius: 2.5px;
    box-shadow: 1px 1px 1px #000;
  }
}
</style>
