from django.db.models import Sum

from .models import Booking, BookingTime, ACTUAL
from .models import SessionSeats


def get_available_slots():
    _available_slots = []

    try:
        session_seats = SessionSeats.objects.latest("id").number
    except SessionSeats.DoesNotExist:
        session_seats = 1

    for x in BookingTime.TIME_CHOICES:
        try:
            slot = (
                Booking.objects.filter(time__status=ACTUAL, time__time=x[0]).aggregate(
                    total_people=Sum("number_of_people")
                )["total_people"]
                or 0
            )
        except BookingTime.DoesNotExist:
            slot = 0
        _available_slots.append(session_seats - slot)
    return tuple(_available_slots)
