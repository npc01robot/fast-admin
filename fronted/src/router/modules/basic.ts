import { BasicTypeEnum } from "@/api/basic";
import { basic } from "@/router/enums";
// 基础信息页面
export default {
  path: "/basic",
  meta: {
    icon: "ep:menu",
    title: "基本信息管理",
    rank: basic
  },
  children: [
    {
      path: "/basic/guarantee",
      name: "basic-guarantee",
      component: () => import("@/views/basic/index.vue"),
      meta: {
        title: "担保单位",
        roles: ["admin"]
      },
      props: { title: "担保单位", type: BasicTypeEnum.GUARANTEE }
    },
    {
      path: "/basic/guarantee-type",
      name: "basic-guarantee-type",
      component: () => import("@/views/basic/index.vue"),
      meta: {
        title: "担保方式",
        roles: ["admin"]
      },
      props: { title: "担保方式", type: BasicTypeEnum.GUARANTEE_TYPE }
    },
    {
      path: "/basic/credict",
      name: "basic-credict",
      component: () => import("@/views/basic/index.vue"),
      meta: {
        title: "授信金融机构",
        roles: ["admin"]
      },
      props: { title: "授信金融机构", type: BasicTypeEnum.CREDIT }
    },
    {
      path: "/basic/loan",
      name: "basic-loan",
      component: () => import("@/views/basic/index.vue"),
      meta: {
        title: "贷款单位",
        roles: ["admin"]
      },
      props: { title: "贷款单位", type: BasicTypeEnum.LOAN_UNIT }
    },
    {
      path: "/basic/loan-type",
      name: "basic-loan-type",
      component: () => import("@/views/basic/index.vue"),
      meta: {
        title: "贷款类型",
        roles: ["admin"]
      },
      props: { title: "贷款类型", type: BasicTypeEnum.LOAN_TYPE }
    }
  ]
} satisfies RouteConfigsTable;
