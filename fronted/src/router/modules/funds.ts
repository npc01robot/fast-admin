export default {
  path: "/funds",
  redirect: "/funds/index",
  rank: 9,
  meta: {
    icon: "informationLine",
    title: "融资情况"
    // showLink: false,
  },
  children: [
    {
      path: "/funds/index",
      name: "funds",
      component: () => import("@/views/funds/index.vue"),
      meta: {
        title: "融资情况"
      }
    }
  ]
} as RouteConfigsTable;
