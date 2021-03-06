# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-09 08:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app02', '0003_test1'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
            ],
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=48, verbose_name='名字'),
        ),
        migrations.AlterField(
            model_name='test1',
            name='title',
            field=models.CharField(max_length=74, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='username',
            field=models.CharField(max_length=47, verbose_name='用户名'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='ug',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app02.UserGroup'),
            preserve_default=False,
        ),
    ]
