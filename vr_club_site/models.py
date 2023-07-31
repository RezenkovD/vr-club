from datetime import date

from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

ACTUAL = "AL"
OUTDATED = "OD"


class BookingTime(models.Model):
    STATUS_CHOICES = (
        (ACTUAL, "Actual"),
        (OUTDATED, "Outdated"),
    )
    TIME_CHOICES = [
        (f"{hour}-{hour + 1}", f"{hour}.00-{hour + 1}.00") for hour in range(12, 22)
    ]

    time = models.CharField(max_length=5, choices=TIME_CHOICES, null=False)
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, null=False, default=ACTUAL
    )
    date = models.DateField(default=date.today)

    def __str__(self):
        return "{0} | {1}".format(self.time, self.status)


class Booking(models.Model):
    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
    )
    name = models.CharField(max_length=32, null=False, default="vrclub")
    email = models.EmailField(max_length=64, null=False, default="vrclub@gmail.com")
    phone_number = PhoneNumberField(
        null=True, blank=True, unique=False, default="+380000000000"
    )
    comment = models.CharField(max_length=256, null=True)
    number_of_people = models.PositiveIntegerField(default=0)  # TODO: rename to people_count
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    time = models.ManyToManyField(BookingTime)

    def __str__(self):
        return self.email + " " + str(self.price)


class SessionSeats(models.Model):  # TODO: Переформатувати таблицю в Settings table
    number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "Сесійних місць: " + str(self.number)
