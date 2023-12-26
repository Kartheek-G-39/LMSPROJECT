from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request,"home.html")
def login(request):
    return render(request,"login.html")
def signup(request):
    return render(request,"login.html")
def aboutus(request):
    return render(request,"about_us.html")

def dashboard(request):
    return render(request,"user_profile.html")
# Create your views here.
