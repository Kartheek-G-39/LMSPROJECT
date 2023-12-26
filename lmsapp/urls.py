from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('home',views.home),
    path('',views.home),
    path('login',views.login),
    path('signup',views.signup),
    path('aboutus',views.aboutus),
    path('dashboard',views.dashboard),
    #path('forgot_password',views.forgotpass),
    #path('forgot_id',views.forgotid),
    
]