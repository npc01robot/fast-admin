import { http } from "@/utils/http";
import type { ResultTable } from "@/api/common_type";

/** 授信列表 */
export const getCreditList = (data?: object) => {
  return http.request<ResultTable>("get", "/api/yb/credit/", data);
};

export const postCredit = (data: object) => {
  return http.request<ResultTable>("post", "/api/yb/credit/", data);
};

export const putCredit = (data?: object, id?: string) => {
  return http.request<ResultTable>("put", `/api/yb/credit/${id}/`, data);
};

export const deleteCredit = (id: number) => {
  return http.request<ResultTable>("delete", `/api/yb/credit/${id}/`);
};

export const getCreditDetail = (id: string) => {
  return http.request<ResultTable>("get", `/api/yb/credit/${id}/`);
};

export const exportCredit = (data?: object) => {
  return http.request<ResultTable>("get", "/api/yb/credit/export/", data);
};
