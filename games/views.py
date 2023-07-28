from django.shortcuts import render, reverse
from django.http import HttpResponseBadRequest, JsonResponse
from django.db.models import Q

from .models import Games

# Create your views here.


def games(request):
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
        {"signup_url": signup_url, "login_url": login_url, "games": games},
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
