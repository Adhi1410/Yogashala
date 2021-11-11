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
from django.forms.models import model_to_dict

import smtplib, ssl
from email.message import EmailMessage


class Mail:

    def __init__(self):
        self.port = 465
        self.smtp_server_domain_name = "smtp.gmail.com"
        self.sender_mail = "yogashaala.team7@gmail.com"
        self.password = "Yoga@123"

    def send(self, emails, subject, content):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)

        for email in emails:
            result = service.sendmail(self.sender_mail, email, f"Subject: {subject}\n{content}")

        service.quit()


def psend(mails,subject,content):
    #mails = mails.split()
    #mail = Mail()
    #mail.send(mails, subject, content)
    email_address = "yogashaala.team7@gmail.com"
    email_password = "Yoga@123"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = mails
    msg.set_content(content)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        msg.content_subtype = "html"
        smtp.send_message(msg)
        print("Mail sent successfully!")


"""def signup(request):
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
"""

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
                if check_admin(user) and user.is_active == True:
                    auth.login(request, user)
                    return HttpResponseRedirect('/admin_home/')
                elif check_teacher(user) and user.is_active == True:
                    auth.login(request, user)
                    return HttpResponseRedirect('/TeacherHome/')
                elif check_student(user) and user.is_active == True:
                    auth.login(request, user)
                    return HttpResponseRedirect('/user_dashboard/')
                else:
                    return render_to_response('/login/', message='Account is not active')

            else:
                messages.info(request, 'Invalid Credentials')
                return redirect('/login/')
    return render(request, 'first_app/login.html')

def add_student(request):
    if not (request.user.is_superuser):
        return render(request, 'first_app/indexH.html')
    data = addcourse.objects.exclude(id='1')
    context = {'d':data }

    if request.method == 'POST':
        first_name = request.POST['first_name']
        username = request.POST['username']
        email = request.POST['email']
        pwd1 = request.POST['pwd1']
        pwd2 = request.POST['pwd2']
        id = request.POST.getlist('id[]')
        if (len(username) == 0 or len(email) == 0 or len(first_name) == 0):
            messages.info(request, "Don't leave the credentials empty!")
            return redirect('/add_student/')

        if (User.objects.filter(email=email).exists() and User.objects.filter(username=username).exists()):
            messages.info(request, "Username and email already exists!")
            u = User.objects.get(username=username)
            print("1")
            for i in id:
                it = addcourse.objects.get(id=i)

                if not (students.objects.filter(username=u,course_id=it,status=True).exists()):
                    l = addcourse.objects.filter(id=i).values_list('classes', flat=True)
                    stud = students(username=u, course_id=it, start_date=datetime.now().date(), classes_attended=0,
                                    classes_left=l, status=True)
                    stud.save()
                    User.objects.filter(username=u).update(is_active=True)
                    mess = "Dear " +str(first_name) + ",\nThank You for purchasing a new yoga package. The updated details can be viewed in the My Courses and Transaction History tabs of your account. "
                    psend(email,'New Course added - Yogashaala',mess)

                    print("hi")
            it = addcourse.objects.get(id='1')

            if not (students.objects.filter(course_id=it,username=u,).exists()):
                it = addcourse.objects.get(id='1')
                l = addcourse.objects.filter(id='1').values_list('classes', flat=True)
                stud = students(username=u, course_id=it, start_date=datetime.now().date(), classes_attended=0,
                                classes_left=l, status=True)
                User.objects.filter(username=u).update(is_active=True)
                stud.save()
            return redirect('/add_student/')



        if ( len(pwd1) == 0 or len(pwd2) == 0):
            messages.info(request, "Don't leave the credentials empty!")
            return redirect('/add_student/')
        if (pwd1 == pwd2):
            if (User.objects.filter(email=email).exists() and User.objects.filter(username=username).exists()):
                messages.info(request, "Username and email already exists!")
                u = User.objects.get(username=username)

                for i in id:
                    it = addcourse.objects.get(id=i)
                    l = addcourse.objects.filter(id=i).values_list('classes', flat=True)
                    stud = students(username=u, course_id=it, start_date=datetime.now().date(), classes_attended=0,
                                    classes_left=l, status=True)
                    stud.save()
                    mess = "Dear " + str(first_name) + "\nThank You for purchasing a new yoga package. The updated details can be viewed in the My Courses and Transaction History tabs of your account. "
                    psend(email, 'New Course added - Yogashaala', mess)

                it = addcourse.objects.get(id='1')

                if not (students.objects.filter(course_id = it).exists()):
                    it = addcourse.objects.get(id='1')
                    l = addcourse.objects.filter(id='1').values_list('classes', flat=True)
                    stud = students(username=u, course_id=it, start_date=datetime.now().date(), classes_attended=0,
                                    classes_left=l, status=True)
                    stud.save()
                return redirect('/add_student/')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "This email already exists!")
                return redirect('/add_student/')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists!")
                return redirect('/add_student/')
            else:
                user = User.objects.create_user(first_name=first_name, username=username,email=email, password=pwd1)
                user.save()
                u = User.objects.get(username=username)
                sms = "Dear " + str(first_name) + ",\nThe yogashaala team congratulates you on the successful creation of your new account. We hope you have a pleasant experience as you embark on this new yoga journey with us and gain new  experiences in every class under the guidance of our friendly and experienced teaching staff. The username and password of your account are as follows:\nUsername: " + str(username)+ "\nPassword: " + str(pwd1)+" "
                psend(email, 'Account Credentials - Yogashaala', sms)
                for i in id:
                    it = addcourse.objects.get(id=i)
                    l = addcourse.objects.filter(id=i).values_list('classes',flat=True)
                    stud = students(username=u, course_id=it,start_date=datetime.now().date(),classes_attended=0,classes_left=l,status=True)
                    stud.save()

                    mess = "Dear " + str(first_name) + ",\nThank You for purchasing a new yoga package. The updated details can be viewed in the My Courses and Transaction History tabs of your account."
                    psend(email, 'New Course added - Yogashaala', mess)


                it = addcourse.objects.get(id='1')
                l = addcourse.objects.filter(id='1').values_list('classes', flat=True)
                stud = students(username=u, course_id=it, start_date=datetime.now().date(), classes_attended=0,
                                classes_left=l, status=True)
                stud.save()
                return redirect('/admin_home/')
        else:
            messages.info(request, 'Passwords are not same')
            return redirect('/admin_home/')

    return render(request, 'first_app/add_student.html',context)

