// 完整版菜单比较多，将 rank 抽离出来，在此方便维护

const home = 0, // 平台规定只有 home 路由的 rank 才能为 0 ，所以后端在返回 rank 的时候需要从非 0 开始
  system = 1,
  monitor = 2,
  basic = 3,
  approve = 4,
  finance = 5,
  guarantee = 6,
  repay_interest = 7,
  composite_cost = 8,
  aggrid = 99,
  components = 99,
  error = 99;

export {
  home,
  basic,
  components,
  error,
  system,
  monitor,
  guarantee,
  aggrid,
  finance,
  repay_interest,
  composite_cost,
  approve
};
