from django.shortcuts import redirect, render
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import BookingForm
from .models import Booking, BookingTime, ACTUAL, OUTDATED
from .utils import get_available_slots, SessionSeats


COST_SESSION = 200
MAX_SESSION = 2


def home(request):
    signup_url = reverse("account_signup")
    login_url = reverse("account_login")
    return render(
        request, "site/index.html", {"signup_url": signup_url, "login_url": login_url}
    )


def booking_view(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Будь ласка, оберіть слот, перед відправкою!")
            return render_main_page()

        _available_slots = get_available_slots()
        slot_av_slots = {
            y[0]: x for y, x in zip(BookingTime.TIME_CHOICES, available_slots)
        }
        slot_compatibility = {
            y[0]: index for index, y in enumerate(BookingTime.TIME_CHOICES)
        }
        slots = form.cleaned_data["slots"]
        if len(slots) > MAX_SESSION:
            messages.error(request, f"Максимальна кількість обраних сеансів: {MAX_SESSION}")
            return render_main_page()

        if len(slots) > 1:
            _is_all_neighbors = is_all_neighbors(slot_compatibility, slots)

            if not _is_all_neighbors:
                messages.error(request, "Сеанси мають бути суміжними")
                return render_main_page()

        people_count = form.cleaned_data["number_of_people"]
        _has_invalid_slots = has_invalid_slots(request, people_count, slot_av_slots, slots)

        if not _has_invalid_slots:
            book_session(slots, form.cleaned_data)
            return redirect("site:home")

    return render_main_page()


def is_all_neighbors(slot_compatibility, slots):
    slots_values = [abs(slot_compatibility[value]) for value in slots]
    sorted_slots = sorted(slots_values)
    for i in range(1, len(sorted_slots)):
        if sorted_slots[i] - sorted_slots[i - 1] != 1:
            return False

    return True


def has_invalid_slots(request, people_count, slot_av_slots, slots):
    _has_invalid_slots = False
    for slot in slots:
        if slot_av_slots[slot] <= 0 or slot_av_slots[slot] < people_count:
            messages.error(request, f"Місць для {slot} вже немає!")
            _has_invalid_slots = True

    return _has_invalid_slots


def render_main_page():
    signup_url = reverse("account_signup")
    login_url = reverse("account_login")

    form = BookingForm()
    _available_slots = get_available_slots()
    return render(
        request,
        "site/index.html",
        {
            "form": form,
            "available_slots": _available_slots,
            "signup_url": signup_url,
            "login_url": login_url,
        },
    )


def book_session(slots, data_to_save):
    booking = Booking(
        name=data_to_save["name"],
        email=data_to_save["email"],
        phone_number=data_to_save["phone_number"],
        number_of_people=data_to_save["number_of_people"],
        comment=data_to_save["comment"],
        price=COST_SESSION * data_to_save["number_of_people"] * len(slots),
    )
    booking.save()

    booking_slots = booking.time.all()  # TODO: Коли може бути?
    for booking_slot in booking_slots:
        booking_slot.status = OUTDATED
        booking_slot.save()

    for slot in slots:
        booking_time = BookingTime(time=slot, status=ACTUAL)
        booking_time.save()
        # TODO: https://docs.djangoproject.com/en/3.0/ref/models/querysets/#bulk-create
        booking.time.add(booking_time)
