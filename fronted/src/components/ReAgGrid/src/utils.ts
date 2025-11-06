import type { ServerSideGridOptions } from "@/components/ReAgGrid/src/server-type";

export function getParams(
  options: ServerSideGridOptions<any>,
  needPage?: boolean
) {
  const filterModel = options.api.getFilterModel();
  const filters = Object.keys(filterModel).reduce((acc, key) => {
    const value = filterModel[key];
    // 根据 filterType 处理不同的过滤器
    if (
      value.filterType === "set" &&
      Array.isArray(value.values) &&
      value.values.length > 0
    ) {
      acc[key] = value.values[0]; // 取第一个值
    } else {
      acc[key] = value; // 其他类型直接赋值
    }
    return acc;
  }, {});
  if (needPage) {
    const currentPage = options.api.paginationGetCurrentPage() + 1;
    const pageSize = options.api.paginationGetPageSize();
    return {
      ...filters,
      page: currentPage,
      page_size: pageSize
    };
  }
  return filters;
}
