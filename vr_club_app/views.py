from django.shortcuts import render


# Create your views here.


def home(request):
    return render(request, "VORTEX.html")


def may(request):
    return render(request, "index.html")
