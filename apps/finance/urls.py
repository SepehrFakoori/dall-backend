from rest_framework.routers import DefaultRouter

from .views import BankViewSet, CheckTypeViewSet, CheckStatusViewSet, CheckViewSet

router = DefaultRouter()

router.register("finance/bank-accounts", BankViewSet)
router.register("finance/checks", CheckViewSet)
router.register("finance/checks-types", CheckTypeViewSet)
router.register("finance/checks-status", CheckStatusViewSet)

urlpatterns = router.urls
