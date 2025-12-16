from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings

from payment.models import Booking
from .forms import *
from .models import *


def calculate_total_charge(product_price, platform_fee_pct, razorpay_fee_pct, gst_pct):
    pre_fee = product_price * (1 + platform_fee_pct)
    platform_fee = platform_fee_pct * product_price
    razorpay_fee_rate = razorpay_fee_pct * (1 + gst_pct)
    total_charge = pre_fee / (1 - razorpay_fee_rate)
    razorpay_fee = total_charge * razorpay_fee_rate
    return {
        "platform_fee": round(platform_fee, 2),
        "razorpay_fee_rate": round(razorpay_fee, 2),
        "total_charge": round(total_charge, 2)
    }


# Create your views here.
def home(request):
    all_events = Event.objects.all()
    context = {
        "all_events": all_events
    }
    return render(request, 'index.html', context)


@login_required
def event_details(request, event_id):

    event = get_object_or_404(Event, event_id=event_id)
    is_owner = False
    is_already_registered = False
    profile = Profile.objects.get(user=request.user)

    # checking for profile details
    if not profile.phone_no or not profile.department or profile.name or profile.college_name:
        return redirect('profile_register')

    total_amount = calculate_total_charge(product_price=int(event.amount),
                                          platform_fee_pct=float(event.commission),
                                          razorpay_fee_pct=0.03,
                                          gst_pct=0.18)

    if profile == event.created_by:
        is_owner = True

    # print(Booking.objects.get(user=profile,event=event,is_paid=True))

    try:
        if event.event_type == "paid":
            is_paid = Booking.objects.get(user=profile, event=event, is_paid=True)
            if is_paid:
                is_already_registered = True
        elif event.event_type == "free":
            if Booking.objects.get(event=event_id, user=profile):
                is_already_registered = True
    except:
        pass

    context = {
        'event': event,
        "is_owner": is_owner,
        "is_already_registered": is_already_registered,
        "platform": total_amount["platform_fee"],
        "razorpay_fee_rate": total_amount["razorpay_fee_rate"],
        "total_charge": total_amount["total_charge"],
    }

    return render(request, "event_details.html", context)


def profile(request):
    user_profile = Profile.objects.get(user=request.user)
    user_event = Booking.objects.filter(user=user_profile)
    valid_bookings = user_event.filter(
        Q(is_paid=True, event__event_type="paid", ) |
        Q(is_paid=False, event__event_type="free")
    )

    context = {
        'profile': user_profile,
        'all_booking': valid_bookings,
        "registered_count": valid_bookings.count(),
        "attended_count": valid_bookings.filter(is_checked_in=True).count(),

    }
    return render(request, "profile.html", context)


def profile_form(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            profile_save = form.save()
            return redirect("profile")

    else:
        form = ProfileForm(instance=user_profile)
    context = {
        "form": form
    }
    return render(request, "register_form.html", context)


### Event view


def event_registation(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            profile = get_object_or_404(Profile, user=request.user)
            event.created_by = profile
            event.current_slots = event.no_of_slots
            event.save()
            messages.success(request, "Your event is Created")
            return redirect("event_details", event.event_id)
    else:
        form = EventForm()
    context = {
        "form": form
    }
    return render(request, "event_register.html", context)


def event_update(request, event_id):
    event = get_object_or_404(Event, event_id=event_id)
    profile = Profile.objects.get(user=request.user)
    if profile == event.created_by:
        if request.method == "POST":
            form = EventForm(request.POST, request.FILES, instance=event)
            if form.is_valid():
                form.save()
                messages.success(request, "Your event Details is updated")
                return redirect("event_details", event_id)
        else:
            form = EventForm(instance=event)

        context = {
            "form": form,
        }
        return render(request, "event_register.html", context)
    else:
        messages.error(request, "Not having access")
        return redirect("home")

def cgpa(request):
    return render(request, "cgpa.html")