def add_course(request):
    if not (request.user.is_superuser):
        return render(request, 'first_app/indexH.html')
    if request.method == 'POST':
        name = request.POST["name"]
        classes = request.POST["classes"]
        duration = request.POST["duration"]
        cost = request.POST["cost"]
        if (addcourse.objects.filter(name=name).exists()):
            return redirect('/admin_home/')
        s = addcourse(name=name,classes=classes,duration=duration,cost=cost)
        s.save()
        return redirect('/admin_home/')


    return render(request, 'first_app/add_course.html')

def myprofile(request):
    if  ( request.user.is_staff):
        return render(request, 'first_app/indexH.html')
    global context
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('/indexU/'))
    id = request.user.username
    u = User.objects.get(username=id)
    context = {
        'age': 'Age in Numerals',
        'gender': 'M/F',
        'height': 'Type your Height in m',
        'weight': 'Type your weight in Kg',
        'bmi': 'BMI will be updated',
        'issue': 'Health Issues, if any',
        'disabled': '',
        #'data - validate' : "Gender is required",
    }

    if profile.objects.filter(username=u).exists() :
        b = profile.objects.get(username=u)
        t='Health Issues, if any'
        if b.issue != 'none' or b.issue != '':
            t = b.issue
        context = {
            'age': b.age,
            'gender' : b.gender,
            'height' : b.height,
            'weight' : b.weight,
            'bmi' : b.bmi,
            'issue' : t,
            'disabled' : 'disabled',
        }
        print(b)

    if request.method == "POST":
        username = request.user.username
        age = request.POST["age"]
        weight = request.POST["weight"]
        height = request.POST["height"]

        issue = request.POST["issue"]
        bmi = round(float(weight) / (float(height) * float(height)),2)
        u = User.objects.get(username=username)
        if profile.objects.filter(username=u).exists():

            profile.objects.filter(username=u).update(age=age, height=height,weight=weight, bmi=bmi, issue=issue)
        else:
            gender = request.POST["gender"]
            gender.lower()
            s = profile(username=u, age=age, gender=gender, height=height,weight=weight, bmi=bmi, issue=issue)
            s.save()
        return redirect('/indexU/')

    return render(request, 'first_app/myprofile.html',context)

