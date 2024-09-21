import { http } from "@/utils/http";

type Result = {
  success: boolean;
  code: number;
  msg?: string;
  data?: any;
};

type ResultTable = {
  success: boolean;
  code: number;
  msg: string;
  data?: {
    list?: Array<any>;
    total?: number;
    page?: number;
    page_size?: number;
    page_count?: number;
  };
};

/** 获取系统管理-用户管理列表 */
export const getUserList = (data?: object) => {
  return http.request<ResultTable>("get", "/api/auth/user/", { params: data });
};
/** 创建系统管理-用户管理 */
export const createUser = (data?: object) => {
  return http.request<ResultTable>("post", "/api/auth/user/", { data });
};

/** 更新系统管理-用户管理 */
export const updateUser = (data?: object, id?: number) => {
  return http.request<ResultTable>("put", `/api/auth/user/${id}/`, {
    data
  });
};

/** 删除系统管理-用户管理 */
export const deleteUser = (id?: number) => {
  return http.request<ResultTable>("delete", `/api/auth/user/${id}/`);
};

/** 修改密码 */
export const changePassword = (data?: object, id?: number) => {
  return http.request<Result>("put", `/api/auth/user/${id}/change_password/`, {
    data
  });
};

/** 系统管理-用户管理-获取所有角色列表 */
export const getAllRoleList = () => {
  return http.request<Result>("get", "/api/auth/role/role_list/");
};

/** 系统管理-用户管理-根据userId，获取对应角色id列表（userId：用户id） */
export const getRoleIds = (id?: number) => {
  return http.request<Result>("get", `/api/auth/user/${id}/role_list/`);
};
/** 系统管理-用户管理-更新用户角色 */
export const updateUserRole = (data?: object, id?: number) => {
  return http.request<Result>("put", `/api/auth/user/${id}/add_roles/`, {
    data
  });
};

/** 系统管理-用户管理- 批量删除用户 */
export const batchDeleteUser = (data?: object) => {
  return http.request<Result>("delete", "/api/auth/user/batch_delete/", {
    data
  });
};

/** 系统管理-用户管理- 上传头像 */
export const uploadAvatar = (data?: object, id?: number) => {
  return http.request<Result>("post", `/api/auth/user/${id}/upload_avatar/`, {
    data
  });
};
/** 获取系统管理-角色管理列表 */
export const getRoleList = (data?: object) => {
  return http.request<ResultTable>("get", "/api/auth/role/", { params: data });
};

/** 创建系统管理-角色管理列表 */
export const createRole = (data?: object) => {
  return http.request<ResultTable>("post", "/api/auth/role/", { data });
};

/** 创建系统管理-角色管理列表 */
export const updateRole = (data?: object, id?: string) => {
  return http.request<ResultTable>("put", `/api/auth/role/${id}/`, {
    data
  });
};

/** 删除系统管理-角色管理列表 */
export const deleteRole = (id?: string) => {
  return http.request<ResultTable>("delete", `/api/auth/role/${id}/`);
};

/** 获取系统管理-菜单管理列表 */
export const getMenuList = (data?: object) => {
  return http.request<Result>("get", "/api/auth/menu/", { params: data });
};

/** 创建系统管理-菜单管理 */
export const createMenu = (data?: object) => {
  return http.request<ResultTable>("post", "/api/auth/menu/", { data });
};

/** 更新系统管理-菜单管理 */
export const updateMenu = (data?: object, id?: number) => {
  return http.request<Result>("put", `/api/auth/menu/${id}/`, {
    data
  });
};

/** 删除系统管理-菜单管理 */
export const deleteMenu = (id?: number) => {
  return http.request<Result>("delete", `/api/auth/menu/${id}/`);
};

/** 获取系统管理-部门管理列表 */
export const getDeptList = (data?: object) => {
  return http.request<Result>("get", "/api/auth/dept/", { data });
};

/** 创建系统管理-部门管理 */
export const postDept = (data?: object) => {
  return http.request<Result>("post", "/api/auth/dept/", { data });
};

/** 更新系统管理-部门管理 */
export const putDept = (data?: object, id?: number) => {
  return http.request<Result>("put", `/api/auth/dept/${id}/`, {
    data
  });
};

/** 删除系统管理-部门管理 */
export const delDept = (id?: number) => {
  return http.request<Result>("delete", `/api/auth/dept/${id}/`);
};

/** 获取系统监控-在线用户列表 */
export const getOnlineLogsList = (data?: object) => {
  return http.request<ResultTable>("post", "/online-logs", { data });
};

/** 获取系统监控-登录日志列表 */
export const getLoginLogsList = (data?: object) => {
  return http.request<ResultTable>("get", "/api/auth/log/", {
    params: data
  });
};

/** 获取系统监控-操作日志列表 */
export const getOperationLogsList = (data?: object) => {
  return http.request<ResultTable>("get", "/api/auth/log/", { data });
};

/** 获取系统监控-系统日志列表 */
export const getSystemLogsList = (data?: object) => {
  return http.request<ResultTable>("get", "/api/auth/log/", { data });
};

/** 获取系统监控-系统日志-根据 id 查日志详情 */
export const getSystemLogsDetail = (data?: object) => {
  return http.request<Result>("post", "/system-logs-detail", { data });
};

/** 获取角色管理-权限-菜单权限 */
export const getRoleMenu = (data?: object) => {
  return http.request<Result>("get", "/api/auth/menu/menu_tree/", { data });
};

/** 获取角色管理-权限-菜单权限-根据角色 id 查对应菜单 */
export const getRoleMenuIds = (data?: object, id?: number) => {
  return http.request<Result>("get", `/api/auth/role/${id}/menu_list/`, {
    data
  });
};

/** 角色管理-权限-菜单权限-更新角色菜单权限 */
export const updateRoleMenu = (data?: object, id?: number) => {
  return http.request<Result>("put", `/api/auth/role/${id}/menu_update/`, {
    data
  });
};
