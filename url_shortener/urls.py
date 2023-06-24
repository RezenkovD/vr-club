from django.contrib.auth import views as auth_views
from django.urls import path

from .views import home_view, redirect_url_view

app_name = "url-shortener"

urlpatterns = [
    path("", home_view, name="home"),
    path("<str:shortened_part>", redirect_url_view, name="redirect"),
]
