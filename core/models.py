import uuid

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models import Model


# Create your models here.
class EventChoices(models.TextChoices):
    TECH = 'tech', 'Tech Event'
    NON_TECH = 'non_tech', 'Non Tech Event'
    BOTH = 'both', 'Both'

class GenderChoice(models.TextChoices):
   MALE = 'male', 'Male'
   FEMALE = 'female', 'Female'

phone_validator = RegexValidator(
    regex=r'^[6-9]\d{9}$',
    message="Enter a valid 10-digit Indian mobile number"
)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    email = models.EmailField()
    phone_no = models.CharField(max_length=10,validators=[phone_validator],null=True)
    name = models.CharField(max_length=255)
    college_name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    interested_event = models.CharField(choices=EventChoices.choices,default=EventChoices.BOTH,max_length=100)
    bio = models.TextField()
    gender = models.CharField(choices=GenderChoice.choices,max_length=100,default="null")
    img = models.ImageField(upload_to="profile_img/",default="logo_dot_sm.png",null=True,blank=True)

    def __str__(self):
        return f"{self.user}: {self.name}"


class EventTypeChoice(models.TextChoices):
    FREE = 'free', 'Free Event'
    PAID = 'paid', 'Paid Event'


class Event(models.Model):
    event_id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=10,validators=[phone_validator])
    password= models.CharField(max_length=255)
    club_name = models.CharField(max_length=255)
    no_of_slots = models.IntegerField()
    event_details = models.TextField()

    # event Images
    img = models.ImageField(upload_to="event_img/",default="logo_dot_sm.png")
    img_2 = models.ImageField(upload_to="event_img/",null=True,blank=True)
    img_3 = models.ImageField(upload_to="event_img/",null=True,blank=True)
    img_4 = models.ImageField(upload_to="event_img/",null=True,blank=True)



    # volunteer Info
    volunteer_name = models.CharField(max_length=255)
    volunteer_phone_no = models.CharField(max_length=10,validators=[phone_validator])
    volunteer_position = models.CharField(max_length=255)

    # Event Info
    registion_opening_date = models.DateField()
    registion_closing_date = models.DateField()
    registion_on_date = models.DateField()
    event_starting_time = models.TimeField()

    # event Type
    event_type = models.CharField(choices=EventTypeChoice.choices,blank=False,null=False,default=EventTypeChoice.PAID)


    def __str__(self):
        return f"{self.name}"

