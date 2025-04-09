import { http } from "@/utils/http";
import type { ResultTable } from "@/api/common_type";

/**  */
export const getFinanceList = (data?: object) => {
  return http.request<ResultTable>("get", "/api/yb/finance/", data);
};

export const downloadFinanceList = (data?: object) => {
  return http.request<ResultTable>("get", "/api/yb/finance/export/", data);
};
