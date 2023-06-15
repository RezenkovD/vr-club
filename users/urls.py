from django.contrib.auth import views as auth_views
from django.urls import path

from .views import home, login_request, logout_request, register_request

app_name = "main"

urlpatterns = [
    path("", home, name="homepage"),
    path("sign-up/", register_request, name="register"),
    path("sign-in/", login_request, name="login"),
    path("logout/", logout_request, name="logout"),
]
