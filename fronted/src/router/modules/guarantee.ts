import { guarantee } from "@/router/enums";

export default {
  path: "/guarantee",
  meta: {
    icon: "ri:shield-fill",
    title: "对外担保",
    rank: guarantee
  },
  children: [
    {
      path: "/guarantee/guarantee",
      name: "GuaranteeInfo",
      component: () => import("@/views/guarantee/index.vue"),
      meta: {
        title: "对外担保",
        roles: ["admin", "common"]
      }
    },
    {
      path: "/guarantee/detail",
      name: "GuaranteeDetail",
      component: () => import("@/views/guarantee/form.vue"),
      meta: {
        title: "对外担保详情",
        roles: ["admin", "common"],
        showLink: false,
        activePath: "/guarantee"
      }
    },
    {
      path: "/guarantee/beGuaranteed",
      name: "BeGuaranteed",
      component: () => import("@/views/be_guaranteed/index.vue"),
      meta: {
        title: "被担保明细",
        roles: ["admin", "common"]
      }
    },
    {
      path: "/guarantee/beGuaranteed/detail",
      name: "BeGuaranteeDetail",
      component: () => import("@/views/be_guaranteed/form.vue"),
      meta: {
        title: "对外担保详情",
        roles: ["admin", "common"],
        showLink: false,
        hiddenTag: true,
        activePath: "/guarantee"
      }
    }
  ]
} satisfies RouteConfigsTable;
