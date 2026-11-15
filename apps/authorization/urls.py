from rest_framework.routers import DefaultRouter

from .views import PermissionViewSet, RoleViewSet, UserRoleViewSet

router = DefaultRouter()

router.register("permissions", PermissionViewSet)
router.register("roles", RoleViewSet)
router.register("user-roles", UserRoleViewSet)

urlpatterns = router.urls
