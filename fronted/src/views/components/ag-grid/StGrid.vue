<template>
  <div>
    <ag-grid-vue
      ref="gridRef"
      :gridOptions="gridOptions"
      style="height: 80vh; width: 100%; flex: 1"
      class="ag-theme-quartz"
    />
  </div>
</template>

<script lang="ts">
import "ag-grid-community/styles/ag-grid.css"; // Mandatory CSS required by the Data Grid
import "ag-grid-community/styles/ag-theme-quartz.css"; // Optional Theme applied to the Data Grid
import { ClientSideRowModelModule } from "ag-grid-community";
import type {
  ColDef,
  ColumnResizedEvent,
  ColumnRowGroupChangedEvent,
  ColumnVisibleEvent,
  GridApi,
  GridOptions,
  GridReadyEvent,
  MenuItemDef
} from "ag-grid-community";
import { ModuleRegistry } from "ag-grid-community";
import {
  ClipboardModule,
  ColumnsToolPanelModule,
  LicenseManager,
  MenuModule,
  RangeSelectionModule,
  RichSelectModule,
  RowGroupingModule,
  ServerSideRowModelModule,
  SetFilterModule,
  StatusBarModule
} from "ag-grid-enterprise";
import { ref, watch } from "vue";

ModuleRegistry.registerModules([
  ClientSideRowModelModule,
  MenuModule,
  ColumnsToolPanelModule,
  ClipboardModule,
  RangeSelectionModule,
  RichSelectModule,
  RowGroupingModule,
  ServerSideRowModelModule,
  SetFilterModule,
  StatusBarModule
]);
Object.assign(LicenseManager.prototype, {
  validateLicense: () => false,
  isDisplayWatermark: () => false,
  getWatermarkMessage: () => false
});
</script>

<script setup lang="ts" generic="RowData = any">
import { AgGridVue } from "ag-grid-vue3";

const props = defineProps({
  name: {
    type: String,
    required: false
  },
  gridOptions: {
    type: Object as () => GridOptions<RowData>,
    required: true
  },
  rowData: {
    type: Array as () => any[],
    required: false
  }
});

const gridRef = ref<AgGridElement<RowData>>();
defineExpose({
  get api() {
    return gridRef.value?.api as GridApi<RowData>;
  }
});
watch(
  () => props.rowData,
  rowData => {
    const api = gridRef.value?.api;
    if (api) {
      api?.setGridOption("rowData", rowData);
    }
  }
);

/**
 * 默认参数
 */
const DEFAULT_OPTIONS = {
  suppressDragLeaveHidesColumns: true,
  stopEditingWhenCellsLoseFocus: true
};

class GridStorage {
  name: string = "";
  _columnWidth: Record<string, number> = {};
  _groupColumns?: string[];
  _columnVisible: Record<string, boolean> = {};
  _delayTimer: any = null;

  get cacheKey() {
    return `GridCache:${this.name}`;
  }

  setColumnWidth(colId: string, width: number) {
    if (!colId) return;
    this._columnWidth[colId] = width;
    this.delaySave();
  }
  setColumnGrouped(columns: string[]) {
    this._groupColumns = columns;
    this.delaySave();
  }
  setColumnVisible(columns: string[], visible: boolean) {
    columns.forEach(colId => {
      this._columnVisible[colId] = visible;
    });
    this.delaySave();
  }

  /**
   * 延时保存表格状态
   */
  delaySave() {
    if (this._delayTimer) {
      clearTimeout(this._delayTimer);
    }
    this._delayTimer = setTimeout(() => {
      this._delayTimer = 0;
      this.save();
    }, 200);
  }

  /**
   * 保存表格状态
   */
  save() {
    const data = JSON.stringify({
      columnWidth: this._columnWidth,
      groupColumns: this._groupColumns,
      columnVisible: this._columnVisible
    });
    localStorage.setItem(this.cacheKey, data);
  }

  read() {
    const data = localStorage.getItem(this.cacheKey);
    let profile: Record<string, any> = {};
    if (data) {
      try {
        profile = JSON.parse(data || "{}");
      } catch (error) {
        console.error(error);
      }
    }

    let { columnWidth = {}, groupColumns, columnVisible = {} } = profile || {};
    this._columnWidth = columnWidth ?? {};
    this._groupColumns = groupColumns;
    this._columnVisible = columnVisible;
  }