def add_teacher(request):
    if not (request.user.is_superuser):
        return render(request, 'first_app/indexH.html')
    data = addcourse.objects.exclude(id='1')
    context = {'d':data }
    if request.method == 'POST':
        first_name = request.POST['first_name']
        username = request.POST['username']
        email = request.POST['email']
        pwd1 = request.POST['pwd1']
        pwd2 = request.POST['pwd2']
        id = request.POST.getlist('id[]')
        if (len(username) == 0 or len(email) == 0  or len(first_name) == 0):
            messages.info(request, "Don't leave the credentials empty!")
            return redirect('/add_teacher/')
        if (User.objects.filter(email=email).exists() and User.objects.filter(username=username).exists()):
            u = User.objects.get(username=username)
            for i in id:
                it = addcourse.objects.get(id=i)
                if not (teacher.objects.filter(username=u,course_id=it).exists()):
                    teach = teacher(username=u, course_id=it)
                    teach.save()
                    psend(email, 'New Course added - Yogashaala', 'New Course has been added to your account')

            it = addcourse.objects.get(id='1')
            if not (teacher.objects.filter(username=u,course_id=it).exists()):
                teach = teacher(username=u, course_id=it)
                teach.save()

            return redirect('/add_teacher/')
        if ( len(pwd1) == 0 or len(pwd2) == 0 ):
            messages.info(request, "Don't leave the credentials empty!")
            return redirect('/add_teacher/')
        if (pwd1 == pwd2):
            if (User.objects.filter(email=email).exists() and User.objects.filter(username=username).exists()):
                u = User.objects.get(username=username)
                for i in id:
                    it = addcourse.objects.get(id=i)
                    teach = teacher(username=u, course_id=it)
                    teach.save()
                    psend(email, 'New Course added - Yogashaala', 'New Course has been added to your account')
                it = addcourse.objects.get(id='1')
                if not (teacher.objects.filter(username=u,course_id=it).exists()):
                    teach = teacher(username=u, course_id=it)
                    teach.save()
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
                sms =  'Dear ' + str(first_name) + '\nThe yogashaala team<br>is delighted to have you join our family. We hope you have a pleasant experience teaching at yogashaala.The username and password of your account as well as courses you will handle are as follows:\nUsername: ' +str(username) +'\npassword: '+ str(pwd1)+' '
                psend(email, 'Account Credentials - Yogashaala',sms)
                u = User.objects.get(username=username)

                for i in id:
                    it = addcourse.objects.get(id=i)
                    teach = teacher(username=u,course_id = it)
                    teach.save()
                it = addcourse.objects.get(id='1')
                teach = teacher(username=u, course_id=it)
                teach.save()
                psend(email, 'New Course added - Yogashaala', 'New Course has been added to your account')
                return redirect('/admin_home/')
        else:
            messages.info(request, 'Passwords are not same')
            return redirect('/admin_home/')

    return render(request, 'first_app/add_teacher.html',context)

def admin_home(request):
    if not (request.user.is_superuser):
        return render(request, 'first_app/indexH.html')
    mo = timetable.objects.filter(day = 'MONDAY')
    tu = timetable.objects.filter(day = 'TUESDAY')
    wed = timetable.objects.filter(day='WEDNESDAY')
    th = timetable.objects.filter(day='THURSDAY')
    fri = timetable.objects.filter(day='FRIDAY')
    sat = timetable.objects.filter(day='SATURDAY')
    sun = timetable.objects.filter(day='SUNDAY')

    context = {
        'mo' : mo,
        'tu' : tu,
        'wed' : wed,
        'th' : th,
        'fri' : fri,
        'sat' : sat,
        'sun' : sun,
        'free' : 'FREE',
        'def' : '/admin_home/'
    }
    return render(request, 'first_app/admin_home.html',context)

def indexH(request):
    return render(request, 'first_app/indexH.html')

def indexU(request):
    return render(request, 'first_app/indexU.html')

def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('indexH'))

