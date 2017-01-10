# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-10 09:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailouts', '0004_newsletters_sender_email'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Newsletters',
            new_name='Newsletter',
        ),
        migrations.RenameModel(
            old_name='NewsletterRecipients',
            new_name='NewsletterRecipient',
        ),
        migrations.RenameModel(
            old_name='Subscriptions',
            new_name='Subscription',
        ),
        migrations.RenameField(
            model_name='newsletterrecipient',
            old_name='newsletter_id',
            new_name='newsletter',
        ),
        migrations.RenameField(
            model_name='newsletterrecipient',
            old_name='subscription_id',
            new_name='subscription',
        ),
    ]
