import { delay } from "@pureadmin/utils";
import { ref, onMounted, reactive } from "vue";
import type { PaginationProps } from "@pureadmin/table";
import Empty from "./empty.svg?component";
import { getOneYearLoanData } from "@/api/loan";

export function useColumns() {
  const dataList = ref([]);
  const loading = ref(true);
  const columns: TableColumnList = [
    {
      sortable: true,
      label: "序号",
      prop: "id"
    },
    {
      sortable: true,
      label: "贷款单位",
      prop: "loan_unit"
    },
    {
      sortable: true,
      label: "贷款名称",
      prop: "name"
    },
    {
      sortable: true,
      label: "贷款类型",
      prop: "type"
    },
    {
      sortable: true,
      label: "贷款金额",
      prop: "loan_amount"
    },
    {
      sortable: true,
      label: "借款日期",
      minWidth: 100,
      prop: "loan_date"
    },
    {
      sortable: true,
      label: "到期日期",
      prop: "due_date"
    }
  ];

  /** 分页配置 */
  const pagination = reactive<PaginationProps>({
    pageSize: 10,
    currentPage: 1,
    layout: "prev, pager, next",
    total: 0,
    align: "center"
  });

  function onCurrentChange(page: number) {
    console.log("onCurrentChange", page);
    loading.value = true;
    delay(300).then(() => {
      loading.value = false;
    });
  }

  onMounted(() => {
    getOneYearLoanData().then(res => {
      dataList.value = res.data;
      pagination.total = res.data.length;
      loading.value = false;
    });
  });

  return {
    Empty,
    loading,
    columns,
    dataList,
    pagination,
    onCurrentChange
  };
}
