from django.shortcuts import redirect, render
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import BookingForm
from .models import Booking, BookingTime, ACTUAL, OUTDATED
from .utils import available__slots, SessionSeats


COST_SESSION = 200


def home(request):
    signup_url = reverse("account_signup")
    login_url = reverse("account_login")
    return render(
        request, "site/index.html", {"signup_url": signup_url, "login_url": login_url}
    )


@login_required(login_url="/users/login/")
def booking_view(request):
    signup_url = reverse("account_signup")
    login_url = reverse("account_login")
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            available_slots = available__slots()
            slot_av_slots = {
                y[0]: x for y, x in zip(BookingTime.TIME_CHOICES, available_slots)
            }
            slot_compatibility = {
                y[0]: index for index, y in enumerate(BookingTime.TIME_CHOICES)
            }
            slots = form.cleaned_data["slots"]
            if len(slots) > 2:
                messages.error(request, f"Максимальна кількість обраних сеансів: 2")
                form = BookingForm()
                available_slots = available__slots()
                return render(
                    request,
                    "site/index.html",
                    {
                        "form": form,
                        "available_slots": available_slots,
                        "signup_url": signup_url,
                        "login_url": login_url,
                    },
                )
            if len(slots) == 2:
                if (
                    abs(slot_compatibility[slots[0]] - slot_compatibility[slots[1]])
                    != 1
                ):
                    messages.error(request, f"Сеанси мають бути суміжними")
                    form = BookingForm()
                    available_slots = available__slots()
                    return render(
                        request,
                        "site/index.html",
                        {
                            "form": form,
                            "available_slots": available_slots,
                            "signup_url": signup_url,
                            "login_url": login_url,
                        },
                    )
            invalid_slots = []
            for slot in slots:
                if (
                    slot_av_slots[slot] <= 0
                    or slot_av_slots[slot] < form.cleaned_data["number_of_people"]
                ):
                    invalid_slots.append(slot)
            if not invalid_slots:
                data_to_save = form.cleaned_data
                booking = Booking(
                    name=data_to_save["name"],
                    email=data_to_save["email"],
                    phone_number=data_to_save["phone_number"],
                    number_of_people=data_to_save["number_of_people"],
                    comment=data_to_save["comment"],
                    price=COST_SESSION * data_to_save["number_of_people"] * len(slots),
                )
                booking.save()
                booking_slots = booking.time.all()
                for booking_slot in booking_slots:
                    booking_slot.status = OUTDATED
                    booking_slot.save()
                for slot in slots:
                    booking_time = BookingTime(time=slot, status=ACTUAL)
                    booking_time.save()
                    booking.time.add(booking_time)
                return redirect("site:home")
            else:
                for x in range(len(invalid_slots)):
                    messages.error(request, f"Місць для {invalid_slots[x]} вже немає!")
        else:
            messages.error(request, "Будь ласка, оберіть слот, перед відправкою!")
    form = BookingForm()
    available_slots = available__slots()
    return render(
        request,
        "site/index.html",
        {
            "form": form,
            "available_slots": available_slots,
            "signup_url": signup_url,
            "login_url": login_url,
        },
    )
