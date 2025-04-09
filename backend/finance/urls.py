from django.urls import re_path
from rest_framework.routers import DefaultRouter

from finance.views import (
    LoanViewSet,
    LoanRepayViewSet,
    LoanInterestViewSet,
)

router = DefaultRouter()
# 对外担保
router.register(r"loan", LoanViewSet, basename="loan")
router.register(r"repay", LoanRepayViewSet, basename="repay")
router.register(r"interest", LoanInterestViewSet, basename="interest")
urlpatterns = []


urlpatterns += router.urls
