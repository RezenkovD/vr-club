from django.contrib.auth import views as auth_views
from django.urls import path

from .views import home

app_name = "intro"

urlpatterns = [
    path("", home, name="homepage"),
]
