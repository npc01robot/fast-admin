// 审批管理

import { approve } from "@/router/enums";

export default {
  path: "/approve",
  meta: {
    icon: "ri:account-box-fill",
    title: "授信审批",
    rank: approve
  },
  children: [
    {
      path: "/approve",
      name: "Credit",
      component: () => import("@/views/approve/index.vue"),
      meta: {
        title: "授信审批",
        roles: ["admin", "common"]
      }
    },
    {
      path: "/approve/detail",
      name: "CreditDetail",
      component: () => import("@/views/approve/form.vue"),
      meta: {
        title: "授信审批详情",
        roles: ["admin", "common"],
        showLink: false,
        activePath: "/approve"
      }
    }
  ]
} satisfies RouteConfigsTable;
