from django.shortcuts import redirect, render
from django.db.models import Count
from django.contrib.auth.decorators import login_required

from .forms import BookingForm
from .models import Booking, BookingTime, ACTUAL

# Create your views here.


def home(request):
    return render(request, "site/index.html")


@login_required(login_url="users:sign-in")
def booking_view(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            user = request.user
            booking = Booking(user=user, comment=comment)
            booking.save()
            slots = form.cleaned_data["slots"]
            for slot in slots:
                booking_time = BookingTime(time=slot, status=ACTUAL)
                booking_time.save()
                booking.time.add(booking_time)
            return redirect("site:home")
    form = BookingForm()
    user = request.user
    available_slots = []
    for x in BookingTime.TIME_CHOICES:
        try:
            slot = (
                BookingTime.objects.filter(status=ACTUAL, time=x[0])
                .exclude(booking__user=user)
                .aggregate(count=Count("id"))["count"]
            )
        except BookingTime.DoesNotExist:
            slot = 0
        available_slots.append(4 - slot)
    return render(
        request,
        "site/booking.html",
        {
            "form": form,
            "available_slots": available_slots,
        },
    )
