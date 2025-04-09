export type Result = {
  success: boolean;
  code: number;
  msg?: string;
  data?: any;
};

export type ResultTable = {
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
};
