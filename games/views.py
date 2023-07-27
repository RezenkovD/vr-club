from django.shortcuts import render, reverse

from .models import Games

# Create your views here.


def games(request):
    signup_url = reverse("account_signup")
    login_url = reverse("account_login")
    games = Games.objects.all()
    return render(
        request,
        "games/games.html",
        {"signup_url": signup_url, "login_url": login_url, "games": games},
    )
