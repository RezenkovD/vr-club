from django.contrib.auth import views as auth_views
from django.urls import path

from .views import filter_games

app_name = "api/games"

urlpatterns = [
    path("", filter_games, name="filter_games"),
]
