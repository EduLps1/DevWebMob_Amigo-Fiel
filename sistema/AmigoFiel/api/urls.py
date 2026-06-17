from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    AmigoFielTokenObtainPairView,
    MeView,
    MobileHomeView,
    MobileLojasView,
    MobileOngsView,
    MobilePetsView,
    MobileProdutosView,
)


app_name = "api"

urlpatterns = [
    path("auth/token/", AmigoFielTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/me/", MeView.as_view(), name="me"),
    path("mobile/home/", MobileHomeView.as_view(), name="mobile-home"),
    path("mobile/pets/", MobilePetsView.as_view(), name="mobile-pets"),
    path("mobile/produtos/", MobileProdutosView.as_view(), name="mobile-produtos"),
    path("mobile/lojas/", MobileLojasView.as_view(), name="mobile-lojas"),
    path("mobile/ongs/", MobileOngsView.as_view(), name="mobile-ongs"),
]
