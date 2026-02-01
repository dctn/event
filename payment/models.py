import uuid

from django.db import models
from django.contrib.auth.models import User

from core.models import Event,Profile,Game


# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    event = models.ForeignKey(Event,on_delete=models.SET_NULL,null=True)
    booking_id = models.CharField(max_length=255,null=True,blank=True,editable=False)
    payment_id = models.CharField(max_length=255,null=True,blank=True,editable=False)
    signature = models.CharField(max_length=255,null=True,blank=True,editable=False)
    booked_date = models.DateTimeField(auto_now_add=True)
    amount_paid = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    qr_code_id =  models.UUIDField(default=uuid.uuid4,editable=False,unique=True,blank=True)
    qr_image = models.ImageField(upload_to="qr_codes/", null=True, blank=True)

    no_of_checkin =  models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.user}"