import { aggrid } from "@/router/enums";

export default {
  path: "/grid",
  meta: {
    icon: "ri:file-info-line",
    title: "AGGrid",
    rank: aggrid
  },
  children: [
    {
      path: "/grid/demo1",
      name: "AGGrid",
      component: () => import("@/views/aggrid/index.vue"),
      meta: {
        title: "AGGrid",
        showParent: true
      }
    }
  ]
} satisfies RouteConfigsTable;
