# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-10 09:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app02', '0004_auto_20170909_0821'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='ur',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app02.Role'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='title',
            field=models.CharField(max_length=64, verbose_name='组名'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='email',
            field=models.EmailField(error_messages={'required': '请输入正确格式'}, max_length=254, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='username',
            field=models.CharField(error_messages={'required': '必须填写'}, max_length=47, verbose_name='用户名'),
        ),
    ]
