import LineChartFill from "@iconify-icons/ri/line-chart-fill";
import DonutChartFill from "@iconify-icons/ri/donut-chart-fill";
import Finance from "@iconify-icons/ri/funds-fill";
import { getHomeLoanData } from "@/api/loan";
import { computed, ref } from "vue";

const loan_total_amount = ref<any>({
  total_amount: 0,
  latest_amount_list: [],
  bond_issue: 0,
  bank_loan: 0,
  one_year_mid_term: 0,
  long_term_loan: 0,
  non_standard: 0,
  credit_loan: 0,
  project_loan: 0,
  low_risk_loan: 0,
  other: 0,
  percent: 0
});
const one_year_amount = ref<any>({
  total_balance: 0,
  latest_amount_list: [],
  bank_loan: 0,
  non_standard: 0,
  other: 0,
  percent: 0
});

const long_term_amount = ref<any>({
  total_balance: 0,
  latest_amount_list: [],
  mid_term: 0,
  project_loan: 0,
  bond_issue: 0,
  non_standard: 0,
  other: 0,
  percent: 0
});
const one_year_repayment_amount = ref<any>({
  total_balance: 0,
  latest_amount_list: [],
  percent: 0
});

const interest_repay_data = ref<any>({
  interest_data: [],
  repay_data: [],
  date: []
});
const chartData = computed(() => {
  return [
    {
      icon: Finance,
      bgColor: "#effaff",
      color: "#41b6ff",
      duration: 2200,
      name: "融资总额",
      value: loan_total_amount.value.total_amount,
      percent: "+" + String(loan_total_amount.value.percent) + "%",
      data: [...loan_total_amount.value.latest_amount_list], // 平滑折线图数据
      line: true,
      dataKey: loan_total_amount.value
    },
    {
      icon: LineChartFill,
      bgColor: "#fff5f4",
      color: "#e85f33",
      duration: 1600,
      name: "一年期融资余额",
      value: one_year_amount.value.total_balance,
      percent: "+" + String(one_year_amount.value.percent) + "%",
      data: one_year_amount.value.latest_amount_list,
      dataKey: one_year_amount.value
    },
    {
      icon: LineChartFill,
      bgColor: "#eff8f4",
      color: "#26ce83",
      duration: 1500,
      name: "中长期融资余额",
      value: long_term_amount.value.total_balance,
      percent: "+" + String(long_term_amount.value.percent) + "%",
      data: [...long_term_amount.value.latest_amount_list],
      dataKey: long_term_amount.value
    },
    {
      icon: DonutChartFill,
      bgColor: "#f6f4fe",
      color: "#7846e5",
      duration: 100,
      name: "一年内到期融资金额",
      value: one_year_repayment_amount.value.total_balance,
      percent: "+" + String(one_year_repayment_amount.value.percent) + "%",
      data: [...one_year_repayment_amount.value.latest_amount_list],
      dataKey: one_year_repayment_amount.value
    }
  ];
});

/** 饼图数据 */
const pieData = computed(() => {
  return [
    {
      title: "融资总额占比",
      subtext: "1",
      data: [
        { name: "一年期", value: one_year_amount.value.total_balance },
        { name: "中长期", value: long_term_amount.value.total_balance }
      ],
      amount: loan_total_amount.value.total_amount,
      dataKey: loan_total_amount.value
    },
    {
      title: "一年期融资余额占比",
      subtext: "2",
      data: [
        { name: "银行贷款", value: one_year_amount.value.bank_loan },
        { name: "非标业务", value: one_year_amount.value.non_standard },
        { name: "其他", value: one_year_amount.value.other }
      ],
      amount: one_year_amount.value.total_balance,
      dataKey: one_year_amount.value
    },
    {
      title: "中长期融资余额占比",
      subtext: "2",
      data: [
        { name: "中期流贷", value: long_term_amount.value.mid_term },
        { name: "项目贷款", value: long_term_amount.value.project_loan },
        { name: "发行债券", value: long_term_amount.value.bond_issue },
        { name: "非标业务", value: long_term_amount.value.non_standard },
        { name: "其他", value: long_term_amount.value.other }
      ],
      amount: long_term_amount.value.total_balance,
      dataKey: long_term_amount.value
    },
    {
      title: "融资总额占比",
      subtext: "1",
      data: [
        { name: "发行债券", value: loan_total_amount.value.bond_issue },
        { name: "银行贷款", value: loan_total_amount.value.bank_loan },
        {
          name: "一年期流贷",
          value: loan_total_amount.value.one_year_mid_term
        },
        { name: "中长期贷款", value: loan_total_amount.value.long_term_loan },
        { name: "非标业务", value: loan_total_amount.value.non_standard },
        { name: "项目贷款", value: loan_total_amount.value.project_loan },
        { name: "其他", value: loan_total_amount.value.other }
      ],
      amount: loan_total_amount.value.total_amount,
      dataKey: loan_total_amount.value
    }
  ];
});

const barChartData = computed(() => {
  return {
    date: [...interest_repay_data.value.date],
    repay: [...interest_repay_data.value.repay_data],
    interest: [...interest_repay_data.value.interest_data]
  };
});

const getLoanData = () => {
  getHomeLoanData().then(res => {
    const data = res.data;
    loan_total_amount.value = data.loan_total_amount;
    one_year_amount.value = data.one_year_loan_amount;
    long_term_amount.value = data.long_term_loan_amount;
    one_year_repayment_amount.value = data.one_year_repayment_amount;
    interest_repay_data.value = data.interest_repay_data;
  });
};
getLoanData();

export { chartData, pieData, barChartData };
