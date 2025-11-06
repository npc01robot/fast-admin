interface GuaranteeType {
  title: string;
  id: number;
  name: string;
  to_name: string;
  relation: string;
  matter: string;
  amount: number;
  actual_amount: number;
  cost: number;
  start_date: string;
  end_date: string;
  remark: string;
  is_deleted: boolean;
}
export type { GuaranteeType };
