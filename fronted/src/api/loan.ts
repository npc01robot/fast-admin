import { http } from "@/utils/http";
import type { ResultTable, Result } from "@/api/common_type";

/**  */
export const getLoanList = (data?: object) => {
  return http.request<ResultTable>("get", "/api/yb/loan/", data);
};

export const getLoanDetail = (id: string) => {
  return http.request<Result>("get", `/api/yb/loan/${id}/`);
};

export const createLoan = (data: object) => {
  return http.request<Result>("post", "/api/yb/loan/", data);
};

export const updateLoan = (data: object, id: string) => {
  return http.request<Result>("put", `/api/yb/loan/${id}/`, data);
};

export const deleteLoan = (id: string) => {
  return http.request<Result>("delete", `/api/yb/loan/${id}/`);
};

export const getLoanRepayList = (data?: object) => {
  return http.request<ResultTable>("get", "/api/yb/repay/", data);
};

export const getLoanRepayDetail = (id: string) => {
  return http.request<Result>("get", `/api/yb/repay/${id}/`);
};

export const createLoanRepay = (data: object) => {
  return http.request<Result>("post", "/api/yb/repay/", data);
};

export const updateLoanRepay = (data: object, id: string) => {
  return http.request<Result>("put", `/api/yb/repay/${id}/`, data);
};

export const deleteLoanRepay = (id: string) => {
  return http.request<Result>("delete", `/api/yb/repay/${id}/`);
};

export const getLoanInterestList = (data?: object) => {
  return http.request<ResultTable>("get", "/api/yb/interest/", data);
};

export const getLoanInterestDetail = (id: string) => {
  return http.request<Result>("get", `/api/yb/interest/${id}/`);
};

export const createLoanInterest = (data: object) => {
  return http.request<Result>("post", "/api/yb/interest/", data);
};

export const updateLoanInterest = (data: object, id: string) => {
  return http.request<Result>("put", `/api/yb/interest/${id}/`, data);
};

export const deleteLoanInterest = (id: string) => {
  return http.request<Result>("delete", `/api/yb/interest/${id}/`);
};

export const exportLoan = (data?: object) => {
  return http.request<ResultTable>("get", "/api/yb/loan/export/", data);
};

export const exportLoanRepay = (data?: object) => {
  return http.request<ResultTable>("get", "/api/yb/repay/export/", data);
};

export const exportLoanInterest = (data?: object) => {
  return http.request<ResultTable>("get", "/api/yb/interest/export/", data);
};

export const getHomeLoanData = () => {
  return http.request<Result>("get", "/api/yb/loan/home_data/");
};

export const getOneYearLoanData = () => {
  return http.request<Result>("get", "/api/yb/loan/one_year_repay_amount/");
};

export const saveExternalLoan = (data: object) => {
  return http.request<Result>("post", "/api/yb/loan/save_external_loan/", data);
};

export const getExternalLoanList = (data?: object) => {
  return http.request<Result>("post", "/api/yb/loan/external_loan/", data);
};
