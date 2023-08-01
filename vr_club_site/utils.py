from django.db.models import Sum

from .models import Booking, BookingTime, ACTUAL, Settings


def get_available_slots(selected_date=None):
    _available_slots = []

    try:
        session_seats = Settings.objects.get(name='seats')
    except Settings.DoesNotExist:
        session_seats = 1

    for x in BookingTime.TIME_CHOICES:
        try:
            slot = (
                Booking.objects.filter(
                    time__status=ACTUAL, time__time=x[0], time__date=selected_date
                ).aggregate(total_people=Sum("people_count"))["total_people"]
                or 0
            )
        except BookingTime.DoesNotExist:
            slot = 0
        _available_slots.append(session_seats - slot)
    return tuple(_available_slots)
