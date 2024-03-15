from django.urls import re_path

from auth_ext.views import AuthUserViewSet, AuthExtUserView, AsyncRoute, AuthRefreshToken

# 刷新JWT有效期接口
urlpatterns = [
    re_path(r'login/$', AuthExtUserView.as_view(), name='token'),
    re_path('refreshToken/', AuthRefreshToken.as_view(), name='token_refresh'),
    re_path('sign/', AuthUserViewSet.as_view(), name='user'),
    re_path('asyncRoutes/', AsyncRoute.as_view(), name='asyncRoutes')

]