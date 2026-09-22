from django.contrib import admin
from django.urls import path, include

from app.views import LoginAPIView

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("admin/", admin.site.urls),

    path("api-auth/", include("rest_framework.urls")),

    path("api/", include("app.router")),

    # Custom Login
    path(
        "api/login/",
        LoginAPIView.as_view(),
        name="login"
    ),

    # Refresh Token
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),
]