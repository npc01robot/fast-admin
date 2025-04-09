import { http } from "@/utils/http";
import type { ResultTable } from "@/api/common_type";
import type { Result } from "@/api/type";

/** 担保单位 */
export const getGuaranteeList = (data?: object) => {
  return http.request<ResultTable>("get", "/api/yb/guarantee/", data);
};

export const postGuarantee = (data: object) => {
  return http.request<Result>("post", "/api/yb/guarantee/", data);
};

export const putGuarantee = (data?: object, id?: string) => {
  return http.request<Result>("put", `/api/yb/guarantee/${id}/`, data);
};

export const deleteGuarantee = (id: string) => {
  return http.request<Result>("delete", `/api/yb/guarantee/${id}/`);
};

export const getGuaranteeDetail = (id: string) => {
  return http.request<Result>("get", `/api/yb/guarantee/${id}/`);
};

/** 被担保单位 */
export const getBeGuaranteedList = (data?: object) => {
  return http.request<ResultTable>("get", "/api/yb/be_guaranteed/", data);
};

export const postBeGuaranteed = (data: object) => {
  return http.request<Result>("post", "/api/yb/be_guaranteed/", data);
};

export const putBeGuaranteed = (data?: object, id?: string) => {
  return http.request<Result>("put", `/api/yb/be_guaranteed/${id}/`, data);
};

export const deleteBeGuaranteed = (id: string) => {
  return http.request<Result>("delete", `/api/yb/be_guaranteed/${id}/`);
};

export const getBeGuaranteedDetail = (id: string) => {
  return http.request<Result>("get", `/api/yb/be_guaranteed/${id}/`);
};

export const exportGuarantee = (data?: object) => {
  return http.request<ResultTable>("get", "/api/yb/guarantee/export/", data);
};

export const exportBeGuarantee = (data?: object) => {
  return http.request<ResultTable>(
    "get",
    "/api/yb/be_guaranteed/export/",
    data
  );
};
