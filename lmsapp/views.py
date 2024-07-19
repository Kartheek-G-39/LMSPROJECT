from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from .models import User,Book
from .models import Userdata,BookLending
from django.urls import reverse
from django.views.decorators.http import require_GET
from django.contrib.auth import logout
from django.contrib.auth import login as loggin 
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Q 
from django.utils import timezone
from .forms import BookLendingForm

def login(request):
    if request.method=="POST":
        email = request.POST.get('mail')
        mail = email.lower()
        passw = request.POST.get('pass')
        try:
            user=User.objects.get(pk=mail)
        except:
            return HttpResponse("User Doesn't exists")
        print(user.is_superuser)
        user = authenticate(email = mail,password = passw)
        if user is not None and user.is_authenticated:
            loggin(request,user)
            userdata=None
            try:
                userdata = Userdata.objects.get(usermail = user)
            except:
                pass
            print(userdata)
            if userdata or user.is_superuser:
                return redirect(reverse('home'))
            else:
                context={
                    'user' : user,
                }
                return redirect("/aftersignup/?mail="+mail)
        else:
            context = {
                'email':email,
                'error':"Invalid Credentials"
            }
            return render(request,"login.html",context)
        # queryset = Book.objects.filter(AccessionNumber=30)
    return render(request,"login.html")
@login_required
def logout_user(request):
    logout(request)
    return redirect("/login/")

@login_required
def home(request,**kwargs):
    user = request.user
    if user.is_superuser:
        branches = ["CIVIL", "EEE", "MECH", "ECE", "CSE", "IT", "CSM", "CSO", "CIC", "AIML", "AID"]
        
        # Fetch all books
        books = Book.objects.all()
        
        # Handle search query
        query = request.GET.get('q')
        if query:
            books = books.filter(Q(AccessionNumber__icontains=query) | 
                                 Q(TitleName__icontains=query) | 
                                 Q(AuthorName__icontains=query) | 
                                 Q(SupplierName__icontains=query))
        
        # Pagination logic (as shown in Step 1)
        paginator = Paginator(books, 100)
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        
        context = {
            "branches": branches,
            "page_obj": page_obj,
            "search_query": query,  # Pass the search query to the template
        }
        return render(request, "admin_home.html", context)
    context = {
        'user':Userdata.objects.filter(usermail=user),
        'book_stu':BookLending.objects.filter(user=user)
    }
    for i in context['book_stu']:
        print(i)
    return render(request,"home.html",context)

def signup(request):
    if request.method=="POST":
        password = request.POST.get('password')
        mail = request.POST.get('roll_number')
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
        in_data=Userdata.objects.filter(usermail_id=mail)
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
        User.objects.filter(email=mail).delete()
    return HttpResponse("ok")

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
                return redirect("/login/")
            except:
                return HttpResponse("Please try again")
    return render(request,"forgot.html")

@login_required
def aftersignup(request):
    if request.method=="GET":
        mail = request.GET.get("mail").upper()
        roll_no = mail.split("@")[0]
        branches = {"01":"CIVIL","02":"EEE","03":"MECH","04":"ECE","05":"CSE","12":"IT","42":"CSM","49":"CSO","47":"CIC","61":"AIML","54":"AID"}
        branch = branches[roll_no[6:8]]
        try:
            libraryid = Userdata.objects.get(usermail=mail).libraryid
        except:
            libraryid=None
        if libraryid:
            return render(request,"student_after_signup.html",{"roll_no":roll_no,"branch":branch,"libraryid":libraryid})
        else:
            return render(request,"student_after_signup.html",{"roll_no":roll_no,"branch":branch})
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
        exists = Userdata.objects.filter(usermail=user)
        if not exists:
            Userdata.objects.create(usermail=user,rollnumber=roll_no,gender=gender,section=sec,name=name,libraryid=libraryid,branch=branch)
        else:
            exists.delete()
            Userdata.objects.create(usermail=user,rollnumber=roll_no,gender=gender,section=sec,name=name,libraryid=libraryid,branch=branch)
        context = {
        'user':Userdata.objects.filter(usermail=user).first(),
        'book_stu':BookLending.objects.filter(user=user)
            }
        return render(request,"home.html",context=context)
    return render(request,"aftersignup.html")

