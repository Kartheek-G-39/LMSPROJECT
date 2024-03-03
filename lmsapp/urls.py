from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('home',views.home),
    path('',views.home),
    path('accounts/login/',views.login),
    path('login',views.login),
    path('signup',views.signup),
    path('logout',views.logout_user),
    path('aftersignup/',views.aftersignup),
    path('register',views.register),
    path('aboutus',views.aboutus),
    path('verify',views.verify),
    path('forgot',views.forgot),
    path('clear',views.clear),
    
]