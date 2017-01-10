from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Subscription, StudentinCourse, Newsletter, NewsletterRecipient

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'opt_in', 'opt_in_source', 'preference_set_datetime')
    search_fields = ('full_name', 'email', 'opt_in', 'opt_in_source', 'preference_set_datetime')

class StudentinCourseAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'course_id')
    search_fields = ('subscription','course_id')

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'course_criteria', 'created_at')
    search_fields = ('subject', 'course_criteria', 'created_at')

class NewsletterRecipientAdmin(admin.ModelAdmin):
    list_display = ('subscription_id', 'newsletter_id', 'sent_flag', 'updated_at')
    search_fields = ('subscription_id', 'newsletter_id', 'sent_flag', 'updated_at')

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(StudentinCourse, StudentinCourseAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(NewsletterRecipient, NewsletterRecipientAdmin)
