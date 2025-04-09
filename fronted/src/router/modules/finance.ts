// 融资情况

import { finance } from "@/router/enums";

export default {
  path: "/finance",
  meta: {
    icon: "ri:funds-fill",
    title: "融资情况",
    rank: finance
  },
  children: [
    {
      path: "/finance",
      name: "Finance",
      component: () => import("@/views/finance/index.vue"),
      meta: {
        title: "融资情况",
        roles: ["admin", "common"]
      }
    },
    {
      path: "/finance/detail",
      name: "FinanceDetail",
      component: () => import("@/views/finance/detail.vue"),
      meta: {
        title: "融资详情",
        roles: ["admin", "common"],
        showLink: false
      }
    }
  ]
} satisfies RouteConfigsTable;
