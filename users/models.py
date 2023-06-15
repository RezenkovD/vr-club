from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class User(models.Model):
    email = models.EmailField(max_length=256, null=False, unique=True)
    first_name = models.CharField(max_length=32, null=False)
    last_name = models.CharField(max_length=32, null=False)
    password = models.CharField(max_length=256, null=False)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)

    def __str__(self):
        return "{0} {1}".format(self.last_name, self.first_name)
