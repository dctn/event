from django.contrib import admin
from .models import Booking
# Register your models here.
admin.site.register(Booking)

class BookingAdmin(admin.ModelAdmin):
    model = Booking
    readonly_fields = ["booking_id","signature","payment_id"]

admin.site.unregister(Booking)
admin.site.register(Booking,BookingAdmin)


