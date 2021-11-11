from django.contrib import auth
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.db.models import F, Count

class profile(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    height = models.FloatField()
    weight = models.FloatField()
    bmi = models.FloatField()
    issue = models.CharField(max_length=500)
    def __str__(self):
        return f'{self.username}  || {self.age}|| {self.gender} || {self.height} || {self.weight} || {self.bmi} || {self.issue}'

class addcourse(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=15)
    classes = models.IntegerField()
    duration = models.IntegerField()
    cost = models.IntegerField()
    def __str__(self):
        return f'{self.id} || {self.name} || {self.classes} || {self.duration} || {self.cost}'

class teacher(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    course_id = models.ForeignKey(addcourse,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.username} || {self.course_id} '

class students(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(addcourse, on_delete=models.CASCADE)
    start_date = models.DateField()
    classes_attended = models.IntegerField()
    classes_left = models.IntegerField()
    status = models.BooleanField()
    def __str__(self):
        return f'{self.username} || {self.course_id} || {self.start_date} || {self.classes_attended} || {self.classes_left} || {self.status}'


class timetable(models.Model):
    day = models.CharField(max_length=25)
    time = models.CharField(max_length=50)
    class_link = models.CharField(max_length=500)
    course_id = models.ForeignKey(addcourse, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.day} || {self.time} || {self.class_link} || {self.course_id}'

class reschedule_req(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    s_day = models.CharField(max_length=15)
    s_time = models.CharField(max_length=50)
    r_day = models.CharField(max_length=15)
    r_time = models.CharField(max_length=50)
    reason = models.CharField(max_length=500)
    today = models.DateField()
    status = models.IntegerField()
    def __str__(self):
        return f'{self.id} ||{self.username} || {self.s_day} || {self.s_time} || {self.r_day} || {self.r_time} || {self.reason} || {self.today} || {self.status}'

class attendance(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    myname = models.ForeignKey(User, on_delete=models.CASCADE,related_name='myname')
    date = models.DateField()
    s_day = models.CharField(max_length=15)
    s_time = models.CharField(max_length=50)
    course_id = models.ForeignKey(addcourse, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.myname} ||{self.username} || {self.date} || {self.s_day} || {self.s_time} || {self.course_id}'











