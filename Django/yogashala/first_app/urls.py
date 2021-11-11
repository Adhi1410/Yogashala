#map the urls with view functions

from django.contrib.admin.decorators import register
from django.urls import path
from . import views

urlpatterns=[
    path('',views.indexH,name='indexH'),
    path('indexU/',views.indexU,name='indexU'),
    path('indexH/',views.indexH,name='indexH'),
    path('login/',views.login_view,name='login'),
    path('myprofile/',views.myprofile,name='myprofile'),
    path('logout/',views.logoutview,name='logout'),
    path('TeacherHome/',views.TeacherHome,name='TeacherHome'),
    path('reschedule/',views.reschedule,name='reschedule'),
    path('attendance_add/',views.attendance_add,name='attendance_add'),
    path('attendance_view/',views.attendance_view,name='attendance_view'),
    path('user_dashboard/',views.user_dashboard,name='user_dashboard'),
    path('indext/',views.indext,name='indext'),
    path('transaction/',views.transaction,name='transaction'),
    path('user_courses/',views.user_courses,name='user_courses'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('reschedule_approve/',views.reschedule_approve,name='reschedule_approve'),
    path('add_course/',views.add_course,name='add_course'),
    path('add_student/',views.add_student,name='add_student'),
    path('add_teacher/',views.add_teacher,name='add_teacher'),
    path('edit_timetable/',views.edit_timetable,name='edit_timetable'),
    path('reschedule_check/',views.reschedule_check,name='reschedule_check'),
    path('admin_attendance/',views.admin_attendance,name='admin_attendance'),
    path('cash/',views.cash,name='cash'),
    path('view_profile/',views.view_profile,name='view_profile'),
]

