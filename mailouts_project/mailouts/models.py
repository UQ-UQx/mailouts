from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Subscription(models.Model):
    email = models.CharField(max_length=1000, blank=False)
    opt_in = models.BooleanField(blank=False)
    opt_in_source = models.CharField(max_length=1000, blank=False)
    preference_set_datetime = models.DateTimeField(blank=True)
    full_name = models.CharField(max_length=1000, blank=False)

class StudentinCourse(models.Model):
    subscription = models.ForeignKey(Subscription)
    course_id = models.CharField(max_length=1000, blank=False)

class Newsletter(models.Model):
    sender_email = models.CharField(max_length=1000, blank=False)
    subject = models.CharField(max_length=1000, blank=False)
    email_body = models.TextField(blank=False)
    email_text = models.TextField(blank=True)
    course_criteria = models.TextField(blank=False)
    demographic_criteria = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NewsletterRecipient(models.Model):
    subscription = models.ForeignKey(Subscription)
    newsletter = models.ForeignKey(Newsletter)
    sent_flag = models.BooleanField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
