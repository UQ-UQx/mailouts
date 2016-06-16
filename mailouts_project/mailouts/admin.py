from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Subscriptions, StudentinCourse

class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'opt_in', 'opt_in_source', 'preference_set_datetime')
    search_fields = ('full_name', 'email', 'opt_in', 'opt_in_source', 'preference_set_datetime')

class StudentinCourseAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'course_id')
    search_fields = ('subscription','course_id')

admin.site.register(Subscriptions, SubscriptionsAdmin)
admin.site.register(StudentinCourse, StudentinCourseAdmin)
