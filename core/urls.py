from django.urls import path
from .views import *
urlpatterns = [
    path("",home,name="home"),
    path("event/",event_details,name="event_details"),
    path("profile/",profile,name="profile"),
]