from django.contrib import admin

from .models import BookingTime, Booking, Settings

# Register your models here.


admin.site.register(BookingTime)
admin.site.register(Booking)
admin.site.register(Settings)
