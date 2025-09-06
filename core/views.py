from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
from .models import *
# Create your views here.
def home(request):
    return render(request,'index.html')

def event_details(request):
    return render(request,"event_details.html")

def profile(request):
    user_profile = Profile.objects.get(user=request.user)
    context = {
    'profile':user_profile,
    }
    return render(request, "profile.html", context)


@login_required
def profile_form(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST,request.FILES,instance=user_profile)
        if form.is_valid():
            profile_save = form.save()
            return redirect("profile")

    else:
        form = ProfileForm(instance=user_profile)
    context = {
        "form":form
    }
    return render(request,"register_form.html",context)


### Event view

def event_registation(request):
    form = EventForm()

    context = {
        "form":form
    }
    return render(request,"event_register.html",context)
