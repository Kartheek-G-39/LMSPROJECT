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
    path("student_details/<str:id>",views.student_details,name="student_details"),
    path('book-search/', views.book_search, name='book_search'),
    
]