from django.db import models
from django.contrib.auth.models import User

from core.models import Event,Profile


# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True)
    event = models.ForeignKey(Event,on_delete=models.SET_NULL,null=True)
    booking_id = models.CharField(max_length=255,null=True,blank=True,editable=False)
    payment_id = models.CharField(max_length=255,null=True,blank=True,editable=False)
    signature = models.CharField(max_length=255,null=True,blank=True,editable=False)
    booked_date = models.DateTimeField(auto_now_add=True)
    amount_paid = models.IntegerField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"