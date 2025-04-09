interface FormItemProps {
  id: number;
  higherDeptOptions: Record<string, unknown>[];
  parent: number | null;
  name: string;
  sort: number;
  status: boolean;
  remark: string;
  type: number;
  creator: string;
}
interface FormProps {
  formInline: FormItemProps;
}

export type { FormItemProps, FormProps };
