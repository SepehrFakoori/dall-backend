from rest_framework.routers import DefaultRouter
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

from .views import UserViewSet, ChangePasswordView, LoginView

router = DefaultRouter()
router.register("users", UserViewSet)

urlpatterns = router.urls + [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="login"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]
