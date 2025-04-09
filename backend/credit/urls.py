from django.urls import re_path
from rest_framework.routers import DefaultRouter

from credit.views import CreditViewSet

router = DefaultRouter()
# 授信
router.register(r"credit", CreditViewSet, basename="finance")
urlpatterns = []


urlpatterns += router.urls
