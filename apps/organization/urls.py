from rest_framework.routers import DefaultRouter

from .views import DepartmentViewSet, DepartmentMembershipViewSet

router = DefaultRouter()

router.register(
    "departments",
    DepartmentViewSet,
    basename="department",
)

router.register(
    "memberships",
    DepartmentMembershipViewSet,
    basename="department-membership",
)

urlpatterns = router.urls
