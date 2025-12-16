from django.urls import path
from .views import *
urlpatterns = [
    path("",home,name="home"),
    path("event/<event_id>",event_details,name="event_details"),
    path("profile/",profile,name="profile"),
    path("profile_register/",profile_form,name="profile_register"),
    path("profile_register<event_id>//",profile_form,name="profile_register_with_event"),
    path("event_registation/",event_registation,name="event_registation"),
    path("event_update/<event_id>/", event_update, name="event_update"),
    path("CGPA_Calculator/", cgpa, name="CGPA_Calculator"),
]