  modify(gridOption: GridOptions) {
    // 附加默认参数
    Object.keys(DEFAULT_OPTIONS).forEach(key => {
      if (!Object.hasOwn(gridOption, key)) {
        gridOption[key] = DEFAULT_OPTIONS[key];
      }
    });

    // 设置列宽
    Object.keys(this._columnWidth).forEach(colId => {
      const width = this._columnWidth[colId];
      if (typeof width == "number" && width >= 0) {
        let column = gridOption.columnDefs?.find(
          (col: ColDef) => (col.colId || col.field) === colId
        ) as ColDef;
        if (!column && colId === "ag-Grid-AutoColumn") {
          column = gridOption.autoGroupColumnDef as ColDef;
        }
        if (column) {
          column.width = width;
        }
      }
    });
    // 设置隐藏
    Object.keys(this._columnVisible).forEach(colId => {
      const visible = this._columnVisible[colId];
      let column = gridOption.columnDefs?.find(
        (col: ColDef) => (col.colId || col.field) === colId
      ) as ColDef;
      if (column) {
        column.hide = !visible;
      }
    });
    // 设置分组
    if (Array.isArray(this._groupColumns)) {
      const colDefs = gridOption.columnDefs?.filter(
        (colDef: ColDef) => colDef.enableRowGroup
      ) as ColDef[];
      let i = 0;
      colDefs?.forEach(colDef => {
        if (colDef.rowGroup) {
          delete colDef.rowGroup;
          delete colDef.hide;
        }
      });
      for (let i = 0; i < this._groupColumns.length; i++) {
        const colId = this._groupColumns[i];
        const colDef = colDefs.find(
          colDef => (colDef.colId || colDef.field) === colId
        );
        if (colDef) {
          colDef.rowGroup = true;
          colDef.rowGroupIndex = i;
          colDef.hide = true;
        }
      }
    }
    // 如果没有分组, 显示自动分组里定义的field列
    if (
      gridOption.autoGroupColumnDef?.field &&
      !gridOption.columnDefs?.some((colDef: ColDef) => colDef.rowGroup)
    ) {
      const colDef = gridOption.columnDefs?.find(
        (colDef: ColDef) =>
          colDef.field === gridOption.autoGroupColumnDef!.field
      ) as ColDef;
      if (colDef?.hide) {
        colDef.hide = false;
      }
    }
  }
}

const TIME_ZONE_OFFSET = new Date().getTimezoneOffset() * 60 * 1000;
const defaultGridOptions: GridOptions = {
  columnTypes: {
    datetime: {
      width: 140,
      valueFormatter: params => {
        if (params.value && params.value !== "...") {
          let date = new Date(Date.parse(params.value) - TIME_ZONE_OFFSET);
          return date
            .toISOString()
            .replace(
              /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}).*$/,
              "$1-$2-$3 $4:$5"
            );
        }
        return params.value;
      }
    }
  },
  defaultColDef: {
    width: 120
  }
};

const cache = new GridStorage();

function hookOptions(gridOptions: GridOptions) {
  const _getContextMenuItems = gridOptions.getContextMenuItems;
  if (_getContextMenuItems) {
    gridOptions.getContextMenuItems = params => {
      const menus = _getContextMenuItems(params);
      return modifyContextMenuItems(menus);
    };
  }
  // 列类型
  gridOptions.columnTypes = {
    ...defaultGridOptions.columnTypes,
    ...gridOptions.columnTypes
  };
  // 默认列
  gridOptions.defaultColDef = {
    ...defaultGridOptions.defaultColDef,
    ...gridOptions.defaultColDef
  };
  // GridReady
  const _gridReady = gridOptions.onGridReady;
  gridOptions.onGridReady = event => {
    onGridReady(event);
    _gridReady?.(event);
  };
  // 数据初值
  if (props.rowData) {
    gridOptions.rowData = props.rowData;
  }
}
if (props.name) {
  cache.name = props.name;
  cache.read();
  cache.modify(props.gridOptions);
  hookOptions(props.gridOptions);
  watch(() => props.gridOptions, hookOptions);
}

function onGridReady(event: GridReadyEvent) {
  const api = event.api;
  api.addEventListener("columnResized", onColumnResized);
  api.addEventListener("columnRowGroupChanged", onColumnRowGroupChanged);
  api.addEventListener("columnVisible", onColumnVisible);
}

function modifyContextMenuItems(menus: (MenuItemDef | string)[]) {
  if (!menus) return menus;
  return menus.map(menu => {
    if (menu === "-") menu = "separator";
    if (typeof menu == "string") return menu;
    if (Array.isArray(menu?.subMenu)) {
      menu.subMenu = modifyContextMenuItems(menu.subMenu);
    }
    // if (
    //   typeof menu.icon === "string" &&
    //   ALL_SUPPORT_ICONS.includes(menu.icon)
    // ) {
    //   menu.icon = useRenderIcon(User);
    // }
    return menu;
  });
}

function onColumnResized(event: ColumnResizedEvent) {
  if (event.column) {
    const colId = event.column.getColId();
    cache.setColumnWidth(colId, event.column.getActualWidth());
  }
}

function onColumnRowGroupChanged(event: ColumnRowGroupChangedEvent) {
  const columns = event.columns?.map(col => col.getColId()) as string[];
  cache.setColumnGrouped(columns);
}

function onColumnVisible(event: ColumnVisibleEvent) {
  const columns = event.columns?.map(n => n.getColId());
  if (columns && event.visible != null) {
    cache.setColumnVisible(columns, event.visible);
  }
}
</script>

<style>
.app-grid {
  width: 100%;
  height: 100%;
}

.app-grid.grid-border {
  border: 1px solid var(--ag-border-color, #888);
}
</style>
