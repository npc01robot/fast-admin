import type { GridApi, GridOptions } from "ag-grid-community";

interface ToolButton {
  label?: string;
  icon?: string;
  disabled?: boolean | (() => boolean);
  hidden?: boolean;
  color?: string;
  action?: ((ToolButton?) => void) | string;
}

interface ToolButtonImpl extends ToolButton {
  disabled?: boolean;
  action: (btn: ToolButton) => void;
}

type Buttons = Array<ToolButton | string>;

interface TinyGridOptions<RowData> {
  /**
   * 表格名称，用于保存列宽等信息
   */
  gridName: string;
  /**
   * AgGrid表格定义
   */
  gridOptions: GridOptions<RowData>;
  /**
   * 搜索框提示
   */
  searchPlaceholder?: string;
  /**
   * 加载表格数据
   */
  loadData: () => Promise<RowData[]>;
  /**
   * 工具栏按钮
   */
  buttons?: Buttons;

  api?: GridApi<RowData>;

  saveChanged?: (data: RowData[]) => Promise<boolean>;

  onQuickFilterChanged?: (keyword: string) => void;
}

export type { TinyGridOptions, ToolButton, ToolButtonImpl, Buttons };
