from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase, TokenRefreshView

from auth_ext.models import AuthExtUser
from auth_ext.serializers import AuthExtTokenObtainPairSerializer, AuthUserSerializer, AuthRefreshTokenSerializer, \
    DepartmentSerializer


# Create your views here.

# 登录视图
class AuthExtUserView(TokenViewBase):
    serializer_class = AuthExtTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

# 注册
class AuthUserViewSet(generics.GenericAPIView):
    serializer_class = AuthUserSerializer
    queryset = AuthExtUser.objects.all()
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # 生成token
        token_serializer = AuthExtTokenObtainPairSerializer(
            data=request.data
        )
        token_serializer.is_valid(raise_exception=True)
        return Response(token_serializer.validated_data, status=status.HTTP_200_OK)


# 刷新token
class AuthRefreshToken(TokenRefreshView):
    serializer_class = AuthRefreshTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

# 用户信息
class AuthUserInfoView(generics.RetrieveAPIView):
    serializer_class = AuthUserSerializer
    queryset = AuthExtUser.objects.all()
    permission_classes = []

    def get_object(self):
        return self.request.user


# 路由生成
# todo: 路由生成功能待完善
class AsyncRoute(generics.GenericAPIView):
    """
    动态生成路由,大型项目使用
    """

    def get(self, request, *args, **kwargs):
        user = AuthExtUser.objects.filter(pk=request.auth.payload['user_code']).first()
        data = [
            {
                "path": "/system",
                "meta": {
                    "icon": "ri:settings-3-line",
                    "title": "menus.pureSysManagement",
                    "rank": 20
                },
                "children": [
                    {
                        "path": "/system/user/index",
                        "name": "SystemUser",
                        "meta": {
                            "icon": "ri:admin-line",
                            "title": "menus.pureUser",
                            "roles": user.roles
                        }
                    },
                    {
                        "path": "/system/role/index",
                        "name": "SystemRole",
                        "meta": {
                            "icon": "ri:admin-fill",
                            "title": "menus.pureRole",
                            "roles": user.roles
                        }
                    },
                    {
                        "path": "/system/menu/index",
                        "name": "SystemMenu",
                        "meta": {
                            "icon": "ep:menu",
                            "title": "menus.pureSystemMenu",
                            "roles": user.roles
                        }
                    },
                    {
                        "path": "/system/dept/index",
                        "name": "SystemDept",
                        "meta": {
                            "icon": "ri:git-branch-line",
                            "title": "menus.pureDept",
                            "roles": user.roles
                        }
                    }
                ]
            },
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
        ]
        return Response(data=data)

class DepartmentViewSet(generics.ListAPIView):
    serializer_class = DepartmentSerializer
    queryset = AuthExtUser.objects.all()
    permission_classes = []