def edit_timetable(request):
    if not (request.user.is_superuser):
        return render(request, 'first_app/indexH.html')
    mo = timetable.objects.filter(day = 'MONDAY')
    tu = timetable.objects.filter(day = 'TUESDAY')
    wed = timetable.objects.filter(day='WEDNESDAY')
    th = timetable.objects.filter(day='THURSDAY')
    fri = timetable.objects.filter(day='FRIDAY')
    sat = timetable.objects.filter(day='SATURDAY')
    sun = timetable.objects.filter(day='SUNDAY')
    data = addcourse.objects.all()
    context = {
        'mo' : mo,
        'tu' : tu,
        'wed' : wed,
        'th' : th,
        'fri' : fri,
        'sat' : sat,
        'sun' : sun,
        'free' : 'FREE',
        'def' : '/admin_home/',
        'data' :data,
    }
    if request.method == 'POST':
        #monday
        try:
            mon1 = request.POST["6:30 - 8:00MONDAY"]
            timetable.objects.filter(day = 'MONDAY',time= '6:30 - 8:00').update(course_id =mon1)
        except:
            pass

        try:
            mon2 = request.POST["8:15 - 9:45MONDAY"]
            timetable.objects.filter(day = 'MONDAY',time= '8:15 - 9:45').update(course_id =mon2)
        except:
            pass
        try:
            mon3 = request.POST["10:00 - 11:30MONDAY"]
            timetable.objects.filter(day = 'MONDAY',time= '10:00 - 11:30').update(course_id =mon3)
        except:
            pass
        try:
            mon4 = request.POST["11:45 - 1:15MONDAY"]
            timetable.objects.filter(day = 'MONDAY',time= '11:45 - 1:15').update(course_id =mon4)
        except:
            pass
        try:
            mon5 = request.POST["2:00 - 3:30MONDAY"]
            timetable.objects.filter(day = 'MONDAY',time= '2:00 - 3:30').update(course_id =mon5)
        except:
            pass
        try:
            mon6 = request.POST["3:45 - 5:15MONDAY"]
            timetable.objects.filter(day = 'MONDAY',time= '3:45 - 5:15').update(course_id =mon6)
        except:
            pass
        try:
            mon7 = request.POST["5:30 - 7:00MONDAY"]
            timetable.objects.filter(day = 'MONDAY',time= '5:30 - 7:00').update(course_id =mon7)
        except:
            pass

        #tuesday

        try:
            tue1 = request.POST["6:30 - 8:00TUESDAY"]
            timetable.objects.filter(day = 'TUESDAY',time= '6:30 - 8:00').update(course_id =tue1)
        except:
            pass

        try:
            tue2 = request.POST["8:15 - 9:45TUESDAY"]
            timetable.objects.filter(day = 'TUESDAY',time= '8:15 - 9:45').update(course_id =tue2)
        except:
            pass
        try:
            tue3 = request.POST["10:00 - 11:30TUESDAY"]
            timetable.objects.filter(day = 'TUESDAY',time= '10:00 - 11:30').update(course_id =tue3)
        except:
            pass
        try:
            tue4 = request.POST["11:45 - 1:15TUESDAY"]
            timetable.objects.filter(day = 'TUESDAY',time= '11:45 - 1:15').update(course_id =tue4)
        except:
            pass
        try:
            tue5 = request.POST["2:00 - 3:30TUESDAY"]
            timetable.objects.filter(day = 'TUESDAY',time= '2:00 - 3:30').update(course_id =tue5)
        except:
            pass
        try:
            tue6 = request.POST["3:45 - 5:15TUESDAY"]
            timetable.objects.filter(day = 'TUESDAY',time= '3:45 - 5:15').update(course_id =tue6)
        except:
            pass
        try:
            tue7 = request.POST["5:30 - 7:00TUESDAY"]
            timetable.objects.filter(day = 'TUESDAY',time= '5:30 - 7:00').update(course_id =tue7)
        except:
            pass

        #wednesday
        try:
            wed1 = request.POST["6:30 - 8:00WEDNESDAY"]
            timetable.objects.filter(day='WEDNESDAY', time='6:30 - 8:00').update(course_id=wed1)
        except:
            pass

        try:
            wed2 = request.POST["8:15 - 9:45WEDNESDAY"]
            timetable.objects.filter(day='WEDNESDAY', time='8:15 - 9:45').update(course_id=wed2)
        except:
            pass
        try:
            wed3 = request.POST["10:00 - 11:30WEDNESDAY"]
            timetable.objects.filter(day='WEDNESDAY', time='10:00 - 11:30').update(course_id=wed3)
        except:
            pass
        try:
            wed4 = request.POST["11:45 - 1:15WEDNESDAY"]
            timetable.objects.filter(day='WEDNESDAY', time='11:45 - 1:15').update(course_id=wed4)
        except:
            pass
        try:
            wed5 = request.POST["2:00 - 3:30WEDNESDAY"]
            timetable.objects.filter(day='WEDNESDAY', time='2:00 - 3:30').update(course_id=wed5)
        except:
            pass
        try:
            wed6 = request.POST["3:45 - 5:15WEDNESDAY"]
            timetable.objects.filter(day='WEDNESDAY', time='3:45 - 5:15').update(course_id=wed6)
        except:
            pass
        try:
            wed7 = request.POST["5:30 - 7:00WEDNESDAY"]
            timetable.objects.filter(day='WEDNESDAY', time='5:30 - 7:00').update(course_id=wed7)
        except:
            pass

        #thursday
        try:
            th1 = request.POST["6:30 - 8:00THURSDAY"]
            timetable.objects.filter(day='THURSDAY', time='6:30 - 8:00').update(course_id=th1)
        except:
            pass

        try:
            th2 = request.POST["8:15 - 9:45THURSDAY"]
            timetable.objects.filter(day='THURSDAY', time='8:15 - 9:45').update(course_id=th2)
        except:
            pass
        try:
            th3 = request.POST["10:00 - 11:30THURSDAY"]
            timetable.objects.filter(day='THURSDAY', time='10:00 - 11:30').update(course_id=th3)
        except:
            pass
        try:
            th4 = request.POST["11:45 - 1:15THURSDAY"]
            timetable.objects.filter(day='THURSDAY', time='11:45 - 1:15').update(course_id=th4)
        except:
            pass
        try:
            th5 = request.POST["2:00 - 3:30THURSDAY"]
            timetable.objects.filter(day='THURSDAY', time='2:00 - 3:30').update(course_id=th5)
        except:
            pass
        try:
            th6 = request.POST["3:45 - 5:15THURSDAY"]
            timetable.objects.filter(day='THURSDAY', time='3:45 - 5:15').update(course_id=th6)
        except:
            pass
        try:
            th7 = request.POST["5:30 - 7:00THURSDAY"]
            timetable.objects.filter(day='THURSDAY', time='5:30 - 7:00').update(course_id=th7)
        except:
            pass

        #friday

        try:
            fri1 = request.POST["6:30 - 8:00FRIDAY"]
            timetable.objects.filter(day='FRIDAY', time='6:30 - 8:00').update(course_id=fri1)
        except:
            pass

        try:
            fri2 = request.POST["8:15 - 9:45FRIDAY"]
            timetable.objects.filter(day='FRIDAY', time='8:15 - 9:45').update(course_id=fri2)
        except:
            pass
        try:
            fri3 = request.POST["10:00 - 11:30FRIDAY"]
            timetable.objects.filter(day='FRIDAY', time='10:00 - 11:30').update(course_id=fri3)
        except:
            pass
        try:
            fri4 = request.POST["11:45 - 1:15FRIDAY"]
            timetable.objects.filter(day='FRIDAY', time='11:45 - 1:15').update(course_id=fri4)
        except:
            pass
        try:
            fri5 = request.POST["2:00 - 3:30FRIDAY"]
            timetable.objects.filter(day='FRIDAY', time='2:00 - 3:30').update(course_id=fri5)
        except:
            pass
        try:
            fri6 = request.POST["3:45 - 5:15FRIDAY"]
            timetable.objects.filter(day='FRIDAY', time='3:45 - 5:15').update(course_id=fri6)
        except:
            pass
        try:
            fri7 = request.POST["5:30 - 7:00FRIDAY"]
            timetable.objects.filter(day='FRIDAY', time='5:30 - 7:00').update(course_id=fri7)
        except:
            pass

        #saturday
        try:
            sat1 = request.POST["6:30 - 8:00SATURDAY"]
            timetable.objects.filter(day='SATURDAY', time='6:30 - 8:00').update(course_id=sat1)
        except:
            pass

        try:
            sat2 = request.POST["8:15 - 9:45SATURDAY"]
            timetable.objects.filter(day='SATURDAY', time='8:15 - 9:45').update(course_id=sat2)
        except:
            pass
        try:
            sat3 = request.POST["10:00 - 11:30SATURDAY"]
            timetable.objects.filter(day='SATURDAY', time='10:00 - 11:30').update(course_id=sat3)
        except:
            pass
        try:
            sat4 = request.POST["11:45 - 1:15SATURDAY"]
            timetable.objects.filter(day='SATURDAY', time='11:45 - 1:15').update(course_id=sat4)
        except:
            pass
        try:
            sat5 = request.POST["2:00 - 3:30SATURDAY"]
            timetable.objects.filter(day='SATURDAY', time='2:00 - 3:30').update(course_id=sat5)
        except:
            pass
        try:
            sat6 = request.POST["3:45 - 5:15SATURDAY"]
            timetable.objects.filter(day='SATURDAY', time='3:45 - 5:15').update(course_id=sat6)
        except:
            pass
        try:
            sat7 = request.POST["5:30 - 7:00SATURDAY"]
            timetable.objects.filter(day='SATURDAY', time='5:30 - 7:00').update(course_id=sat7)
        except:
            pass

        #sunday
        try:
            sun1 = request.POST["6:30 - 8:00SUNDAY"]
            timetable.objects.filter(day='SUNDAY', time='6:30 - 8:00').update(course_id=sun1)
        except:
            pass

        try:
            sun2 = request.POST["8:15 - 9:45SUNDAY"]
            timetable.objects.filter(day='SUNDAY', time='8:15 - 9:45').update(course_id=sun2)
        except:
            pass
        try:
            sun3 = request.POST["10:00 - 11:30SUNDAY"]
            timetable.objects.filter(day='SUNDAY', time='10:00 - 11:30').update(course_id=sun3)
        except:
            pass
        try:
            sun4 = request.POST["11:45 - 1:15SUNDAY"]
            timetable.objects.filter(day='SUNDAY', time='11:45 - 1:15').update(course_id=sun4)
        except:
            pass
        try:
            sun5 = request.POST["2:00 - 3:30SUNDAY"]
            timetable.objects.filter(day='SUNDAY', time='2:00 - 3:30').update(course_id=sun5)
        except:
            pass
        try:
            sun6 = request.POST["3:45 - 5:15SUNDAY"]
            timetable.objects.filter(day='SUNDAY', time='3:45 - 5:15').update(course_id=sun6)
        except:
            pass
        try:
            sun7 = request.POST["5:30 - 7:00SUNDAY"]
            timetable.objects.filter(day='SUNDAY', time='5:30 - 7:00').update(course_id=sun7)
        except:
            pass


    return render(request, 'first_app/edit_timetable.html',context)

