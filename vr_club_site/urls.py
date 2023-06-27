from django.contrib.auth import views as auth_views
from django.urls import path

from .views import home, booking_view

app_name = "site"

urlpatterns = [
    path("", home, name="home"),
    path("booking/", booking_view, name="booking"),
]
