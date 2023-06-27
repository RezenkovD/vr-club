from django.contrib import admin

from .models import BookingTime, Booking

# Register your models here.


admin.site.register(BookingTime)
admin.site.register(Booking)
