from rest_framework.routers import DefaultRouter

from .views import OrganizationViewSet, OrganizationMemberShipViewSet

router = DefaultRouter()

router.register("organizations", OrganizationViewSet)
router.register("organizations/memberships", OrganizationMemberShipViewSet)

urlpatterns = router.urls
