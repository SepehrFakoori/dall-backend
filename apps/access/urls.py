from rest_framework.routers import DefaultRouter

from .views import RoleViewSet

router = DefaultRouter()

router.register("access", RoleViewSet, basename="access")

urlpatterns = router.urls
