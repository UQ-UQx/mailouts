from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Subscriptions(models.Model):
    email = models.CharField(max_length=1000, blank=False)
    opt_in = models.BooleanField(blank=False)
    opt_in_source = models.CharField(max_length=1000, blank=False)
    preference_set_datetime = models.DateTimeField(blank=True)
    full_name = models.CharField(max_length=1000, blank=False)

class StudentinCourse(models.Model):
    subscription = models.ForeignKey(Subscriptions)
    course_id = models.CharField(max_length=1000, blank=False)
