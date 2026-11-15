from rest_framework.routers import DefaultRouter

from .views import PermissionViewSet, RoleViewSet, UserRoleViewSet

router = DefaultRouter()

router.register("permission", PermissionViewSet)
router.register("role", RoleViewSet)
router.register("user-roles", UserRoleViewSet)

urlpatterns = router.urls
