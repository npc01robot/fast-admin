// 服务端数据表格
import type {
  GridApi,
  GridOptions,
  IServerSideGetRowsParams
} from "ag-grid-community";

interface ToolButton {
  label?: string;
  icon?: string;
  name?: string;
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

type ILoadRowParams = {
  search: string;
  ordering?: string;
  page: number;
  page_size: number;
  offset: number;
  limit: number;
  [key: string]: any;
};
interface ILoadRows<RowData> {
  (
    params: ILoadRowParams,
    origin: IServerSideGetRowsParams
  ): Promise<{ rowCount?: number; rowData: RowData[] }>;
}
interface ServerSideGridOptions<RowData = any> {
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
   * 工具栏按钮
   */
  buttons?: Buttons;
  /**
   * 初始搜索关键字
   */
  keyword?: string;

  /**
   * 关键词搜索参数名 (默认为`search`)
   */
  searchParam?: string;

  api?: GridApi<RowData>;

  saveChanged?: (data: RowData[]) => Promise<boolean>;

  /**
   * 加载数据
   */
  loadRows: ILoadRows<RowData>;

  /**
   * 刷新数据
   */
  onReload?: () => void;
}

export type {
  ServerSideGridOptions,
  ILoadRowParams,
  ILoadRows,
  ToolButton,
  ToolButtonImpl,
  Buttons
};
