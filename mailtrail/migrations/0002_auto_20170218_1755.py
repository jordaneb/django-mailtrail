# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 17:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailtrail', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='email',
            old_name='message',
            new_name='payload',
        ),
        migrations.AddField(
            model_name='email',
            name='plaintext_message',
            field=models.TextField(blank=True),
        ),
    ]