def TeacherHome(request):
    if not (request.user.is_staff):
        return render(request, 'first_app/indexH.html')
    id = request.user.username
    u = User.objects.get(username=id)
    tec_id = teacher.objects.filter(username =u)
    tt = timetable.objects.all()
    replace = None
    for i in tt:
        if i.course_id.id == 1:
            replace = i
            break
    ml = []
    tl = []
    wel = []
    thl = []
    frl = []
    sal = []
    sul = []
    mo = timetable.objects.filter(day='MONDAY')
    tu = timetable.objects.filter(day='TUESDAY')
    wed = timetable.objects.filter(day='WEDNESDAY')
    th = timetable.objects.filter(day='THURSDAY')
    fri = timetable.objects.filter(day='FRIDAY')
    sat = timetable.objects.filter(day='SATURDAY')
    sun = timetable.objects.filter(day='SUNDAY')

    for i in mo:
        for j in  tec_id:
            if i.course_id.id == j.course_id.id:
                ml.append(i)
                break
        else:
            ml.append(replace)

    for i in tu:
        for j in  tec_id:
            if i.course_id.id == j.course_id.id:
                tl.append(i)
                break
        else:
            tl.append(replace)

    for i in wed:
        for j in  tec_id:
            if i.course_id.id == j.course_id.id:
                wel.append(i)
                break
        else:
            wel.append(replace)

    for i in th:
        for j in  tec_id:
            if i.course_id.id == j.course_id.id:
                thl.append(i)
                break
        else:
            thl.append(replace)

    for i in fri:
        for j in  tec_id:
            if i.course_id.id == j.course_id.id:
                frl.append(i)
                break
        else:
            frl.append(replace)

    for i in sat:
        for j in  tec_id:
            if i.course_id.id == j.course_id.id:
                sal.append(i)
                break
        else:
            sal.append(replace)

    for i in sun:
        for j in  tec_id:
            if i.course_id.id == j.course_id.id:
                sul.append(i)
                break
        else:
            sul.append(replace)
    context = {
    'mo' : ml,
    'tu' : tl,
    'wed' : wel,
    'th' : thl,
    'fri' : frl,
    'sat' : sal,
    'sun' : sul,
    'check': tec_id,
    'free' : 'FREE',
    'def' : '/TeacherHome/',
    'myname' : u.first_name,
    }
    return render(request, 'first_app/TeacherHome.html',context)

