from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import (
    OrganizationViewSet,
    OrganizationMembershipViewSet,
    DepartmentViewSet,
    DepartmentMembershipViewSet,
)

router = DefaultRouter()

router.register(
    "organizations",
    OrganizationViewSet,
    basename="organization",
)


# Organization nested router
organizations_router = NestedDefaultRouter(
    router,
    "organizations",
    lookup="organization",
)

organizations_router.register(
    "memberships",
    OrganizationMembershipViewSet,
    basename="organization-membership",
)
organizations_router.register(
    "departments",
    DepartmentViewSet,
    basename="organization-department",
)


# Department nested router
departments_router = NestedDefaultRouter(
    organizations_router,
    "departments",
    lookup="department",
)

departments_router.register(
    "memberships",
    DepartmentMembershipViewSet,
    basename="department-membership",
)

urlpatterns = router.urls + organizations_router.urls + departments_router.urls
