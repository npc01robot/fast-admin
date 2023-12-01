export default {
  path: "/assure",
  redirect: "/assure/index",
  rank: 9,
  meta: {
    icon: "informationLine",
    title: "对外担保"
    // showLink: false,
  },
  children: [
    {
      path: "/assure/index",
      name: "assure",
      component: () => import("@/views/assure/index.vue"),
      meta: {
        title: "对外担保"
      }
    }
  ]
} as RouteConfigsTable;
