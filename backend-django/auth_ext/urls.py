from auth_ext.views.department import DepartmentViewSet
from auth_ext.views.menu import MenuViewSet, MenuTreeViewSet
from auth_ext.views.role import RoleViewSet
from auth_ext.views.routes import AsyncRoute
from auth_ext.views.user import (
    AuthExtUserView,
    AuthRefreshToken,
    AuthUserMineView,
    AuthUserViewSet,
    AuthUserInfoViewSet,
)
from django.urls import re_path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"dept", DepartmentViewSet, basename="dept")
router.register(r"role", RoleViewSet, basename="role")
# 菜单管理
router.register(r"menu", MenuViewSet, basename="menu")
router.register("user", AuthUserInfoViewSet, basename="user")
# 刷新JWT有效期接口
urlpatterns = [
    re_path(r"login/$", AuthExtUserView.as_view(), name="token"),
    re_path("refreshToken/", AuthRefreshToken.as_view(), name="token_refresh"),
    re_path("sign/", AuthUserViewSet.as_view(), name="user"),
    re_path("asyncRoutes/", AsyncRoute.as_view(), name="asyncRoutes"),
    re_path("mine/", AuthUserMineView.as_view(), name="mine"),
    re_path("menu/menu_tree/", MenuTreeViewSet.as_view(), name="role-menu")
]


urlpatterns += router.urls
