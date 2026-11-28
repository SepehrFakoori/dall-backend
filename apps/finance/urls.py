from rest_framework.routers import DefaultRouter

from .views import AccountTypeViewSet, BankAccountViewSet

router = DefaultRouter()

router.register("finance/accounts-types", AccountTypeViewSet, basename="account-type")
router.register("finance/bank-accounts", BankAccountViewSet, basename="bank-account")

urlpatterns = router.urls
