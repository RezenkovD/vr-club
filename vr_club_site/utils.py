import decimal

from django.db import IntegrityError, transaction
from django.db.models import Sum
from django.contrib import messages

from .models import Booking, BookingTime, ACTUAL, Settings


COST_SESSION = 200
MAX_SESSION = 2


def get_available_slots(selected_date=None):
    _available_slots = []

    try:
        setting = Settings.objects.get(name="seats")
        setting_type = setting.variable_type
        session_seats = setting.value
        if setting_type == "int":
            session_seats = int(session_seats)
        elif setting_type == "str":
            session_seats = str(session_seats)
        elif setting_type == "decimal":
            session_seats = decimal.Decimal(session_seats)

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


def book_session(request, slots, data_to_save):
    booking = Booking(
        name=data_to_save["name"],
        email=data_to_save["email"],
        phone_number=data_to_save["phone_number"],
        people_count=data_to_save["people_count"],
        comment=data_to_save["comment"],
        price=COST_SESSION * data_to_save["people_count"] * len(slots),
    )
    booking.save()
    booking_times_to_create = [
        BookingTime(time=slot, status=ACTUAL, date=data_to_save["date"])
        for slot in slots
    ]
    try:
        with transaction.atomic():
            BookingTime.objects.bulk_create(booking_times_to_create)

            for booking_time in booking_times_to_create:
                booking.time.add(booking_time)
    except IntegrityError as e:
        messages.error(request, f"Помилка бронювання: {e}")
