from django.urls import re_path
from rest_framework.routers import DefaultRouter

from external_guarantee.views import (
    ExternalGuaranteeViewSet,
    ExternalBeGuaranteedViewSet,
)

router = DefaultRouter()
# 对外担保
router.register(r"guarantee", ExternalGuaranteeViewSet, basename="guarantee")
router.register(
    r"be_guaranteed", ExternalBeGuaranteedViewSet, basename="guarantee_detail"
)
urlpatterns = []


urlpatterns += router.urls
