from rest_framework.routers import DefaultRouter

from .views import (
    AccountTypeViewSet,
    BankAccountViewSet,
    CheckTypeViewSet,
    CheckStatusViewSet,
    CheckViewSet,
)

router = DefaultRouter()

router.register("finance/accounts-types", AccountTypeViewSet, basename="account-type")
router.register("finance/bank-accounts", BankAccountViewSet, basename="bank-account")
router.register("finance/checks", CheckViewSet, basename="check")
router.register("finance/checks-types", CheckTypeViewSet, basename="check-type")
router.register("finance/checks-status", CheckStatusViewSet, basename="check-status")

urlpatterns = router.urls
