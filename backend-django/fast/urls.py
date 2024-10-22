"""yinbao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path


MODULE_DICT = {
    "login": "登录",
    "sign": "注册",
    "dept": "部门管理",
    "role": "角色管理",
    "user": "用户管理",
    "menu": "菜单管理",
    "grid": "表格管理",
}


class APIUrls:
    urlpatterns = [
        path("grid/", include("grid.urls")),
    ]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("auth_ext.urls")),
    path("fast/", include(APIUrls.urlpatterns)),
]
