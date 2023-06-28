from django.shortcuts import redirect, render
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import BookingForm
from .models import Booking, BookingTime, ACTUAL
from .utils import available__slots

# Create your views here.


def home(request):
    return render(request, "site/index.html")


@login_required(login_url="users:sign-in")
def booking_view(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            available_slots = available__slots(request)
            slot_av_slots = {
                y[0]: x for y, x in zip(BookingTime.TIME_CHOICES, available_slots)
            }
            unavailable_slots = []
            slots = form.cleaned_data["slots"]
            for slot in slots:
                if slot_av_slots[slot] <= 0:
                    unavailable_slots.append(slot)
            if not unavailable_slots:
                comment = form.cleaned_data["comment"]
                user = request.user
                booking = Booking(user=user, comment=comment)
                booking.save()
                for slot in slots:
                    booking_time = BookingTime(time=slot, status=ACTUAL)
                    booking_time.save()
                    booking.time.add(booking_time)
                return redirect("site:home")
            else:
                for x in range(len(unavailable_slots)):
                    messages.error(
                        request, f"Місць для {unavailable_slots[x]} вже немає!"
                    )
        else:
            messages.error(request, "Будь ласка, оберіть слот, перед відправкою!")
    form = BookingForm()
    available_slots = available__slots(request)
    return render(
        request,
        "site/booking.html",
        {
            "form": form,
            "available_slots": available_slots,
        },
    )