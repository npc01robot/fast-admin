interface Result {
  success: boolean;
  code: number;
  msg?: string;
  data?: any;
}

interface ResultTable {
  success: boolean;
  code: number;
  msg: string;
  data?: {
    list?: Array<any>;
    total?: number;
    page?: number;
    pageSize?: number;
    pageCount?: number;
  };
}
export type { Result, ResultTable };
