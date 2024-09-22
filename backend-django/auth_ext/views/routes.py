# 路由生成
# todo: 路由生成功能待完善
from auth_ext.models.menu import Menu
from auth_ext.models.user import AuthExtUser
from rest_framework import generics
from rest_framework.response import Response


class AsyncRoute(generics.ListAPIView):
    """
    动态生成路由,大型项目使用
    """

    def get(self, request, *args, **kwargs):
        menu_list = []
        role_list = []
        user = AuthExtUser.objects.filter(pk=request.auth.payload["user_code"]).first()
        if not user:
            raise ValueError("User not found")
        roles = user.roles.filter(status=1, is_deleted=False).all()
        if "admin" in roles.values_list("code", flat=True):
            menu_list = Menu.objects.filter(
                is_deleted=False, parent__isnull=False
            ).all()
            role_list = ["admin"]
        else:
            for role in roles:
                menu_list.extend(
                    role.menu.filter(is_deleted=False, parent__isnull=True).all()
                )  # 顶级菜单
                role_list.append(role.code)

        def build_menu_tree(menu, roles):
            res = {
                "path": menu.path,
                "name": menu.name,
                "meta": {
                    "icon": menu.icon,
                    "title": menu.title,
                    "roles": roles,
                },
            }
            # 过滤尚未删除的子菜单
            children_menu = menu.children.filter(is_deleted=False)
            if children_menu:
                res["children"] = [
                    build_menu_tree(child, roles) for child in children_menu
                ]
            return res

        try:
            menu_list = list(set(menu_list))  # 去重
            data = [
                {
                    "path": menu.path,
                    "meta": {
                        "icon": menu.icon,
                        "title": menu.title,
                        "rank": menu.rank,
                    },
                    "children": [
                        build_menu_tree(child, role_list)
                        for child in menu.children.filter(is_deleted=False).all()
                    ],
                }
                for menu in menu_list
            ]
        except Exception as e:
            # 记录错误日志
            print(f"Error occurred: {e}")
            data = []
        if "admin" in role_list:
            data.extend(
                [
                    {
                        "path": "/system",
                        "meta": {
                            "icon": "ri:settings-3-line",
                            "title": "menus.pureSysManagement",
                            "rank": 90,
                        },
                        "children": [
                            {
                                "path": "/system/user/index",
                                "name": "SystemUser",
                                "meta": {
                                    "icon": "ri:admin-line",
                                    "title": "menus.pureUser",
                                    "roles": ["admin"],
                                },
                            },
                            {
                                "path": "/system/role/index",
                                "name": "SystemRole",
                                "meta": {
                                    "icon": "ri:admin-fill",
                                    "title": "menus.pureRole",
                                    "roles": ["admin"],
                                },
                            },
                            {
                                "path": "/system/menu/index",
                                "name": "SystemMenu",
                                "meta": {
                                    "icon": "ep:menu",
                                    "title": "menus.pureSystemMenu",
                                    "roles": ["admin"],
                                },
                            },
                            {
                                "path": "/system/dept/index",
                                "name": "SystemDept",
                                "meta": {
                                    "icon": "ri:git-branch-line",
                                    "title": "menus.pureDept",
                                    "roles": ["admin"],
                                },
                            },
                        ],
                    },
                    {
                        "path": "/monitor",
                        "meta": {
                            "icon": "ep:monitor",
                            "title": "menus.pureSysMonitor",
                            "rank": 91,
                        },
                        "children": [
                            {
                                "path": "/monitor/online-user",
                                "component": "monitor/online/index",
                                "name": "OnlineUser",
                                "meta": {
                                    "icon": "ri:user-voice-line",
                                    "title": "menus.pureOnlineUser",
                                    "roles": ["admin"],
                                },
                            },
                            {
                                "path": "/monitor/login-logs",
                                "component": "monitor/logs/login/index",
                                "name": "LoginLog",
                                "meta": {
                                    "icon": "ri:window-line",
                                    "title": "menus.pureLoginLog",
                                    "roles": ["admin"],
                                },
                            },
                            {
                                "path": "/monitor/operation-logs",
                                "component": "monitor/logs/operation/index",
                                "name": "OperationLog",
                                "meta": {
                                    "icon": "ri:history-fill",
                                    "title": "menus.pureOperationLog",
                                    "roles": ["admin"],
                                },
                            },
                            {
                                "path": "/monitor/system-logs",
                                "component": "monitor/logs/system/index",
                                "name": "SystemLog",
                                "meta": {
                                    "icon": "ri:file-search-line",
                                    "title": "menus.pureSystemLog",
                                    "roles": ["admin"],
                                },
                            },
                        ],
                    },
                ]
            )
        return Response(data)

        # data = [
        #     {
        #         "path": "/system",
        #         "meta": {
        #             "icon": "ri:settings-3-line",
        #             "title": "menus.pureSysManagement",
        #             "rank": 20,
        #         },
        #         "children": [
        #             {
        #                 "path": "/system/user/index",
        #                 "name": "SystemUser",
        #                 "meta": {
        #                     "icon": "ri:admin-line",
        #                     "title": "menus.pureUser",
        #                     "roles": ["admin"],
        #                 },
        #             },
        #             {
        #                 "path": "/system/role/index",
        #                 "name": "SystemRole",
        #                 "meta": {
        #                     "icon": "ri:admin-fill",
        #                     "title": "menus.pureRole",
        #                     "roles": ["admin"],
        #                 },
        #             },
        #             {
        #                 "path": "/system/menu/index",
        #                 "name": "SystemMenu",
        #                 "meta": {
        #                     "icon": "ep:menu",
        #                     "title": "menus.pureSystemMenu",
        #                     "roles": ["admin"],
        #                 },
        #             },
        #             {
        #                 "path": "/system/dept/index",
        #                 "name": "SystemDept",
        #                 "meta": {
        #                     "icon": "ri:git-branch-line",
        #                     "title": "menus.pureDept",
        #                     "roles": ["admin"],
        #                 },
        #             },
        #         ],
        #     },
        # {
        #     "path": "/monitor",
        #     "meta": {
        #         "icon": "ep:monitor",
        #         "title": "menus.pureSysMonitor",
        #         "rank": 21
        #     },
        #     "children": [
        #         {
        #             "path": "/monitor/online-user",
        #             "component": "monitor/online/index",
        #             "name": "OnlineUser",
        #             "meta": {
        #                 "icon": "ri:user-voice-line",
        #                 "title": "menus.pureOnlineUser",
        #                 "roles": ["admin"]
        #             }
        #         },
        #         {
        #             "path": "/monitor/login-logs",
        #             "component": "monitor/logs/login/index",
        #             "name": "LoginLog",
        #             "meta": {
        #                 "icon": "ri:window-line",
        #                 "title": "menus.pureLoginLog",
        #                 "roles": ["admin"]
        #             }
        #         },
        #         {
        #             "path": "/monitor/operation-logs",
        #             "component": "monitor/logs/operation/index",
        #             "name": "OperationLog",
        #             "meta": {
        #                 "icon": "ri:history-fill",
        #                 "title": "menus.pureOperationLog",
        #                 "roles": ["admin"]
        #             }
        #         },
        #         {
        #             "path": "/monitor/system-logs",
        #             "component": "monitor/logs/system/index",
        #             "name": "SystemLog",
        #             "meta": {
        #                 "icon": "ri:file-search-line",
        #                 "title": "menus.pureSystemLog",
        #                 "roles": ["admin"]
        #             }
        #         }
        #     ]
        # },
        # {
        #     "path": "/permission",
        #     "meta": {
        #         "title": "menus.purePermission",
        #         "icon": "ep:lollipop",
        #         "rank": 22
        #     },
        #     "children": [
        #         {
        #             "path": "/permission/page/index",
        #             "name": "PermissionPage",
        #             "meta": {
        #                 "title": "menus.purePermissionPage",
        #                 "roles": ["admin", "common"]
        #             }
        #         },
        #         {
        #             "path": "/permission/button",
        #             "meta": {
        #                 "title": "menus.purePermissionButton",
        #                 "roles": ["admin", "common"]
        #             },
        #             "children": [
        #                 {
        #                     "path": "/permission/button/router",
        #                     "component": "permission/button/index",
        #                     "name": "PermissionButtonRouter",
        #                     "meta": {
        #                         "title": "menus.purePermissionButtonRouter",
        #                         "auths": [
        #                             "permission:btn:add",
        #                             "permission:btn:edit",
        #                             "permission:btn:delete"
        #                         ]
        #                     }
        #                 },
        #                 {
        #                     "path": "/permission/button/login",
        #                     "component": "permission/button/perms",
        #                     "name": "PermissionButtonLogin",
        #                     "meta": {
        #                         "title": "menus.purePermissionButtonLogin"
        #                     }
        #                 }
        #             ]
        #         }
        #     ]
        # },
        # {
        #     "path": "/iframe",
        #     "meta": {
        #         "icon": "ri:links-fill",
        #         "title": "menus.pureExternalPage",
        #         "rank": 23
        #     },
        #     "children": [
        #         {
        #             "path": "/iframe/embedded",
        #             "meta": {
        #                 "title": "menus.pureEmbeddedDoc"
        #             },
        #             "children": [
        #                 {
        #                     "path": "/iframe/colorhunt",
        #                     "name": "FrameColorHunt",
        #                     "meta": {
        #                         "title": "menus.pureColorHuntDoc",
        #                         "frameSrc": "https://colorhunt.co/",
        #                         "keepAlive": True,
        #                         "roles": ["admin", "common"]
        #                     }
        #                 },
        #                 {
        #                     "path": "/iframe/uigradients",
        #                     "name": "FrameUiGradients",
        #                     "meta": {
        #                         "title": "menus.pureUiGradients",
        #                         "frameSrc": "https://uigradients.com/",
        #                         "keepAlive": True,
        #                         "roles": ["admin", "common"]
        #                     }
        #                 },
        #                 {
        #                     "path": "/iframe/ep",
        #                     "name": "FrameEp",
        #                     "meta": {
        #                         "title": "menus.pureEpDoc",
        #                         "frameSrc": "https://element-plus.org/zh-CN/",
        #                         "keepAlive": True,
        #                         "roles": ["admin", "common"]
        #                     }
        #                 },
        #                 {
        #                     "path": "/iframe/tailwindcss",
        #                     "name": "FrameTailwindcss",
        #                     "meta": {
        #                         "title": "menus.pureTailwindcssDoc",
        #                         "frameSrc": "https://tailwindcss.com/docs/installation",
        #                         "keepAlive": True,
        #                         "roles": ["admin", "common"]
        #                     }
        #                 },
        #                 {
        #                     "path": "/iframe/vue3",
        #                     "name": "FrameVue",
        #                     "meta": {
        #                         "title": "menus.pureVueDoc",
        #                         "frameSrc": "https://cn.vuejs.org/",
        #                         "keepAlive": True,
        #                         "roles": ["admin", "common"]
        #                     }
        #                 },
        #                 {
        #                     "path": "/iframe/vite",
        #                     "name": "FrameVite",
        #                     "meta": {
        #                         "title": "menus.pureViteDoc",
        #                         "frameSrc": "https://cn.vitejs.dev/",
        #                         "keepAlive": True,
        #                         "roles": ["admin", "common"]
        #                     }
        #                 },
        #                 {
        #                     "path": "/iframe/pinia",
        #                     "name": "FramePinia",
        #                     "meta": {
        #                         "title": "menus.purePiniaDoc",
        #                         "frameSrc": "https://pinia.vuejs.org/zh/index.html",
        #                         "keepAlive": True,
        #                         "roles": ["admin", "common"]
        #                     }
        #                 },
        #                 {
        #                     "path": "/iframe/vue-router",
        #                     "name": "FrameRouter",
        #                     "meta": {
        #                         "title": "menus.pureRouterDoc",
        #                         "frameSrc": "https://router.vuejs.org/zh/",
        #                         "keepAlive": True,
        #                         "roles": ["admin", "common"]
        #                     }
        #                 }
        #             ]
        #         },
        #         {
        #             "path": "/iframe/external",
        #             "meta": {
        #                 "title": "menus.pureExternalDoc"
        #             },
        #             "children": [
        #                 {
        #                     "path": "/external",
        #                     "name": "https://pure-admin.github.io/pure-admin-doc",
        #                     "meta": {
        #                         "title": "menus.pureExternalLink",
        #                         "roles": ["admin", "common"]
        #                     }
        #                 },
        #                 {
        #                     "path": "/pureUtilsLink",
        #                     "name": "https://pure-admin-utils.netlify.app/",
        #                     "meta": {
        #                         "title": "menus.pureUtilsLink",
        #                         "roles": ["admin", "common"]
        #                     }
        #                 }
        #             ]
        #         }
        #     ]
        # },
        # {
        #     "path": "/tabs",
        #     "meta": {
        #         "icon": "ri:bookmark-2-line",
        #         "title": "menus.pureTabs",
        #         "rank": 24
        #     },
        #     "children": [
        #         {
        #             "path": "/tabs/index",
        #             "name": "Tabs",
        #             "meta": {
        #                 "title": "menus.pureTabs",
        #                 "roles": ["admin", "common"]
        #             }
        #         },
        #         {
        #             "path": "/tabs/query-detail",
        #             "name": "TabQueryDetail",
        #             "meta": {
        #                 "showLink": False,
        #                 "activePath": "/tabs/index",
        #                 "roles": ["admin", "common"]
        #             }
        #         }
        #     ]
        # },
        # ]
        # return Response(data=data)
