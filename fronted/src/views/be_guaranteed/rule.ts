import { reactive } from "vue";
import type { FormRules } from "element-plus";

/** 自定义表单规则校验 */
export const formRules = reactive(<FormRules>{
  name: [{ required: true, message: "担保单位名称为必填项", trigger: "blur" }],
  to_name: [
    { required: true, message: "被担保单位名称为必填项", trigger: "blur" }
  ],
  amount: [{ required: true, message: "担保金额为必填项", trigger: "blur" }],
  start_time: [
    { required: true, message: "起始时间为必填项", trigger: "blur" }
  ],
  end_time: [{ required: true, message: "结束时间为必填项", trigger: "blur" }]
});
