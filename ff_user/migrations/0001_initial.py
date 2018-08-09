# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-07-22 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=20)),
                ('upwd', models.CharField(max_length=40)),
                ('uemail', models.CharField(max_length=30)),
                ('ureceipt', models.CharField(max_length=20)),
                ('uaddress', models.CharField(max_length=100)),
                ('uzip', models.CharField(max_length=6)),
                ('uphone', models.CharField(max_length=10)),
                ('ucomment', models.CharField(max_length=100)),
            ],
        ),
    ]
