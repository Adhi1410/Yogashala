from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
import random
from django.contrib.auth import logout
from datetime import date, datetime,timedelta

def check_admin(user):
    return user.is_superuser


def check_student(user):
    return (not user.is_staff)


def check_teacher(user):
    return user.is_staff


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if (len(username) == 0 or len(password) == 0):
            messages.info(request, 'Do not leave Credentials empty!')
            return HttpResponseRedirect('/login/')
        else:
            if not User.objects.filter(username=username).exists():
                messages.info(request, 'Username does not exist.')
                return HttpResponseRedirect('/login/')
            elif user is not None:
                if check_admin(user):
                    auth.login(request, user)
                    return HttpResponseRedirect('/admin_home/')
                elif check_teacher(user):
                    auth.login(request, user)
                    return HttpResponseRedirect('/TeacherHome/')
                elif check_student(user):
                    auth.login(request, user)
                    return HttpResponseRedirect('/user_dashboard/')
            else:
                messages.info(request, 'Invalid Credentials')
                return redirect('/login/')
    return render(request, 'first_app/login.html')


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = 1
        username = request.POST['username']
        email = request.POST['email']
        pwd1 = request.POST['pwd1']
        pwd2 = request.POST['pwd2']
        if (len(username) == 0 or len(email) == 0 or len(pwd1) == 0 or len(pwd2) == 0 or len(first_name) == 0):
            messages.info(request, "Don't leave the credentials empty!")
            return redirect('/signup/')
        if (pwd1 == pwd2):
            if (User.objects.filter(email=email).exists() and User.objects.filter(username=username).exists()):
                messages.info(request, "Username and email already exists!")
                return redirect('/signup/')
            elif User.objects.filter(email=email).exists():  # checks whether email is already in use
                messages.info(request, "This email already exists!")
                return redirect('/signup/')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists!")
                return redirect('/signup/')
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                                email=email, password=pwd1)
                user.save()
                return redirect('/login/')
        else:
            messages.info(request, 'Passwords are not same')
            return redirect('/signup/')

    return render(request, 'first_app/signup.html')


def add_student(request):
    if not (request.user.is_superuser):
        return render(request, 'first_app/indexH.html')
    data = addcourse.objects.all()
    context = {'d':data }

    if request.method == 'POST':
        first_name = request.POST['first_name']
        username = request.POST['username']
        email = request.POST['email']
        pwd1 = request.POST['pwd1']
        pwd2 = request.POST['pwd2']
        ids = request.POST.getlist('ids')
        if (len(username) == 0 or len(email) == 0 or len(pwd1) == 0 or len(pwd2) == 0 or len(first_name) == 0):
            messages.info(request, "Don't leave the credentials empty!")
            return redirect('/add_student/')
        if (pwd1 == pwd2):
            if (User.objects.filter(email=email).exists() and User.objects.filter(username=username).exists()):
                print(1)
                messages.info(request, "Username and email already exists!")
                return redirect('/add_student/')
            elif User.objects.filter(email=email).exists():
                # checks whether email is already in use
                print(2)
                messages.info(request, "This email already exists!")
                return redirect('/add_student/')
            elif User.objects.filter(username=username).exists():
                print(3)
                messages.info(request, "Username already exists!")
                return redirect('/add_student/')
            else:
                user = User.objects.create_user(first_name=first_name, username=username,email=email, password=pwd1)
                user.save()

                today = date.today()
                query = addcourse.objects.values_list('id','duration')
                c = {'d': query}
                bd = date.today()
                enddate = bd + timedelta(days=10)
                trans = students(email=email,cid=ids[0],date = today.strftime("%Y-%m-%d"),expdate= enddate)
                trans.save()
                return redirect('/admin_home/')
        else:
            messages.info(request, 'Passwords are not same')
            return redirect('/admin_home/')

    return render(request, 'first_app/add_student.html',context)

def add_course(request):
    if not (request.user.is_superuser):
        return render(request, 'first_app/indexH.html')
    if request.method == 'POST':
        id = request.POST["id"]
        name = request.POST["name"]
        duration = request.POST["duration"]
        s = addcourse(id=id,name=name,duration=duration)
        flag = s.save()

        if flag is None:
            return render(request, 'first_app/admin_home.html')
        else:
            return render(request, 'first_app/admin_home.html')

    return render(request, 'first_app/add_course.html')

def myprofile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('/indexU/'))

    if request.method == "POST":
        username = request.user.username
        first_name = request.user.first_name
        email = request.user.email
        age = request.POST["age"]
        weight = request.POST["weight"]
        height = request.POST["height"]
        gender = request.POST["gender"]
        gender.lower()
        issue = request.POST["issue"]
        bmi = int(weight) / (int(height) * int(height))

        s = profile(username=username, first_name=first_name, email=email, age=age, gender=gender, height=height,
                    weight=weight, bmi=bmi, issue=issue)
        flag = s.save()

        if flag is None:
            return HttpResponseRedirect(reverse('/indexU/'))
        else:
            return HttpResponseRedirect(reverse('/indexU/'))

    return render(request, 'first_app/myprofile.html')



def indexH(request):
    return render(request, 'first_app/indexH.html')


def indexU(request):
    return render(request, 'first_app/indexU.html')


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('indexH'))


def TeacherHome(request):
    return render(request, 'first_app/TeacherHome.html')


def reschedule(request):
    return render(request, 'first_app/reschedule.html')


def attendance_add(request):
    return render(request, 'first_app/attendance_add.html')


def attendance_view(request):
    return render(request, 'first_app/attendance_view.html')


def user_dashboard(request):
    return render(request, 'first_app/user_dashboard.html')


def indext(request):
    return render(request, 'first_app/indext.html')


def transaction(request):
    return render(request, 'first_app/transaction.html')


def user_courses(request):
    return render(request, 'first_app/user_courses.html')


def admin_home(request):
    return render(request, 'first_app/admin_home.html')


def reschedule_approve(request):
    return render(request, 'first_app/reschedule_approve.html')








def add_teacher(request):
    if not (request.user.is_superuser):
        return render(request, 'first_app/indexH.html')
    data = addcourse.objects.all()
    context = {'d':data }
    if request.method == 'POST':
        first_name = request.POST['first_name']
        username = request.POST['username']
        email = request.POST['email']
        pwd1 = request.POST['pwd1']
        pwd2 = request.POST['pwd2']
        ids = request.POST.getlist('ids')
        if (len(username) == 0 or len(email) == 0 or len(pwd1) == 0 or len(pwd2) == 0 or len(first_name) == 0):
            messages.info(request, "Don't leave the credentials empty!")
            return redirect('/add_teacher/')
        if (pwd1 == pwd2):
            if (User.objects.filter(email=email).exists() and User.objects.filter(username=username).exists()):
                messages.info(request, "Username and email already exists!")
                return redirect('/add_teacher/')
            elif User.objects.filter(email=email).exists():  # checks whether email is already in use
                messages.info(request, "This email already exists!")
                return redirect('/add_teacher/')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists!")
                return redirect('/add_teacher/')
            else:
                user = User.objects.create_user(first_name=first_name, username=username,email=email, password=pwd1)
                user.is_staff = True
                user.save()
                today = date.today()
                trans = teacher(email=email,cid=ids[0],date = today.strftime("%Y-%m-%d") )
                trans.save()
                return redirect('/admin_home/')
        else:
            messages.info(request, 'Passwords are not same')
            return redirect('/admin_home/')

    return render(request, 'first_app/add_student.html',context)
    return render(request, 'first_app/add_teacher.html')


def edit_timetable(request):
    return render(request, 'first_app/edit_timetable.html')
