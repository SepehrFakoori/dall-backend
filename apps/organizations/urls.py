from rest_framework.routers import DefaultRouter

from .views import (
    OrganizationViewSet,
    OrganizationMembershipsViewSet,
    OrganizationUnitsViewSet,
)

router = DefaultRouter()

router.register("organizations", OrganizationViewSet)
router.register("organizations/memberships", OrganizationMembershipsViewSet)
router.register("organizations/units", OrganizationUnitsViewSet)

urlpatterns = router.urls
