# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-07 10:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_app02userinfo_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='app02userinfo',
            name='username',
        ),
    ]