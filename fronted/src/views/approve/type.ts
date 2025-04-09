interface CreditType {
  title: string;
  id: number;
  code: string;
  name: string;
  organization: string;
  amount: number;
  surplus_amount: number;
  group_chairman: string;
  group_deputy_chairman: boolean;
  sub_chairman: string;
  sub_deputy_chairman: boolean;
  start_date: string;
  end_date: string;
  remark: string;
  create_time: string;
  update_time: string;
  three_deputy_chairman_date: string;
  three_chairman_date: string;
  two_deputy_chairman_date: string;
  two_chairman_date: string;
  group_deputy_chairman_date: string;
  group_chairman_date: string;
  three_chairman_decision_file: string;
  two_chairman_decision_file: string;
  group_chairman_decision_file: string;
}
export default CreditType;
