from rest_framework.routers import DefaultRouter

from basic.views import BasicViewSet

router = DefaultRouter()
# 对外担保
router.register(r"basic", BasicViewSet, basename="basic")
urlpatterns = []


urlpatterns += router.urls
