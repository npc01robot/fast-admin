from rest_framework.routers import DefaultRouter

from grid.views import GridViewSet

router = DefaultRouter()
router.register(r"grid", GridViewSet, basename="grid")
urlpatterns = []
urlpatterns += router.urls
