import { http } from "@/utils/http";
import type { ResultTable, Result } from "@/api/type";

/** 导出列表 */
export const exportList = (data?: object) => {
  return http.request<ResultTable>("get", "/api/yb/export/", data);
};

/** 导出类型 */
export const exportType = () => {
  return http.request<Result>("get", "/api/yb/export_type/");
};

export const uploadFile = (data?: object) => {
  return http.request<Result>("post", "/api/yb/upload/", data);
};

export const importFile = (data?: object) => {
  return http.request<Result>("post", "/api/yb/import/", data);
};
