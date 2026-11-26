from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CurrentTenantView, MembershipViewSet

router = DefaultRouter()
router.register("memberships", MembershipViewSet, basename="membership")

urlpatterns = [
    path("tenant/", CurrentTenantView.as_view(), name="current-tenant"),
    *router.urls,
]
