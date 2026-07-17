from django.urls import path

from .views import LoginAPIView, LoginRefreshAPIView

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="user-login"),
    path("login/refresh/", LoginRefreshAPIView.as_view(), name="user-login-refresh"),
]
