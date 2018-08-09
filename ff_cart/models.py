# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class CartInfo(models.Model):
    user=models.ForeignKey('ff_user.UserInfo')
    goods=models.ForeignKey('ff_goods.GoodsInfo')
    count=models.IntegerField()