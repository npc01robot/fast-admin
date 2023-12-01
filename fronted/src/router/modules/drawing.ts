export default {
  path: "/drawing",
  redirect: "/drawing/index",
  rank: 9,
  meta: {
    icon: "informationLine",
    title: "实际贷款情况",
    showLink: false
  },
  children: [
    {
      path: "/drawing/index",
      name: "drawing",
      component: () => import("@/views/drawing/index.vue"),
      meta: {
        title: "实际贷款情况"
      }
    }
  ]
} as RouteConfigsTable;
