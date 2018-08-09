# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserInfo(models.Model):
    uname=models.CharField(max_length=20)
    upwd=models.CharField(max_length=40)
    uemail=models.CharField(max_length=30)
    ureceipt=models.CharField(max_length=20, default="")
    uaddress=models.CharField(max_length=100, default="")
    uzip=models.CharField(max_length=6, default="")
    uphone=models.CharField(max_length=10, default="")
    ucomment=models.CharField(max_length=100, default="")
    #default, blank is constraint for Python. No affect on Database structures