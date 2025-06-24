from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'index.html')

def event_details(request):
    return render(request,"register_form.html")

