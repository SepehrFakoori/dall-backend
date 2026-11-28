from rest_framework.routers import DefaultRouter

from .views import AssetViewSet

router = DefaultRouter()

router.register("assets", AssetViewSet, basename="assets")

urlpatterns = router.urls
