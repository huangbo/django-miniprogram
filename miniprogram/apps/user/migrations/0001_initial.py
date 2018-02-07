# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-02 05:26
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(blank=True, default='', max_length=150)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('gender', models.CharField(blank=True, choices=[('male', '男'), ('female', '女'), ('unknown', '未知')], default='unknown', max_length=10)),
                ('avatar_url', models.URLField(blank=True, default='')),
                ('edu', models.CharField(blank=True, choices=[('junior', '专科'), ('undergraduate', '本科'), ('master', '硕士'), ('doctor', '博士'), ('other', '其他')], default='other', max_length=10)),
                ('career', models.CharField(blank=True, default='', max_length=150)),
                ('married', models.CharField(blank=True, choices=[('yes', '已婚'), ('no', '未婚'), ('unknown', '未知')], default='unknown', max_length=10)),
                ('mobile', models.CharField(max_length=12, null=True, unique=True)),
                ('mobile_verified', models.BooleanField(default=False)),
                ('email', models.CharField(max_length=80, null=True, unique=True)),
                ('email_verified', models.BooleanField(default=False)),
                ('identity', models.CharField(max_length=80, null=True, unique=True)),
                ('identity_verified', models.BooleanField(default=False)),
                ('subscribed', models.BooleanField(default=False)),
                ('channel', models.CharField(blank=True, default='', max_length=150)),
                ('last_login', models.DateTimeField()),
                ('status', models.IntegerField(blank=True, choices=[(1, 'valid'), (0, 'invalid')], default=1)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
                'swappable': 'AUTH_USER_MODEL',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='QQAccount',
            fields=[
                ('weibo_open_id', models.CharField(max_length=190, primary_key=True, serialize=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='qq_account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WechatAccount',
            fields=[
                ('wechat_open_id', models.CharField(max_length=190, primary_key=True, serialize=False)),
                ('wechat_unionid', models.CharField(default=' ', max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wechat_account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WeiboAccount',
            fields=[
                ('weibo_open_id', models.CharField(max_length=190, primary_key=True, serialize=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='weibo_account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
