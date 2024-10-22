interface FormItemProps {
  id: number;
  higherDeptOptions: Record<string, unknown>[];
  parent: number | null;
  name: string;
  principal: string;
  phone: string | number;
  email: string;
  sort: number;
  status: boolean;
  remark: string;
}
interface FormProps {
  formInline: FormItemProps;
}

export type { FormItemProps, FormProps };
