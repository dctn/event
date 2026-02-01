import uuid

from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.db import transaction
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
from dotenv import load_dotenv
from check_in.views import *


from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.models.customer_details import CustomerDetails
from cashfree_pg.models.order_meta import OrderMeta
load_dotenv()

x_api_version = "2023-08-01"

cashfree = Cashfree(XEnvironment=Cashfree.SANDBOX)
cashfree.XClientId = settings.CASHFREE_CLIENT_ID
cashfree.XClientSecret = settings.CASHFREE_CLIENT_SECRET


def calculate_total_charge(product_price, platform_fee_pct, razorpay_fee_pct, gst_pct):
    pre_fee = product_price * (1 + platform_fee_pct)
    razorpay_fee_rate = razorpay_fee_pct * (1 + gst_pct)
    total_charge = pre_fee / (1 - razorpay_fee_rate)
    return round(total_charge, 2)

# total = calculate_total_charge(100, 0.15, 0.03, 0.18)


# Create your views here.

##################### Razorpay ########################
# @login_required
# def proccess_order(request,event_id):
#
#     client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
#     # print(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET)
#     event = get_object_or_404(Event,event_id=event_id)
#
#     total_amount = calculate_total_charge(product_price=int(event.amount),
#                                           platform_fee_pct=float(event.commission),
#                                           razorpay_fee_pct=0.03,
#                                           gst_pct=0.18)
#     data = {
#         "amount": (int(total_amount) * 100),
#         "currency": "INR",
#         "payment_capture": "1"
#     }
#
#     razorpay_order = client.order.create(data)
#     Booking.objects.create(
#         user=request.user ,
#         amount_paid=total_amount,
#         event=event,
#         booking_id=razorpay_order['id']
#     )
#
#     if os.environ.get("ENVIRONMENT") == "production":
#         callback_url = request.build_absolute_uri(reverse(settings.RAZOR_PAY_CALLBACK_URL)).replace("http://",
#                                                                                                     "https://")
#     else:
#         callback_url = request.build_absolute_uri(reverse(settings.RAZOR_PAY_CALLBACK_URL))
#
#     return JsonResponse({
#         "order_id": razorpay_order["id"],
#         "RAZORPAY_KEY_ID": settings.RAZORPAY_KEY_ID,
#         "product_name": event.name,
#         "amount": razorpay_order["amount"],
#         "callback_url": callback_url,
#     })
#
#
# @csrf_exempt
# def payment_verify(request):
#     if "razorpay_signature" in request.POST:
#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#
#         order_id = request.POST.get("razorpay_order_id")
#         razorpay_payment_id = request.POST.get("razorpay_payment_id")
#         razorpay_signature = request.POST.get("razorpay_signature")
#
#         try:
#             client.utility.verify_payment_signature({
#                 "razorpay_order_id": order_id,
#                 "razorpay_payment_id": razorpay_payment_id,
#                 "razorpay_signature": razorpay_signature,
#             })
#
#             booking = Booking.objects.get(booking_id=order_id)
#             booking.payment_id = razorpay_payment_id
#             booking.signature = razorpay_signature
#             booking.is_paid = True
#
#             event = booking.event
#             event.current_slots -= 1
#             event.save()
#
#             booking.save()
#             messages.success(request,"your amount paid and ticket has booked")
#             return redirect("payment_success",booking.booking_id)
#
#
#
#         except razorpay.errors.SignatureVerificationError:
#             messages.error(request,"booking failed")
#             return  redirect("home")

