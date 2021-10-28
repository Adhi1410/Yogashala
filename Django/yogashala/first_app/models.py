from django.contrib import auth
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.db.models import F, Count

class profile(models.Model):
    username = models.CharField(max_length=40)
    first_name = models.CharField(max_length=40)
    email = models.EmailField()

    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    height = models.IntegerField()
    weight = models.IntegerField()
    bmi = models.IntegerField()
    issue = models.CharField(max_length=500)
    def __str__(self):
        return f'{self.first_name} || {self.username} || {self.email} || {self.age} || {self.weight} || {self.height} || {self.bmi} || {self.issue}\n'

class addcourse(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=15)
    duration = models.IntegerField()
    def __str__(self):
        return f'{self.id} || {self.name} || {self.duration}'

class teacher(models.Model):
    email = models.EmailField()
    cid = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f'{self.email} || {self.cid} || {self.date}'

class students(models.Model):
    email = models.EmailField()
    cid = models.IntegerField()
    date = models.DateField()
    expdate = models.DateField()
    def __str__(self):
        return f'{self.email} || {self.cid} || {self.date} || {self.expdate}'













