import calendar
import decimal
from datetime import datetime, date

from django.db import IntegrityError, transaction
from django.db.models import F, Sum, Case, When, Value, IntegerField
from django.db.models.functions import Greatest, Least
from django.contrib import messages

from .models import Booking, BookingTime, ACTUAL, Settings


COST_SESSION = 200
MAX_SESSION = 2


def get_price(date):
    day_of_week = date.weekday()
    if day_of_week >= 5:
        price = get_weekend_price()
    else:
        price = get_weekday_price()
    return price


def get_session_seats():
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

    return session_seats


def get_weekday_price():
    try:
        setting = Settings.objects.get(name="weekdays")
        setting_type = setting.variable_type
        weekend_price = setting.value
        if setting_type == "int":
            weekend_price = int(weekend_price)
        elif setting_type == "str":
            weekend_price = str(weekend_price)
        elif setting_type == "decimal":
            weekend_price = decimal.Decimal(weekend_price)
    except Settings.DoesNotExist:
        weekend_price = 300
    return weekend_price


def get_weekend_price():
    try:
        setting = Settings.objects.get(name="weekend")
        setting_type = setting.variable_type
        weekday_price = setting.value
        if setting_type == "int":
            weekday_price = int(weekday_price)
        elif setting_type == "str":
            weekday_price = str(weekday_price)
        elif setting_type == "decimal":
            weekday_price = decimal.Decimal(weekday_price)
    except Settings.DoesNotExist:
        weekday_price = 500
    return weekday_price


def get_available_slots_for_month(currentYear=None, currentMonth=None):
    _available_slots = []
    session_seats = get_session_seats()
    days_in_month = calendar.monthrange(int(currentYear), int(currentMonth))[1]

    time_choice_to_index = {
        choice[0]: index for index, choice in enumerate(BookingTime.TIME_CHOICES)
    }

    all_time_choices = [choice[0] for choice in BookingTime.TIME_CHOICES]

    daily_available_slots = {
        day: [session_seats] * len(all_time_choices)
        for day in range(1, days_in_month + 1)
    }

    bookings = (
        Booking.objects.filter(
            time__status=ACTUAL,
            time__date__year=currentYear,
            time__date__month=currentMonth,
        )
        .annotate(
            time_index=Case(
                *[
                    When(time__time=choice, then=Value(index))
                    for choice, index in time_choice_to_index.items()
                ],
                output_field=IntegerField(),
            )
        )
        .values("time__date", "time_index")
        .annotate(total_people=Sum("people_count"))
    )

    for booking in bookings:
        day = booking["time__date"].day
        time_index = booking["time_index"]
        total_people = booking["total_people"]
        daily_available_slots[day][time_index] -= total_people

    for day, available_slots in daily_available_slots.items():
        selected_date = date(int(currentYear), int(currentMonth), day)
        total_available_slots = sum(max(slot, 0) for slot in available_slots)
        _available_slots.append(
            {
                "date": selected_date.strftime("%Y-%m-%d"),
                "available_slots": total_available_slots,
            }
        )

    return _available_slots


def get_available_slots(selected_date=None):
    _available_slots = []
    session_seats = get_session_seats()

    for x in BookingTime.TIME_CHOICES:
        try:
            slot = (
                Booking.objects.filter(
                    time__status=ACTUAL, time__time=x[0], time__date=selected_date
                ).aggregate(
                    total_people=Least(Greatest(Sum("people_count"), 0), session_seats)
                )[
                    "total_people"
                ]
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
        price=get_price(data_to_save["date"])
        * data_to_save["people_count"]
        * len(slots),
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