##################### Cashfree ########################
@login_required
def process_order_cashfree(request,event_id):

    profile = get_object_or_404(Profile,user=request.user)
    event = get_object_or_404(Event, event_id=event_id)

    total_amount = calculate_total_charge(product_price=int(event.amount),
                                          platform_fee_pct=float(event.commission),
                                          razorpay_fee_pct=0.03,
                                          gst_pct=0.18)

    customer = CustomerDetails(
        customer_id=f"user_{request.user.username}",
        customer_name=profile.name,
        customer_phone=profile.phone_no,
        customer_email=request.user.email
    )

    cashfree_order_id = str(uuid.uuid4())

    if os.environ.get("ENVIRONMENT") == "production":
        callback_url = OrderMeta(
            return_url=request.build_absolute_uri(
                reverse(settings.RAZOR_PAY_CALLBACK_URL)) + "?order_id={order_id}".replace("http://",
                                                                                           "https://")
        )
    else:
        callback_url = OrderMeta(
            return_url=request.build_absolute_uri(reverse(settings.RAZOR_PAY_CALLBACK_URL)) + "?order_id={order_id}")

    data = CreateOrderRequest(
        order_id=cashfree_order_id,
        order_amount=float(total_amount),  # RUPEES
        order_currency="INR",
        customer_details=customer,
        order_meta=callback_url,
    )

    response = cashfree.PGCreateOrder(
        x_api_version,
        data,
        None,
        None
    )

    booking = Booking.objects.create(
        user=request.user,
        amount_paid=total_amount,
        event=event,
        booking_id=cashfree_order_id
    )
    booking.signature = response.data.payment_session_id
    booking.save()

    return JsonResponse({
        "payment_session_id": response.data.payment_session_id
    })

@csrf_exempt
def payment_verify_cashfree(request):
    cashfree_order_id = request.GET.get("order_id")

    # 1️⃣ Validate request
    if not cashfree_order_id:
        return render(
            request,
            "payment_success.html",
            {
                "status": "Invalid request",
                "is_success": False,
            }
        )
        # 2️⃣ Fetch order from DB

    try:
        booking = Booking.objects.get(booking_id=cashfree_order_id)
    except Booking.DoesNotExist:
        return render(
            request,
            "payment_success.html",
            {
                "status": "Order not found",
                "is_success": False,
            }
        )

        # 3️⃣ Fetch order status from Cashfree
    response = cashfree.PGFetchOrder(
        x_api_version,
        cashfree_order_id,
        None
    )

    print("Cashfree Response:", response.data)

    # 4️⃣ HARD BLOCK — payment not completed
    if response.data.order_status != "PAID":
        return render(
            request,
            "payment_success.html",
            {
                "status": "Payment not completed",
                "payment_status": response.data.order_status,
                "order_id": cashfree_order_id,
                "is_success": False,
            }
        )

    # 5️⃣ Prevent duplicate processing
    if response.data.order_status == "PAID":
        with transaction.atomic():
            booking.is_paid = True
            booking.signature = response.data.payment_session_id

            event = booking.event
            event.current_slots -= 1
            event.save()
            booking.save()
            messages.success(request, "your amount paid and ticket has booked")

            return redirect("payment_success", booking.booking_id)
    return None


def register_free_event(request,event_id,action):
    event = get_object_or_404(Event,event_id=event_id)
    profile = get_object_or_404(Profile,user=request.user)
    if action == "register":
        booking = Booking.objects.create(
            user= request.user,
            event=event,
            amount_paid=0,
            booking_id=uuid.uuid4()
        )
        event.current_slots -= 1
        event.save()

        if not booking.qr_image:
            qr_url = request.build_absolute_uri(
                reverse("checkin_ticket", args=[booking.qr_code_id])
            )
            qr_img = generate_qr_code(qr_url)
            booking.qr_image.save(
                f"qr_{booking.qr_code_id}.png",
                ContentFile(qr_img),
                save=True
            )

        messages.success(request,"your ticket slot is booked")
        return redirect("profile")
    elif action == "un_register":
        Booking.objects.get(user=request.user,event=event).delete()
        event.current_slots += 1
        event.save()
        messages.success(request,"your ticket slot is un register")
        return redirect("event_details",event_id)


def payment_success(request,booking_id):
    profile = get_object_or_404(Profile,user=request.user)


    # checking for profile details
    if not profile.phone_no or not profile.department:
        return redirect('profile_register')

    try:
        booking = get_object_or_404(Booking,booking_id=booking_id,user=request.user)
        if not booking.qr_image:
            qr_url = request.build_absolute_uri(
                reverse("checkin_ticket", args=[booking.qr_code_id])
            )
            qr_img = generate_qr_code(qr_url)
            booking.qr_image.save(
                f"qr_{booking.qr_code_id}.png",
                ContentFile(qr_img),
                save=True
            )

        context = {
            "booking": booking,
            "is_success": True,
        }

        return render(request,"payment_success.html",context)
    except:
        messages.error(request,"invalid ticket")
        return redirect("home")