def reschedule(request):
    if not (request.user.is_staff):
        return render(request, 'first_app/indexH.html')
    id = request.user.username
    u = User.objects.get(username=id)
    global tr
    global sec
    global day
    global time
    global reason
    global free
    context={
        'data' : '',
    }
    if request.method=='POST' and "search" in request.POST:
        try:
            day = request.POST['day']
            time = request.POST['time']
            reason = request.POST['reason']
            tr= teacher.objects.filter(username=u).exclude(course_id=1)

            sec = timetable.objects.filter(day=day, time=time)
            for i in tr:
                for j in sec:
                    if i.course_id.id == j.course_id.id:
                        free = timetable.objects.filter(course_id=1)

                        context = {
                            'data': free
                        }
                        break

        except:
            pass
    if request.method=='POST' and "mark" in request.POST:

        id = request.POST.getlist('id[]')
        t = id[0].split(' || ')
        print(t[0],t[1])
        print(day,time,reason)
        if reschedule_req.objects.filter(s_day=day, s_time=time, r_day=t[0], r_time=t[1],today=datetime.now().date()).exists():
            return redirect('/TeacherHome/')
        else:
            resche = reschedule_req(username=u, s_day=day, s_time=time, r_day=t[0], r_time=t[1], reason=reason,today=datetime.now().date(), status=1)
            resche.save()
    return render(request, 'first_app/reschedule.html',context)

def attendance_add(request):
    if not (request.user.is_staff):
        return render(request, 'first_app/indexH.html')
    id = request.user.username
    u = User.objects.get(username=id)
    ls = teacher.objects.filter(username=u).exclude(course_id =1)

    context={
        'search': ls,
    }
    global day
    global time
    global course_id
    date = datetime.now().date()
    if request.method=='POST' and "search" in request.POST:
        try:
            day = request.POST['day']
            time = request.POST['time']
            course_id = request.POST['course_id']
        except:
            pass
    try:
        temp = students.objects.filter(course_id = course_id,status = True)
        d_t = timetable.objects.filter(day = day,time = time)

        if int(d_t[0].course_id.id) == int(course_id):
            context = {
                'search': ls,
                'data' : temp,
            }
        course_id = d_t[0].course_id.id
    except:
        pass
    if request.method=='POST' and "mark" in request.POST:
        id = request.POST.getlist('id[]')
        for i in id:
            u = User.objects.get(username=i)
            cid = addcourse.objects.filter(id = course_id)
            email = u.email
            print(email)
            id = request.user.username
            my = User.objects.get(username=id)
            if attendance.objects.filter(myname=my,username=u,date=date,course_id=cid[0]).exists():
                return redirect('/TeacherHome/')
            #print(u,date,time,c[0])
            else:
                t = attendance(myname=my,username=u,date=date,s_day=day,s_time=time,course_id=cid[0])
                t.save()
                left = students.objects.filter(username=u,course_id=cid[0],status=True)
                t = left[0].classes_left
                t =t -1
                if t ==0:
                    students.objects.filter(username=u, course_id=cid[0], status=True).update(classes_left=t,status=False)
                else:
                    students.objects.filter(username=u,course_id=cid[0],status=True).update(classes_left = t)
                    psend(email, 'Attendance had been update', 'Attendance has been updated, check to My courses')

                y = students.objects.filter(username=u,status=True).exclude(course_id=1)
                if not y:
                    User.objects.filter(username = u).update(is_active = False)
                    psend(email, 'Course Expired', 'All the courses you purchased has been expired')

        return redirect('/TeacherHome/')

    return render(request, 'first_app/attendance_add.html',context)

