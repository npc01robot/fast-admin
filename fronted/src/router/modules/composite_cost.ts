// 综合成本管理

import { composite_cost } from "@/router/enums";

export default {
  path: "/comprehensive-cost",
  meta: {
    icon: "ri:paypal-fill",
    title: "综合成本",
    rank: composite_cost
  },
  children: [
    {
      path: "/comprehensive-cost",
      name: "综合成本",
      component: () => import("@/views/composite_cost/index.vue"),
      meta: {
        title: "综合成本",
        roles: ["admin", "common"]
      }
    }
  ]
} satisfies RouteConfigsTable;