@login_required
def branch_students(request,branch):
    students = Userdata.objects.filter(branch__iexact = branch)
    query = request.GET.get('q')
    academic_years = Userdata.objects.values_list('academic_year', flat=True).distinct()
    if query:
        students = students.filter(Q(rollnumber__icontains=query) | 
                                Q(name__icontains=query) | 
                                Q(section__icontains=query) | 
                                Q(id__icontains=query))
    context={
        "students": students,
        "branch":branch,
        "academic_years":academic_years
    }
    return render(request,"branch_students.html",context)

@login_required
def student_details(request,id):
    user = Userdata.objects.get(id=id)
    if request.method == "POST":
        form = BookLendingForm(request.POST)
        if form.is_valid():
            book_lending = form.save(commit=False)
            book_lending.user = user.usermail
            book_lending.save()
            return redirect('student_details', id=id)
    form = BookLendingForm()
    context = {
        'user':user,
        'book_stu':BookLending.objects.filter(user=user.usermail).order_by('-lending_time'),
        'form':form
    }
    return render(request,"home.html",context)

@require_GET
def book_search(request):
    term = request.GET.get('term', '')
    books = Book.objects.filter(TitleName__icontains=term) | Book.objects.filter(AccessionNumber__icontains=term)
    results = []
    for book in books:
        results.append({
            'id': book.id,
            'text': f"{book.TitleName} - {book.AccessionNumber}"
        })
    return JsonResponse({'results': results})

@login_required
def book_details(request,id):
    book = Book.objects.get(pk=id)
    borrowers = book.lendinginfo.all()
    context={
        'book':book,
        'borrowers' : borrowers
    }

    return render(request,"book_details.html",context)


def update_return_date(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        print(book_id)
        return_date = request.POST.get('return_date')
        if book_id and return_date:
            book_lending = get_object_or_404(BookLending, pk=book_id)
            book_lending.return_time = timezone.datetime.strptime(return_date, '%Y-%m-%d')
            book_lending.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


@csrf_exempt
def reset_verify_email(request):
    if request.method == "POST":
        mail = request.POST.get("mail")
        user_exists = User.objects.filter(email=mail).exists()
        return JsonResponse({"message": "exists" if user_exists else "not_exists"})

@csrf_exempt
def reset_clear_otp(request):
    if request.method == "POST":
        mail = request.POST.get("mail")
        # Clear OTP or perform necessary actions
        return JsonResponse({"status": "success"})

def reset_password(request):
    if request.method == "POST":
        mail = request.POST.get("mail")
        new_password = request.POST.get("password")
        try:
            user = User.objects.get(email=mail)
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('password_reset_done')
        except User.DoesNotExist:
            return redirect('reset_password')
    return render(request, 'reset_password.html')

def password_reset_done(request):
    return render(request, 'password_reset_done.html')


@csrf_exempt
def verify_email(request):
    if request.method == "POST":
        mail = request.POST.get("mail")
        # Perform your check to see if the email exists in the database
        user_exists = False  # Replace with actual check
        return JsonResponse({"message": "exists" if user_exists else "does_not_exist"})

@csrf_exempt
def clear_otp(request):
    if request.method == "POST":
        mail = request.POST.get("mail")
        # Clear OTP or perform necessary actions
        return JsonResponse({"status": "success"})

def forgot_password(request):
    if request.method == "POST":
        # Handle form submission if needed
        return redirect('password_reset_done')
    return render(request, 'forgot_password.html')

def password_reset_done(request):
    return render(request, 'password_reset_done.html')