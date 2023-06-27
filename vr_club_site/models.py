from django.contrib.auth.models import User
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
        (f"{hour}-{hour + 1}", f"{hour}.00-{hour + 1}.00") for hour in range(13, 21)
    ]
    time = models.CharField(max_length=5, choices=TIME_CHOICES, null=False)
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, null=False, default=ACTUAL
    )

    def __str__(self):
        return "{0} | {1}".format(self.time, self.status)


class Booking(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    comment = models.CharField(max_length=128, null=True)
    time = models.ManyToManyField(BookingTime)

    def __str__(self):
        return self.user.username
