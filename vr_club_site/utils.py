from django.db.models import Count
from .forms import BookingForm
from .models import Booking, BookingTime, ACTUAL


def available__slots(request):
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
    return tuple(available_slots)
