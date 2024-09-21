import { http } from "@/utils/http";
import type { ResultTable } from "@/api/type";

export const getGrid = (data?: object) => {
  return http.request<ResultTable>("get", "/api/fast/grid/grid/", { data });
};
