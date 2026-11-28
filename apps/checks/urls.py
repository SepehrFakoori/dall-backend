from rest_framework.routers import DefaultRouter

from .views import CheckTypeViewSet, CheckStatusViewSet, CheckViewSet

router = DefaultRouter()

router.register("checks", CheckViewSet, basename="check")
router.register("checks/types", CheckTypeViewSet, basename="check-type")
router.register("checks/status", CheckStatusViewSet, basename="check-status")

urlpatterns = router.urls
