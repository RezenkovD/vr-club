from django.urls import path

from .views import index_page, get_available_slots_view
from games.views import game_page

app_name = "site"

urlpatterns = [
    path("", index_page, name="home"),
    path("games/", game_page, name="games"),
    path(
        "api/get_available_slots/",
        get_available_slots_view,
        name="get_available_slots",
    ),
]
