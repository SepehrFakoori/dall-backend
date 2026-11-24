from rest_framework_nested.routers import NestedDefaultRouter

from apps.tenants.urls import router
from apps.tenants.views import MembershipViewSet
from .views import DepartmentViewSet, DepartmentMembershipViewSet

tenant_router = NestedDefaultRouter(
    router,
    "tenants",
    lookup="tenant",
)

tenant_router.register(
    "memberships",
    MembershipViewSet,
    basename="tenant-membership",
)

tenant_router.register(
    "departments",
    DepartmentViewSet,
    basename="tenant-department",
)

department_router = NestedDefaultRouter(
    tenant_router,
    "departments",
    lookup="departments",
)

department_router.register(
    "memberships",
    DepartmentMembershipViewSet,
    basename="department-membership",
)

urlpatterns = router.urls + tenant_router.urls + department_router.urls
