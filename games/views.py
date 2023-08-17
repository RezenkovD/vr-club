from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseBadRequest, JsonResponse
from django.db.models import Q
from django.contrib import messages

from .models import Games

from vr_club_site.forms import BookingForm
from vr_club_site.models import BookingTime
from vr_club_site.utils import (
    get_available_slots,
    has_invalid_slots,
    is_all_neighbors,
    book_session,
    MAX_SESSION,
)


def games_page(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Будь ласка, оберіть слот, перед відправкою!")
            return render_game_page(request)
        selected_date = form.cleaned_data["date"]
        _available_slots = get_available_slots(selected_date)
        slot_av_slots = {
            y[0]: x for y, x in zip(BookingTime.TIME_CHOICES, _available_slots)
        }
        slot_compatibility = {
            y[0]: index for index, y in enumerate(BookingTime.TIME_CHOICES)
        }
        slots = form.cleaned_data["slots"]

        if len(slots) > MAX_SESSION:
            messages.error(
                request, f"Максимальна кількість обраних сеансів: {MAX_SESSION}"
            )
            return render_game_page(request)

        if len(slots) > 1:
            _is_all_neighbors = is_all_neighbors(slot_compatibility, slots)

            if not _is_all_neighbors:
                messages.error(request, "Сеанси мають бути суміжними")
                return render_game_page(request)

        people_count = form.cleaned_data["people_count"]
        _has_invalid_slots = has_invalid_slots(
            request, people_count, slot_av_slots, slots
        )

        if not _has_invalid_slots:
            book_session(request, slots, form.cleaned_data)
            return redirect("site:games")

    return render_game_page(request)


def render_game_page(request):
    form = BookingForm()
    signup_url = reverse("account_signup")
    login_url = reverse("account_login")
    game_mode = request.GET.get("game_mode")
    games = Games.objects.all()
    if game_mode == "multiplayer":
        games = games.filter(game_mode="single")
    elif game_mode == "signle":
        games = games.filter(game_mode="multiplayer")
    return render(
        request,
        "games/games.html",
        {
            "form": form,
            "signup_url": signup_url,
            "login_url": login_url,
            "games": games,
        },
    )


def filter_games(request):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    if is_ajax:
        if request.method == "GET":
            game_mode = request.GET.get("game_mode")
            filter_condition = Q(game_mode="both")
            if game_mode == "multiplayer":
                filter_condition |= Q(game_mode="multiplayer")
            elif game_mode == "single":
                filter_condition |= Q(game_mode="single")
            else:
                games = list(Games.objects.all().values())
                return JsonResponse({"context": games})
            games = list(Games.objects.filter(filter_condition).values())
            return JsonResponse({"context": games})
        return JsonResponse({"status": "Invalid request"}, status=400)
    else:
        return HttpResponseBadRequest("Invalid request")
