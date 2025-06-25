from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class EventChoices(models.TextChoices):
    TECH = 'tech', 'Tech Event'
    NON_TECH = 'non_tech', 'Non Tech Event'
    BOTH = 'both', 'Both'

class GenderChoice(models.TextChoices):
   MALE = 'male', 'Male'
   FEMALE = 'female', 'Female'

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    email = models.EmailField()
    phone_no = models.
    name = models.CharField(max_length=255)
    college_name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    interested_event = models.CharField(choices=EventChoices.choices,default=EventChoices.BOTH,max_length=100)
    bio = models.TextField()
    gender = models.CharField(choices=GenderChoice.choices,max_length=100)
    img = models.ImageField(upload_to="profile_img/")

    def __str__(self):
        return f"{self.user}: {self.name}"