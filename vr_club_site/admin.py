from django.contrib import admin

from .models import BookingTime, Booking, SessionSeats

# Register your models here.


admin.site.register(BookingTime)
admin.site.register(Booking)
admin.site.register(SessionSeats)
