from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

ADMINISTRATOR = "AD"
OWNER = "OW"
EMPLOYEE = "EM"
VISITOR = "VI"


class Profile(models.Model):
    ROLE_CHOICES = (
        (ADMINISTRATOR, "Administrator"),
        (OWNER, "Owner"),
        (EMPLOYEE, "Employee"),
        (VISITOR, "Visitor"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    role = models.CharField(
        max_length=2, choices=ROLE_CHOICES, null=False, default=VISITOR
    )

    def __str__(self):
        return "{0} | {1}".format(self.user.username, self.role)
