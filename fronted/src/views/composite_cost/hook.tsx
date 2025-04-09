import { onMounted, onUnmounted, reactive, ref } from "vue";
import type { GridOptions } from "ag-grid-community";
import EventEmitter from "eventemitter3";
import type { ToolButton } from "@/views/components/ag-grid/server-type";
import { getExternalLoanList, getLoanList, saveExternalLoan } from "@/api/loan";
import { columnType } from "@/views/components/ag-grid/columnType";
import { BasicTypeEnum, getBasicList } from "@/api/basic";
import { handleColumTree } from "@/utils/tree";
import type { TinyGridOptions } from "@/views/components/ag-grid/tiny-type";
import dayjs from "dayjs";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import CheckedIcon from "@iconify-icons/ep/checked";
import { message } from "@/utils/message";

export function useCompositeCostHook() {
  const componentRef = ref<ServerSideGridElement<any>>();
  type _GridType = typeof componentRef.value;
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  let api: NonNullable<_GridType>;

  const emit = new EventEmitter<"modelUpdated">();
  const changed_date = ref(new Date());
  onMounted(() => {
    api = componentRef.value!;
  });
  onUnmounted(() => {
    emit.removeAllListeners();
  });
  const vm = reactive({
    loading: false
  });
  const cacheOrgnizationTree = ref<any>({});
  const cacheLoanUnitTree = ref<any>({});
  const cacheLoanTypeTree = ref<any>({});
  const gridOptions: GridOptions<any> = {
    defaultColDef: {
      suppressHeaderMenuButton: true
    },
    columnTypes: {
      ...columnType,
      loan_unit: {
        valueFormatter: params => {
          return params.value;
        },
        filter: "agSetColumnFilter",
        filterParams: {
          treeList: true,
          values: params => {
            getBasicList({ params: { type: BasicTypeEnum.LOAN_UNIT } }).then(
              res => {
                cacheLoanUnitTree.value = handleColumTree(res.data);
                params.success(res.data);
              }
            );
          },
          treeListPathGetter: data => {
            const path = cacheLoanUnitTree.value[data.id];
            if (path) {
              return path.map(item => item.name);
            }
            return [data.name];
          },
          valueFormatter: params => params.value.name,
          keyCreator: params => params.value.name,
          closeOnApply: true,
          excelMode: "windows",
          buttons: ["apply", "reset"]
        }
      },
      loan_type: {
        valueFormatter: params => {
          return params.value;
        },
        filter: "agSetColumnFilter",
        filterParams: {
          treeList: true,
          values: params => {
            getBasicList({ params: { type: BasicTypeEnum.LOAN_TYPE } }).then(
              res => {
                cacheLoanTypeTree.value = handleColumTree(res.data);
                params.success(res.data);
              }
            );
          },
          treeListPathGetter: data => {
            const path = cacheLoanTypeTree.value[data.id];
            if (path) {
              return path.map(item => item.name);
            }
            return [data.name];
          },
          valueFormatter: params => params.value.name,
          keyCreator: params => params.value.name,
          closeOnApply: true,
          excelMode: "windows",
          buttons: ["apply", "reset"]
        }
      },
      bank: {
        valueFormatter: params => {
          return params.value;
        },
        filter: "agSetColumnFilter",
        filterParams: {
          treeList: true,
          values: params => {
            getBasicList({ params: { type: BasicTypeEnum.CREDIT } }).then(
              res => {
                cacheOrgnizationTree.value = handleColumTree(res.data);
                params.success(res.data);
              }
            );
          },
          treeListPathGetter: data => {
            const path = cacheOrgnizationTree.value[data.id];
            if (path) {
              return path.map(item => item.name);
            }
            return [data.name];
          },
          valueFormatter: params => params.value.name,
          keyCreator: params => params.value.name,
          closeOnApply: true,
          excelMode: "windows",
          buttons: ["apply", "reset"]
        }
      }
    },
    onCellValueChanged: event => {
      setUserDate(event);
    },
    columnDefs: [
      { field: "id" },
      {
        field: "loan_unit",
        headerName: "贷款单位名称",
        type: "loan_unit"
      },
      {
        field: "credit_name",
        headerName: "授信金融机构名称",
        type: "bank"
      },
      {
        field: "type",
        headerName: "贷款类型",
        type: "loan_type"
      },
      {
        field: "loan_balance",
        headerName: "贷款余额",
        type: "number"
      },
      {
        headerName: "借款借据",
        children: [
          {
            field: "contract_rate",
            headerName: "合同利率",
            type: "percent"
          },
          {
            field: "overall_rate",
            headerName: "综合利率",
            type: "percent"
          },
          {
            field: "loan_date",
            headerName: "贷款借款日",
            type: "date"
          },
          {
            field: "due_date",
            headerName: "贷款到期日",
            type: "date"
          }
        ]
      },
      {
        headerName: "实际还款",
        children: [
          {
            field: "last_repay_date",
            headerName: "归还贷款本金日期"
          },
          {
            field: "repay_amount",
            headerName: "归还贷款本金金额",
            type: "number"
          }
        ]
      },
      {
        children: [
          {
            field: "loan_amount",
            headerName: "本金",
            type: "number"
          },
          {
            field: "interest_start_date",
            headerName: "起始日",
            editable: true, // 让该列可以编辑
            valueGetter: params => {
              return params.data.interest_start_date
                ? dayjs(params.data.interest_start_date).format("YYYY-MM-DD")
                : dayjs(params.data.loan_date).format("YYYY-MM-DD");
            },
            valueFormatter: params => {
              return params.value
                ? dayjs(params.value).format("YYYY-MM-DD")
                : "";
            },
            cellEditor: "agDateCellEditor", // 使用日期选择器作为单元格编辑器
            cellEditorParams: {
              format: "YYYY-MM-DD" // 设置日期的格式
            }
          },
          {
            headerName: "结束日",
            field: "interest_end_date", // 这是用户输入的列
            editable: true, // 让该列可以编辑
            valueFormatter: params => {
              return params.value
                ? dayjs(params.value).format("YYYY-MM-DD")
                : "";
            },
            cellEditor: "agDateCellEditor", // 使用日期选择器作为单元格编辑器
            cellEditorParams: {
              format: "YYYY-MM-DD" // 设置日期的格式
            }
          },
          {
            field: "days",
            headerName: "天数"
          },
          {
            field: "principal_rights",
            headerName: "本金权数"
          }
        ],
        headerName: "付息统计测算"
      },
      {
        field: "interest_cost",
        headerName: "实际付息",
        type: "number",
        editable: true
      },
      {
        field: "contract_rate_overall_cost",
        headerName: "合同利率综合成本",
        type: "percent"
      },
      {
        field: "contract_pay_interest",
        headerName: "综合付息",
        type: "number"
      },
      {
        field: "actual_rate_overall_cost",
        headerName: "实际利率综合成本",
        type: "percent"
      }
    ],
    pinnedBottomRowData: [
      {
        id: 0
      }
    ]
  };

  const buttons: Array<ToolButton | string> = [
    {
      name: "save",
      icon: useRenderIcon(CheckedIcon),
      label: "保存所有",
      action: () => {
        saveAll();
      }
    }
  ];
  const saveAll = () => {
    const rowData = [];
    options.api.forEachNode(node => {
      const data = node.data;
      if (data.interest_end_date) {
        const interest_start_date = data.interest_start_date
          ? dayjs(data.interest_start_date).format("YYYY-MM-DD")
          : dayjs(data.loan_date).format("YYYY-MM-DD");
        rowData.push({
          loan_id: data.id,
          start_date: interest_start_date,
          end_date: dayjs(data.interest_end_date).format("YYYY-MM-DD"),
          actual_cost: data.interest_cost
        });
      }
    });
    if (rowData.length === 0) {
      message("保存失败，请填写起始日期和结束日期！", { type: "error" });
    } else {
      console.log(rowData);
      // 调用接口保存数据
      saveExternalLoan({ data: rowData }).then(res => {
        if (res.code === 0) {
          message("保存成功！", { type: "success" });
        } else {
          message("保存失败！", { type: "error" });
        }
      });
    }
  };
  // 定义异步函数 loadData
  async function loadData(params) {
    // 默认页码和每页大小
    params = {
      ...params,
      page: 1,
      page_size: 99999
    };

    /*
     调用 getLoanList 获取数据
    */
    return getLoanList({ params: params }).then(res => {
      const rowData = res.data.list;
      vm.loading = false;
      return rowData; // 返回数据
    });
  }

  const options: TinyGridOptions<any> = {
    gridName: "综合成本",
    gridOptions: gridOptions,
    buttons: buttons,
    loadData: () => loadData({})
  };

  const setUserDate = (event: any) => {
    // 如果是结束日列发生变化，更新整列数据
    if (
      event.colDef.field === "interest_start_date" ||
      event.colDef.field === "interest_end_date"
    ) {
      options.api.forEachNode(node => {
        if (event.colDef.field === "interest_start_date") {
          node.setDataValue(
            "interest_start_date",
            event.data.interest_start_date
          );
        }
        node.setDataValue("interest_end_date", event.data.interest_end_date);
        const days = dayjs(node.data.interest_end_date).diff(
          node.data.interest_start_date
            ? dayjs(node.data.interest_start_date)
            : dayjs(node.data.loan_date),
          "days"
        );
        node.setDataValue("days", days);
        const principal_rights = (node.data.loan_amount / 360) * days;
        node.setDataValue("principal_rights", principal_rights.toFixed(2));
        const contract_pay_interest = principal_rights * node.data.overall_rate;
        node.setDataValue(
          "contract_pay_interest",
          contract_pay_interest.toFixed(2)
        );
        const actual_rate_overall_cost = contract_pay_interest
          ? contract_pay_interest / principal_rights
          : 0;
        node.setDataValue(
          "actual_rate_overall_cost",
          actual_rate_overall_cost.toFixed(2)
        );
      });
      updatePinnedBottomRow();
    }

    if (
      event.data.interest_end_date &&
      changed_date.value !== event.data.interest_end_date
    ) {
      changed_date.value = event.data.interest_end_date;
      // 如果起始日和结束日都有值
      const rowData = [];
      options.api.forEachNode(node => {
        rowData.push({
          loan_id: node.data.id,
          start_date: node.data.interest_start_date
            ? dayjs(node.data.interest_start_date).format("YYYY-MM-DD")
            : dayjs(node.data.loan_date).format("YYYY-MM-DD"),
          end_date: dayjs(node.data.interest_end_date).format("YYYY-MM-DD")
        });
      });
      getExternalLoanList({ data: rowData }).then(res => {
        if (res.code === 0) {
          const data = res.data;
          options.api.forEachNode(node => {
            const item = data.find(item => item.loan_id === node.data.id);
            if (item) {
              node.setDataValue("interest_cost", item.actual_cost);
            } else {
              node.setDataValue("interest_cost", 0);
            }
          });
        }
      });
    }

    if (
      event.colDef.field === "interest_cost" ||
      changed_date.value === event.data.interest_end_date
    ) {
      options.api.forEachNode(node => {
        const contract_rate_overall_cost = node.data.principal_rights
          ? node.data.interest_cost / node.data.principal_rights
          : 0;
        node.setDataValue(
          "contract_rate_overall_cost",
          contract_rate_overall_cost.toFixed(2)
        );
      });
      updatePinnedBottomRow();
    }
  };
  function updatePinnedBottomRow() {
    const totalValues = {};
    const field = [
      "days",
      "loan_amount",
      "loan_balance",
      "repay_amount",
      "principal_rights",
      "interest_cost",
      "contract_pay_interest",
    ];
    options.api.forEachNode(node => {
      const data = node.data;
      Object.keys(data).forEach(key => {
        if (totalValues[key] && field.includes(key)) {
          totalValues[key] += Number(data[key]);
        } else {
          totalValues[key] = Number(data[key]);
        }
      });
    });
    // 创建底部固定行
    const pinnedRow = {}; // 你可以在这里设置一个静态的标题（如“总计”）
    Object.keys(totalValues).forEach(key => {
      pinnedRow[key] = totalValues[key].toFixed(2); // 将聚合结果赋值到固定行数据中
    });
    pinnedRow["contract_rate_overall_cost"] =
      Number(pinnedRow["interest_cost"]) / Number(pinnedRow["principal_rights"]);
    pinnedRow["actual_rate_overall_cost"] =
      Number(pinnedRow["contract_pay_interest"]) / Number(pinnedRow["principal_rights"]);
    // 更新底部固定行数据
    options.api.setGridOption("pinnedBottomRowData", [pinnedRow]);
  }
  return {
    componentRef,
    options
  };
}
