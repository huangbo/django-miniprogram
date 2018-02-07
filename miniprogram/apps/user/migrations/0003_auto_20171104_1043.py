# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-04 10:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20171102_0917'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qqaccount',
            old_name='weibo_open_id',
            new_name='openid',
        ),
        migrations.RenameField(
            model_name='wechataccount',
            old_name='wechat_open_id',
            new_name='openid',
        ),
        migrations.RenameField(
            model_name='weiboaccount',
            old_name='weibo_open_id',
            new_name='openid',
        ),
        migrations.RemoveField(
            model_name='wechataccount',
            name='wechat_unionid',
        ),
        migrations.AddField(
            model_name='wechataccount',
            name='sessionkey',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='wechataccount',
            name='unionid',
            field=models.CharField(default='', max_length=255),
        ),
    ]