def attendance_view(request):
    if not (request.user.is_staff):
        return render(request, 'first_app/indexH.html')
    id = request.user.username
    u = User.objects.get(username=id)
    context = {
        'data' :'',
    }
    if request.method == "POST":
        try:
            date = request.POST["sdate"]
            t = attendance.objects.filter(myname=u,date = date)
            context={
                'data' : t,
            }
        except:
            pass
    return render(request, 'first_app/attendance_view.html',context)

def user_dashboard(request):
    id = request.user.username
    u = User.objects.get(username=id)
    tec_id = students.objects.filter(username=u)
    tt = timetable.objects.all()
    ls = []
    for i in tec_id:
        if i.status == True :
            ls.append(i)

    replace = None
    for i in tt:
        if i.course_id.id == 1:
            replace = i
            break

    ml = []
    tl = []
    wel = []
    thl = []
    frl = []
    sal = []
    sul = []
    mo = timetable.objects.filter(day='MONDAY')
    tu = timetable.objects.filter(day='TUESDAY')
    wed = timetable.objects.filter(day='WEDNESDAY')
    th = timetable.objects.filter(day='THURSDAY')
    fri = timetable.objects.filter(day='FRIDAY')
    sat = timetable.objects.filter(day='SATURDAY')
    sun = timetable.objects.filter(day='SUNDAY')

    for i in mo:
        for j in ls:
            if i.course_id.id == j.course_id.id:
                ml.append(i)
                break
        else:
            ml.append(replace)

    for i in tu:
        for j in ls:
            if i.course_id.id == j.course_id.id:
                tl.append(i)
                break
        else:
            tl.append(replace)

    for i in wed:
        for j in ls:
            if i.course_id.id == j.course_id.id:
                wel.append(i)
                break
        else:
            wel.append(replace)

    for i in th:
        for j in ls:
            if i.course_id.id == j.course_id.id:
                thl.append(i)
                break
        else:
            thl.append(replace)

    for i in fri:
        for j in ls:
            if i.course_id.id == j.course_id.id:
                frl.append(i)
                break
        else:
            frl.append(replace)

    for i in sat:
        for j in ls:
            if i.course_id.id == j.course_id.id:
                sal.append(i)
                break
        else:
            sal.append(replace)

    for i in sun:
        for j in ls:
            if i.course_id.id == j.course_id.id:
                sul.append(i)
                break
        else:
            sul.append(replace)

    context = {
        'mo': ml,
        'tu': tl,
        'wed': wel,
        'th': thl,
        'fri': frl,
        'sat': sal,
        'sun': sul,
        'check': tec_id,
        'free': 'FREE',
        'def': '/TeacherHome/',
        'myname' : u.first_name,
    }
    return render(request, 'first_app/user_dashboard.html',context)

def indext(request):
    return render(request, 'first_app/indext.html')

def transaction(request):
    id = request.user.username
    u = User.objects.get(username=id)
    tec_id = students.objects.filter(username=u)
    lis = sorted(tec_id,key=lambda x:x.start_date,reverse=True)
    ls=[]
    for i in lis:
        if i.course_id.id != 1:
            ls.append(i)

    context = {
        'trans': ls,
        'active' :'mode mode_on',
        'exp': 'mode mode_off',
        'true' : True,
    }
    return render(request, 'first_app/transaction.html',context)

def user_courses(request):
    id = request.user.username
    u = User.objects.get(username=id)
    tec_id = students.objects.filter(username=u)
    ls=[]
    for i in tec_id:
        if i.status == True and i.course_id.id != 1:
            ls.append(i)
    context = {
        'trans': ls,
    }
    return render(request, 'first_app/user_courses.html',context)

