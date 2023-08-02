from datetime import date

from django.db import models

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
        return "{0} | {1} | {2}".format(self.date, self.time, self.status)


class Booking(models.Model):
    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
    )
    name = models.CharField(max_length=32, null=False, default="vrclub")
    email = models.EmailField(max_length=64, null=False, default="vrclub@gmail.com")
    phone_number = models.CharField(
        max_length=20, null=True, blank=True, default="+380000000000"
    )
    comment = models.CharField(max_length=256, null=True)
    people_count = models.PositiveIntegerField(
        default=0
    )  # TODO: rename to people_count
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    time = models.ManyToManyField(BookingTime)

    def __str__(self):
        return "{0} | {1}".format(self.email, self.price)


class Settings(models.Model):
    VARIABLE_TYPES = (
        ("str", "String"),
        ("int", "Integer"),
        ("decimal", "Decimal"),
        ("bool", "Boolean"),
    )

    name = models.CharField(max_length=100, unique=True)
    variable_type = models.CharField(max_length=10, choices=VARIABLE_TYPES)
    value = models.TextField()

    def __str__(self):
        return f"{self.name}:{self.variable_type} = {self.value}"
