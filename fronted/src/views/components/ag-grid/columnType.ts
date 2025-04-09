import accounting from "accounting";

export const columnType = {
  bool: {
    valueFormatter: params => {
      return params.value ? "是" : "否";
    },
    filter: "agSetColumnFilter",
    filterParams: {
      valueFormatter: params => {
        return params.value.label;
      },
      keyCreator: params => params.value.value,
      closeOnApply: true,
      excelMode: "windows",
      buttons: ["apply", "reset"],
      values: [
        { label: "否", value: false },
        { label: "是", value: true }
      ]
    }
  },
  number: {
    valueFormatter: params => {
      const value = params.value || 0;
      return accounting.formatMoney(value, "¥", 2);
    }
  },
  percent: {
    valueFormatter: params => {
      const value = params.value || 0;
      return accounting.formatNumber(value, 2) + "%";
    }
  }
};
