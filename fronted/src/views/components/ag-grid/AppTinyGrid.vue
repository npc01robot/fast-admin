<template>
  <div class="wrapper">
    <StGrid class="grid" :name="options.gridName" :grid-options="gridOptions" />
  </div>
</template>

<!-- 该组件用于少量数据的简单管理 -->

<script setup lang="ts" generic="RowData">
import type {
  CellValueChangedEvent,
  GetContextMenuItemsParams,
  GridApi,
  GridOptions,
  GridReadyEvent,
  RowDataTransaction
} from "ag-grid-community";
import { computed, reactive, shallowReactive, watch } from "vue";
import StGrid from "./StGrid.vue";
import GridTextStatusComponent from "./GridTextStatusComponent.vue";
import {
  TinyGridOptions,
  ToolButton,
  ToolButtonImpl
} from "@/views/components/ag-grid/tiny-type";

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
  components: {
    GridTextStatusComponent
  },
  statusBar: {
    statusPanels: [
      { statusPanel: "agTotalAndFilteredRowCountComponent", align: "left" }
    ]
  }
};

const props = defineProps<{ options: TinyGridOptions<RowData> }>();
const options = props.options;
defineExpose({
  search: search,
  saveChanged: saveChanged
});

const changedRows = shallowReactive(new Set<RowData>());
const vm = reactive({
  keyword: "",
  ready: false,
  loading: false,
  get changed() {
    return !!changedRows.size;
  }
});
watch(
  () => vm.keyword,
  keyword => {
    api?.setGridOption("quickFilterText", keyword);
    options.onQuickFilterChanged?.(keyword);
  }
);
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
    }
  });
  opts.getContextMenuItems = proxyGetContextMenuItems.bind(
    null,
    opts.getContextMenuItems?.bind(opts)
  );
  return opts;
});

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

async function search() {
  if (vm.loading) return;
  vm.loading = true;
  changedRows.clear();
  const data = await options.loadData();
  api?.setGridOption("rowData", data);
  vm.loading = false;
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
      for (let i of selectionIndexs) {
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
  await search();
  vm.ready = true;
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
    await search();
  }
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
  flex: 0 1 550px;
  gap: 10px;
}

.keyword {
  flex: 1 1 auto;
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
