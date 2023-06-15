from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Role(models.Model):
    title = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=64)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    roles = models.ManyToManyField(Role)

    def __str__(self):
        return self.user.username