def reschedule_approve(request):
    if not (request.user.is_superuser):
        return render(request, 'first_app/indexH.html')
    ls = reschedule_req.objects.filter(status=1)
    t = sorted(ls,key=lambda x:x.id,reverse=True)

    tt = timetable.objects.all()
    replace = None
    for i in tt:
        if i.course_id.id == 1:
            replace = i
            break

    lable = []
    colours = []
    d = []
    co = teacher.objects.filter(course_id =1)
    for i in co:
        lable.append(i.username.first_name)
        cou = reschedule_req.objects.filter(username=i.username).count()
        d.append(cou)

    for j in range(len(d)):
        r = str(random.randint(50, 255))
        g = str(random.randint(50, 255))
        b = str(random.randint(50, 255))
        tt = 'rgb(' + r + ',' + g + ',' + b + ')'
        colours.append(tt)
    context = {
        'ls': t,
        'labels': lable,
        'data': d,
        'col': colours,
    }

    if request.method == 'POST':
        for key, value in request.POST.items():
            try:
                op_rs = reschedule_req.objects.filter(id=key)
                temp2 = None
                if value == 'approve':
                    temp= timetable.objects.filter(day=op_rs[0].s_day, time= op_rs[0].s_time)
                    temp2 = timetable.objects.filter(day=op_rs[0].r_day, time= op_rs[0].r_time)
                    stu = students.objects.filter(course_id=temp[0].course_id, status=True)

                    for i in stu:
                        smess = "Dear " + str(i.username.first_name) + " we are sorry to inform you that your " + \
                                str(i.course_id.name) + " course scheduled on " + str(op_rs[0].s_day) + " " + \
                                str(op_rs[0].s_time) + " has been rescheduled to " + \
                                str(op_rs[0].r_day) + " " + str(op_rs[0].r_time)
                        psend(i.username.email, 'Classes Rescheduled', smess)
                    timetable.objects.filter(day=op_rs[0].r_day, time=op_rs[0].r_time).update(course_id = temp[0].course_id)
                    timetable.objects.filter(day=op_rs[0].s_day, time=op_rs[0].s_time).update(course_id = replace.course_id)
                    reschedule_req.objects.filter(id=key).update(status=2)
                    t = reschedule_req.objects.filter(id=key)
                    mess = "Dear " + str(t[0].username.first_name) + " This is to let you know that your Rescheduling request applied on " + str(t[0].today) + " has been Approved"
                    psend(t[0].username.email, 'Rescheduling request - Approved', mess)





                elif value == 'deny':
                    reschedule_req.objects.filter(id=key).update(status = 3)
                    t = reschedule_req.objects.filter(id=key)
                    print(t[0].username.email)
                    mess = "Dear " + str(t[0].username.first_name) + " We are sorry to let you know that your Rescheduling request applied on " + str(t[0].today) +" has been denied"

                    psend(t[0].username.email, 'Rescheduling request - Denied', mess)

                else:
                    pass
            except:
                pass
        return redirect('/reschedule_approve/')

    return render(request, 'first_app/reschedule_approve.html',context)

def reschedule_check(request):
    if not (request.user.is_staff):
        return render(request, 'first_app/indexH.html')
    id = request.user.username
    u = User.objects.get(username=id)
    ls = reschedule_req.objects.filter(username=u)
    t = sorted(ls,key=lambda x:x.today,reverse=True)
    context={
        'ls' :t,
        'active': 'mode mode_on',
        'exp': 'mode mode_off',
        'net': 'mode mode_done',
        'one':1,
        'two' :2,
    }
    return render(request, 'first_app/reschedule_check.html',context)

def admin_attendance(request):
    if not (request.user.is_superuser):
        return render(request, 'first_app/indexH.html')
    t = attendance.objects.all()
    context= {
        'data' : t,
    }
    return render(request, 'first_app/admin_attendance.html',context)

def cash(request):
    if not (request.user.is_superuser):
        return render(request, 'first_app/indexH.html')
    ls = students.objects.all().exclude(course_id =1)
    ls = sorted(ls,reverse=True,key=lambda x:x.start_date)
    s=0
    for i in ls:
        s = s + int(i.course_id.cost)

    #'rgb(255, 99, 132)'
    lable = []
    colours = []
    d = []
    co = addcourse.objects.all().exclude(id =1)
    for i in co:
        lable.append(i.name)
        cou = students.objects.filter(course_id = i.id).count()
        d.append(cou)

    for j in range (len(d)):
        r =str(random.randint(50,255))
        g =str(random.randint(50,255))
        b =str(random.randint(50,255))
        t = 'rgb('+r+','+g+','+b+')'
        colours.append(t)
    context = {
        'trans': ls,
        'active': 'mode mode_on',
        'exp': 'mode mode_off',
        'true': True,
        'sum' :s,
        'labels': lable,
        'data': d,
        'col': colours,
    }

    return render(request, 'first_app/cash.html',context)

def view_profile(request):
    if not (request.user.is_staff):
        return render(request, 'first_app/indexH.html')
    id = request.user.username
    u = User.objects.get(username=id)
    ls = teacher.objects.filter(username=u).exclude(course_id=1)

    context = {
        'search': ls,
    }
    if request.method == 'POST' and "search" in request.POST:
        try:
            course_id = request.POST['course_id']
            cid = addcourse.objects.filter(id = course_id)
            tt = students.objects.filter(status=True,course_id=cid[0].id).exclude(course_id =1)
            lp=[]
            lr=[]
            for i in tt:

                if i.username in lr:
                    pass
                else:
                    lr.append(i.username)
                    lp.append(i)
            t = profile.objects.all()
            ty=[]
            for i in lp:
                for j in t:
                    if i.username == j.username:
                        ty.append(j)

            context = {
                'data': ty,
                'search': ls,
            }
        except:
            pass

    return render(request, 'first_app/view_profile.html',context)