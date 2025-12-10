from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
import razorpay
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import os
from core.models import Event, Profile
from .models import Booking

from check_in.views import *

def calculate_total_charge(product_price, platform_fee_pct, razorpay_fee_pct, gst_pct):
    pre_fee = product_price * (1 + platform_fee_pct)
    razorpay_fee_rate = razorpay_fee_pct * (1 + gst_pct)
    total_charge = pre_fee / (1 - razorpay_fee_rate)
    return round(total_charge, 2)

# total = calculate_total_charge(100, 0.15, 0.03, 0.18)


# Create your views here.

@login_required
def proccess_order(request,event_id):

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

    event = get_object_or_404(Event,event_id=event_id)
    profile = get_object_or_404(Profile,user=request.user)

    total_amount = calculate_total_charge(product_price=int(event.amount),
                                          platform_fee_pct=float(event.commission),
                                          razorpay_fee_pct=0.03,
                                          gst_pct=0.18)
    data = {
        "amount": (int(total_amount) * 100),
        "currency": "INR",
        "payment_capture": "1"
    }

    razorpay_order = client.order.create(data)
    Booking.objects.create(
        user=profile ,
        amount_paid=total_amount,
        event=event,
        booking_id=razorpay_order['id']
    )

    if os.environ.get("ENVIRONMENT") == "production":
        callback_url = request.build_absolute_uri(reverse(settings.RAZOR_PAY_CALLBACK_URL)).replace("http://",
                                                                                                    "https://")
    else:
        callback_url = request.build_absolute_uri(reverse(settings.RAZOR_PAY_CALLBACK_URL))

    return JsonResponse({
        "order_id": razorpay_order["id"],
        "RAZORPAY_KEY_ID": settings.RAZORPAY_KEY_ID,
        "product_name": event.name,
        "amount": razorpay_order["amount"],
        "callback_url": callback_url,
    })


@csrf_exempt
def payment_verify(request):
    if "razorpay_signature" in request.POST:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        order_id = request.POST.get("razorpay_order_id")
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_signature = request.POST.get("razorpay_signature")

        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            })

            booking = Booking.objects.get(booking_id=order_id)
            booking.payment_id = razorpay_payment_id
            booking.signature = razorpay_signature
            booking.is_paid = True

            event = booking.event
            event.current_slots -= 1
            event.save()

            booking.save()
            messages.success(request,"your amount paid and ticket has booked")
            return redirect("payment_success",booking.booking_id)



        except razorpay.errors.SignatureVerificationError:
            messages.error(request,"booking failed")
            return  redirect("home")


def register_free_event(request,event_id,action):
    event = get_object_or_404(Event,event_id=event_id)
    profile = get_object_or_404(Profile,user=request.user)
    if action == "register":
        Booking.objects.create(
            user= profile,
            event=event,
            amount_paid=0,
        )
        event.current_slots -= 1
        messages.success(request,"your ticket slot is booked")
        return redirect("profile")
    elif action == "un_register":
        Booking.objects.get(user=profile,event=event).delete()
        event.current_slots += 1
        messages.success(request,"your ticket slot is un register")
        return redirect("event_details",event_id)

def payment_success(request,booking_id):
    profile = get_object_or_404(Profile,user=request.user)
    try:
        booking = get_object_or_404(Booking,booking_id=booking_id,user=profile)
        if not booking.qr_image:
            qr_url = request.build_absolute_uri(
                reverse("checkin_ticket", args=[booking.qr_code_id])
            )
            qr_img = generate_qr_code(qr_url)
            booking.qr_image.save(
                f"qr_{booking.qr_code_id}",
                ContentFile(qr_img),
                save=True
            )

        context = {
            "booking": booking,
        }

        return render(request,"payment_success.html",context)
    except:
        messages.error(request,"invalid ticket")
        return redirect("home")



