from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse

from .forms import BookingForm
from .models import BookingTime
from .utils import (
    get_available_slots,
    get_available_slots_for_month,
    get_session_seats,
    is_all_neighbors,
    has_invalid_slots,
    book_session,
    MAX_SESSION,
)


def get_available_slots_view(request):
    if request.method == "GET":
        selected_date = request.GET.get("date")
        available_slots = get_available_slots(selected_date)
        return JsonResponse({"available_slots": available_slots})


def get_available_slots_for_month_view(request):
    if request.method == "GET":
        year = request.GET.get("year")
        month = request.GET.get("month")
        available_slots = get_available_slots_for_month(year, month)
        return JsonResponse({"available_slots": available_slots})


def index_page(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Будь ласка, оберіть слот, перед відправкою!")
            return render_index_page(request)
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
            return render_index_page(request)

        if len(slots) > 1:
            _is_all_neighbors = is_all_neighbors(slot_compatibility, slots)

            if not _is_all_neighbors:
                messages.error(request, "Сеанси мають бути суміжними")
                return render_index_page(request)

        people_count = form.cleaned_data["people_count"]
        _has_invalid_slots = has_invalid_slots(
            request, people_count, slot_av_slots, slots
        )

        if not _has_invalid_slots:
            book_session(request, slots, form.cleaned_data)
            return redirect("site:home")

    return render_index_page(request)


def render_index_page(request):
    signup_url = reverse("account_signup")
    login_url = reverse("account_login")
    form = BookingForm()
    return render(
        request,
        "site/index.html",
        {
            "form": form,
            "signup_url": signup_url,
            "login_url": login_url,
        },
    )
