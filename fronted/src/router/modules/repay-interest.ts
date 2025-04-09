// 还本付息

import { repay_interest } from "@/router/enums";

export default {
  path: "/repay-interest",
  meta: {
    icon: "ri:money-cny-box-fill",
    title: "还本付息",
    rank: repay_interest
  },
  children: [
    {
      path: "/repay-interest/repay",
      name: "Repay",
      component: () => import("@/views/repay/index.vue"),
      meta: {
        title: "还本列表",
        roles: ["admin", "common"]
      }
    },
    {
      path: "/repay-interest/repay/detail",
      name: "RepayDetail",
      component: () => import("@/views/repay/form.vue"),
      meta: {
        title: "还本详情",
        roles: ["admin", "common"],
        showLink: false,
        activePath: "/repay-interest/repay"
      }
    },
    {
      path: "/repay-interest/interest",
      name: "Interest",
      component: () => import("@/views/interest/index.vue"),
      meta: {
        title: "付息列表",
        roles: ["admin", "common"]
      }
    },
    {
      path: "/repay-interest/interest/detail",
      name: "InterestDetail",
      component: () => import("@/views/interest/form.vue"),
      meta: {
        title: "付息详情",
        roles: ["admin", "common"],
        showLink: false,
        activePath: "/repay-interest/interest"
      }
    }
  ]
} satisfies RouteConfigsTable;
