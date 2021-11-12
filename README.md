<h1>YOGASHALA</h1>

<h2>OVERVIEW</h2>
<p>To design a website which acts as a Point of Sales (POS) for a Yoga Company that is trying to adapt to the online mode of teaching due to the current pandemic situation.
Our main focus while designing the website was geared towards providing the users with a pleasant one-stop experience for all their yoga needs. 
Although the main focus was towards the user end we have provided dynamic functionalities for both the administration as well as the teacher
in order to ensure the website does not become obsolete and stays relevant in the ever-changing future.</p>

<h4>NOTE: The proprietary video conferencing application is uploaded to another github repository for clarity and deployment purposes.<br>It can be accessed with the following link : "https://github.com/Cyber-Celestial/psg-meet-app".</h4>
  

<h2>KEY FEATURES</h2>
a) Proprietary Video Conferencing Application.<br>
b) Responsive Webpages which adapt to any device dimensions.<br>
c) Multiple user classes.<br>
d) Analysis model of cash flow and footfall.<br>
e) The cohesive flow of Time Table between modules.<br>

<h2>DESCRIPTION OF FILES USED</h2>
<h3>Django Folder and yogashala Folder:</h3>
Consists of all files and folders with regards to the website.
<h4>first_app Folder:</h4>
Contains all the database, tables, and html pages.
<h5>templates Folder:</h5>
Contains all the html pages of the website


indexH.html - indexH.html page shows the generic home page displayed to users when they first visit the website without logging in.

login.html - login.html page offers the user (all 3 classes of users) login option.

user_dashboard.html - user_dashboard.html page displays the timetable for the customer / student. This is also the home page for the user.

myprofile.html - myprofile.html page shows the student's profile. The user can edit their details to make their accounts more personalized.

user_courses.html - user_courses.html page gives the courses in which the student is or was enrolled in.

transaction.html - transaction.html page gives the student the courses they had purchased along with their purchase date and active status.

TeacherHome.html - TeacherHome.html page displays the timetable for the teacher. This is also the home page for the teacher.

reschedule.html - reschedule.html page offers the teacher the option to reschedule their class's date and time.

reschedule_check.html - reschedule_check.html page shows the teacher's rescheduling request's status.

attendance_add.html - attendance_add.html page is used by the teacher to add attendance for a particular course on a particular date.

attendance_view.html - attendance_view.html page displays the attendance of the students under that particular teacher's course.

admin_home.html - admin_home.html page shows the admin's home page which consists of the Master timetable.

reschedule_approve.html - reschedule_approve.html page gives all the rescheduling requests sent by all the teachers. The admin can choose to approve or deny each request. It also shows the rescheduling analysis of different teachers.

edit_timetable.html - edit_timetable.html page gives the admin access to edit the master timetable itself. Any change in the master timetable will be reflected in every student's and teacher's timetables.

add_student.html - add_student.html page displays the student adding option to the admin. Using this, the admin can add students to their respective courses as well as create their student ids themselves.

add_teacher.html - add_teacher.html page offers the admin the facility to add teacher accounts. While creating the teacher's account, the courses the respective teachers will be responsible for will also be mentioned priorly.

add_course.html - add_course.html page shows the course adding feature of the web application.

admin_attendance.html - admin_attendance.html page gives the attendance of the teachers for their courses.

cash.html - cash.html page gives the admin a detailed analysis of the cash flow for all courses. It also provides insight on which courses are preferred over the others.


## Demo

🔗[Yogashaala](https://drive.google.com/file/d/15hSU4nIt6ksfu3cgIDf9l_RAzzhlPFZf/view?usp=sharing)

## Tools Used

#### Front-End
```bash
    HTML
    CSS and Bootstrap
    Javascript
```
#### Back-End
```bash
    Node.js
    Django
    Express
```

## Deployment

#### Django installation
```bash
    pipenv install django
```

#### Project and App creation
```bash
    django-admin startproject {project-name}
    python manage.py startapp {app-name}
```

#### Admin registration
```bash
    python manage.py createsuperuser
```

#### Run the Project (you can add a port number if you want)
```bash
    python manage.py runserver {port number}
```

#### Install SMTP
```bash
    pip install secure-smtplib
```

## Authors

- [A Kirthic Vishnu]
- [Adharsh S]
- [Aditya Sriram]
- [K Sandeep Kumar]
- [Kumaresh S]

