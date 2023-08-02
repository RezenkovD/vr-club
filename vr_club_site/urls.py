from django.urls import path

from .views import home, booking_view, get_available_slots_view
from games.views import games

app_name = "site"

urlpatterns = [
    path("", booking_view, name="home"),
    path("games/", games, name="games"),
    path(
        "api/get_available_slots/",
        get_available_slots_view,
        name="get_available_slots",
    ),
]
