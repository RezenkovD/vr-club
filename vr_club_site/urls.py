from django.urls import path

from .views import (
    index_page,
    devices_page,
    get_available_slots_view,
    get_available_slots_for_month_view,
    get_price_day,
)
from games.views import games_page

app_name = "site"

urlpatterns = [
    path("", index_page, name="home"),
    path("games/", games_page, name="games"),
    path("devices/", devices_page, name="devices"),
    path(
        "api/get_available_slots/",
        get_available_slots_view,
        name="get_available_slots",
    ),
    path(
        "api/get_available_slots_for_month/",
        get_available_slots_for_month_view,
        name="get_available_slots_for_month",
    ),
    path(
        "api/get_price_day/",
        get_price_day,
        name="get_price_day",
    ),
]
