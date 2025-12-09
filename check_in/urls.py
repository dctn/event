from django.urls import path
from . import views
urlpatterns = [
    path("check_in/<qr_id>",views.checkin_ticket,name="checkin_ticket"),
    path("download-qr/<str:booking_id>/", views.download_qr, name="download_qr"),
    path("qr_scanner/<event_id>/",views.qr_scan,name="qr_scan"),
    path("download_img/<event_id>/",views.download_img,name="download_img"),
]