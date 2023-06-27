from django.contrib.auth import views as auth_views
from django.urls import path

from .views import home

app_name = "site"

urlpatterns = [
    path("", home, name="home"),
]
