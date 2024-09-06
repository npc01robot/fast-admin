from auth_ext.views.department import DepartmentViewSet
from auth_ext.views.routes import AsyncRoute
from auth_ext.views.user import (
    AuthExtUserView,
    AuthRefreshToken,
    AuthUserInfoView,
    AuthUserViewSet,
)
from django.urls import re_path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"dept", DepartmentViewSet, basename="dept")
# 刷新JWT有效期接口
urlpatterns = [
    re_path(r"login/$", AuthExtUserView.as_view(), name="token"),
    re_path("refreshToken/", AuthRefreshToken.as_view(), name="token_refresh"),
    re_path("sign/", AuthUserViewSet.as_view(), name="user"),
    re_path("asyncRoutes/", AsyncRoute.as_view(), name="asyncRoutes"),
    re_path("mine/", AuthUserInfoView.as_view(), name="mine"),
]


urlpatterns += router.urls
