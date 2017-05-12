from django.db import models
from django.utils import timezone
from registration.signals import user_registered
from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model

from django.contrib.auth.models import User
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager
import logging

class UserProfile(models.Model):
    user = models.ForeignKey('User')
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    degree = models.CharField(max_length=30)
    is_lecturer = models.BooleanField(initial=False)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE) #При удалении группы удаляются все юзеры

class Group(models.Model):
    starosta_id = models.OneToOneField(UserProfile, on_delete=models.SET_NULL)
    number = models.CharField(max_length=30)
    
class Course(models.Model):
    report_type = models.CharField(max_length=254)
    beginning_date = models.DateTimeField()
    ending_date = models.DateTimeField()
    courses = models.ManyToManyField(UserProfile)
    courses = models.ManyToManyField(Group)

class Subject(models.Model):
    name = models.CharField(max_length=254)
    is_necessary = models.BooleanField(initial=False)

class CommonMaterial(models.Model):
    text = models.TextField()
    subjects = models.ManyToManyField(Subject)

class Class(models.Model):
    conspect = models.TextField()
    homework = models.TextField()
    data = models.DateTimeField()
    is_canceled = models.BooleanField(initial=False)
    group_id = models.ForeignKey(Course, on_delete=models.CASCADE)

class ClassFormat(models.Model):
    day_of_week = models.IntegerField()
    type_of_class = models.CharField(max_length=254)
    time_of_beginning = models.TimeField()
    time_of_ending = models.TimeField()
    building = models.CharField(max_length=30)
    auditorium = models.CharField(max_length=30)
    starosta_id = models.OneToOneField(Course, on_delete=models.CASCADE)
    week_number = models.IntegerField()

class CourseMaterial(models.Model):
    text = models.TextField()
    courses = models.ManyToManyField(Course)

######################################

def user_registered_callback(sender, user, request, **kwargs):
    profile = ExUserProfile(user = user)

    profile.is_lecturer = bool(request.POST["is_lecturer"])
    profile.first_name = string(request.POST["first_name"])
    profile.middle_name = bool(request.POST["middle_name"])
    profile.last_name = bool(request.POST["last_name"])
    profile.phone_number = bool(request.POST["phone_number"])
    profile.email = bool(request.POST["email"])
    profile.degree = bool(request.POST["degree"])

    profile.save()

user_registered.connect(user_registered_callback)

class EmailBackend(object):
    def authenticate(self, username=None, password=None, **kwargs):
        logger.error('Something wrong in authentificate!')

        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if getattr(user, 'is_active', False) and  user.check_password(password):
                return user
        return None