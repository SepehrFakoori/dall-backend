from rest_framework.routers import DefaultRouter

from .views import BankViewSet, CheckViewSet

router = DefaultRouter()

router.register("finance/bank-accounts", BankViewSet)
router.register("finance/checks", CheckViewSet)

urlpatterns = router.urls
