from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from .models import User,userdata
from .retrival import auth
from django.contrib.auth import logout
from django.contrib.auth import login as loggin
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request,"home.html")
def login(request):
    if request.method=="POST":
        mail = request.POST.get('mail')
        mail=mail.lower()
        passw = request.POST.get('pass')
        try:
            user=User.objects.get(pk=mail)
        except:
            return HttpResponse("User does not exists")
        if auth(mail,passw):
            loggin(request,user)
            return redirect("/aftersignup/?mail="+mail)
        else:
            return HttpResponse("incorrect password")
    return render(request,"login.html")
def logout_user(request):
    logout(request)
    return redirect("/login")
def signup(request):
    if request.method=="POST":
        password = request.POST.get('passw')
        mail = request.POST.get('mail')
        mail=mail.lower()
        if password:
            data=User.objects.create_user(mail,password)
            data.save()
            try:
                user=User.objects.get(pk=mail)
            except:
                pass
            loggin(request,user)
            return redirect("/aftersignup/?mail="+mail)
    return render(request,"signup.html")
@csrf_exempt
def verify(request):
    if request.method == "POST":
        mail=request.POST.get('mail')
        mail=mail.lower()
        exists,in_data=False,False
        exists=User.objects.filter(email__iexact=mail)
        in_data=userdata.objects.filter(usermail_id=mail)
        if not exists:
            return JsonResponse({"message":"ok"})
        elif not in_data:
            return JsonResponse({"message":"nodata"})
        else:
            return JsonResponse({"message":"exists"})
    return HttpResponse("inside verify view")
@csrf_exempt
def clear(request):
    if request.method=="POST":
        mail = request.POST.get('mail')
        print(mail)
        User.objects.filter(email=mail).delete()
def aboutus(request):
        return render(request,"About_US.html")
def register(request):
    return render(request,"first_login.html")
def forgot(request):
    if request.method=="POST":
        password = request.POST.get('passw')
        mail = request.POST.get('mail')
        mail=mail.lower()
        if password:
            try:
                user=User.objects.update_password(mail,password)
                return redirect("/login")
            except:
                return HttpResponse("Please try again")
    return render(request,"forgot.html")
def aftersignup(request):
    branches = {"01":"CIVIL","02":"EEE","03":"MECH","04":"ECE","05":"CSE","12":"IT","42":"CSM","49":"CSO","47":"CIC","61":"AIML","54":"AID"}
    if request.method=="GET":
        mail = request.GET.get("mail").upper()
        roll_no = mail.split("@")[0]
        branch = branches[roll_no[6:8]]
        try:
            libraryid = userdata.objects.get(usermail=mail).libraryid
        except:
            libraryid=None
        if libraryid:
            return render(request,"aftersignup.html",{"roll_no":roll_no,"branch":branch,"libraryid":libraryid})
        else:
            return render(request,"aftersignup.html",{"roll_no":roll_no,"branch":branch})
    elif request.method=="POST":
        roll_no = request.POST.get("rollnum")
        mail = roll_no+"@vvit.net"
        branch = branches[roll_no[6:8]]
        option = request.POST.get("radio")
        
        if option == "male":
            gender = "👨(M)"
        elif option == "female":
            gender = "👧(F)"
        sec = request.POST.get("section")
        name = request.POST.get("name")
        libraryid = request.POST.get("libraryid")
        user=User.objects.get(email=mail.lower())
        exists = False
        exists = userdata.objects.filter(usermail=user)
        if not exists:
            userdata.objects.create(usermail=user,rollnumber=roll_no,gender=gender,section=sec,name=name,libraryid=libraryid,branch=branch)
        else:
            exists.delete()
            userdata.objects.create(usermail=user,rollnumber=roll_no,gender=gender,section=sec,name=name,libraryid=libraryid,branch=branch)
        return render(request,"firstpage.html")
    return render(request,"aftersignup.html")