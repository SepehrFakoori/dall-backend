from rest_framework.routers import DefaultRouter

from .views import ProjectViewSet, UseViewSet

router = DefaultRouter()

router.register("projects", ProjectViewSet)
router.register("uses", UseViewSet)

urlpatterns = router.urls
