import { http } from "@/utils/http";
import type { Result } from "@/api/type";
import { handleTree } from "@/utils/tree";

export const getBasicList = (data?: object) => {
  return http.request<Result>("get", "/api/yb/basic/", data);
};

export const postBasic = (data?: object) => {
  return http.request<Result>("post", "/api/yb/basic/", data);
};

export const putBasic = (data?: object, id?: number) => {
  return http.request<Result>("put", `/api/yb/basic/${id}/`, data);
};

export const delBasic = (id?: number) => {
  return http.request<Result>("delete", `/api/yb/basic/${id}/`);
};

export enum BasicTypeEnum {
  GUARANTEE = 1,
  GUARANTEE_TYPE = 2,
  CREDIT = 3,
  LOAN_UNIT = 4,
  LOAN_TYPE = 5
}

export const getBasicTree = async (type: number) => {
  return await getBasicList({ params: { type: type } }).then(res => {
    return handleTree(res.data);
  });
};

export const exportBasicTemplate = (data?: object) => {
  return http.request<Result>("get", "/api/yb/basic/excel_template/", data);
};

// 上传文件
export const importBasic = (data?: object) => {
  return http.request<Result>("post", "/api/yb/basic/excel/", data, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  });
};
