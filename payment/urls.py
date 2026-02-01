from django.urls import path
from .views import *
urlpatterns = [
    # path("proccess_order/<event_id>/",proccess_order,name="proccess_order"),
    path("proccess_order/<event_id>/",process_order_cashfree,name="process_order_cashfree"),
    # path("payment_verify/",payment_verify,name="payment_verify"),
    path("payment_verify/",payment_verify_cashfree,name="payment_verify"),
    path("register_free_event/<event_id>/<action>/", register_free_event, name="register_free_event"),
    path("payment_success/<booking_id>/",payment_success,name="payment_success"),
]