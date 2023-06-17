from django.contrib.auth import views as auth_views
from django.urls import path

from .views import home, logout_request, sign_in, sign_up

app_name = "users"

urlpatterns = [
    path("", home, name="homepage"),
    path("sign-up/", sign_up, name="sign-up"),
    path("sign-in/", sign_in, name="sign-in"),
    path("logout/", logout_request, name="logout"),
]
