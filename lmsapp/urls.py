from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('',views.home,name = "home"),
    path('accounts/login/',views.login),
    path('login/',views.login,name = "login"),
    path('signup',views.signup,name = "signup"),
    path('logout',views.logout_user,name ="logout"),
    path('aftersignup/',views.aftersignup,name="save_student_details"),
    path('register',views.register),
    path("branch_students/<str:branch>",views.branch_students,name="branch_students"),
    path('aboutus',views.aboutus,name = "aboutus"),
    path('verify',views.verify),
    path('forgot',views.forgot,name = "forgot"),
    path('clear',views.clear),
    path("student_details/<str:id>/",views.student_details,name="student_details"),
    path("book_details/<str:id>/",views.book_details,name="book_details"),
    path('book-search/', views.book_search, name='book_search'),
    path('update-return-date/', views.update_return_date, name='update_return_date'),
    path('reset/verify/', views.reset_verify_email, name='reset_verify_email'),
    path('reset/clear/', views.reset_clear_otp, name='reset_clear_otp'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),
    path('verify/', views.verify_email, name='verify_email'),
    path('clear/', views.clear_otp, name='clear_otp'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),
]
    
