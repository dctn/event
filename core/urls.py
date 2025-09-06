from django.urls import path
from .views import *
urlpatterns = [
    path("",home,name="home"),
    path("event/",event_details,name="event_details"),
    path("profile/",profile,name="profile"),
    path("profile_register/",profile_form,name="profile_register"),
    path("event_registation/",event_registation,name="event_registation")
]
