from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
import qrcode
from io import BytesIO
from payment.models import Booking
from django.http import FileResponse, HttpResponse
from core.models import Event, Profile
from django.contrib import messages

# Create your views here.
def download_img(request,event_id):
    event = get_object_or_404(Event, event_id=event_id)
    img_path = event.img.path

    return FileResponse(
        img_path,
        as_attachment=True,
        filename=f"{event.name}.png",
        content_type="image/png"
    )

def generate_qr_code(url_text):
    qr = qrcode.make(url_text)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return buffer.getvalue()



def download_qr(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)

    qr_path = booking.qr_image.path  # absolute file path
    file = open(qr_path, "rb")

    return FileResponse(
        file,
        as_attachment=True,
        filename=f"ticket_qr_{booking_id}.png",
        content_type="image/png"
    )

@login_required
def checkin_ticket(request, qr_id):
    # Get the booking
    try:
        booking = Booking.objects.get(qr_code_id=qr_id)
    except Booking.DoesNotExist:
        return HttpResponse("INVALID_TICKET")

    # Get event
    event = booking.event

    # Get current user's profile
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return HttpResponse("INVALID_TICKET")

    # SECURITY CHECK — only event owner can scan
    if event.created_by != profile:
        return HttpResponse("NOT_ALLOWED")

    # Must be paid ticket
    if event.event_type == "paid" and not booking.is_paid:
        return HttpResponse("INVALID_TICKET")

    # Already scanned
    if booking.is_checked_in:
        return HttpResponse("ALREADY_CHECKED_IN")

    # Mark as checked in
    booking.is_checked_in = True
    booking.save()

    return HttpResponse("CHECKIN_SUCCESS")

@login_required
def qr_scan(request,event_id):
    event = get_object_or_404(Event, event_id=event_id)
    profile = Profile.objects.get(user=request.user)
    if event.created_by == profile:
        return render(request,"scan_qr.html")
    else:
        messages.error(request,"You are not authorized to scan")
        return redirect("home")