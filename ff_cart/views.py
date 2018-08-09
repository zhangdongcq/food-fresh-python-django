# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from ff_user import user_decorator
from django.shortcuts import render, redirect
from models import *

# Create your views here.
@user_decorator.login
def cart(request):
    uid=request.session['user_id']
    carts=CartInfo.objects.filter(user_id=uid)
    context={
        'title': 'User Cart',
        'page_name': 1,
        'carts': carts,
    }
    return render(request, 'ff_cart/cart.html', context)

@user_decorator.login
def add(request, gid, count):
    # User uid purchased product with gid and quantity is count
    uid=request.session['user_id']
    gid=int(gid)
    count=int(count)
    # validate the remians in cart, if no record, add, otherwise create new one
    carts=CartInfo.objects.filter(user_id=uid,goods_id=gid)
    if len(carts)>=1:
        cart=carts[0]
        cart.count=cart.count+count
    else:
        cart=CartInfo()
        cart.user_id=uid
        cart.goods_id=gid
        cart.count=count
    cart.save()
    # if it is ajax request, then return json, otherwise cart
    if request.is_ajax():
        count=CartInfo.objects.filter(user_id=request.session['user_id']).count()
        return JsonResponse({'count':count, 'cart_id':cart.id})


@user_decorator.login
def edit(request, cart_id, count):
    try:
        cart=CartInfo.objects.get(pk=int(cart_id))
        count1=cart.count=int(count)
        cart.save()
        data={'ok':0}
    except Exception as e:
        data={'ok': count1}
    return JsonResponse(data)
@user_decorator.login
def delete(request, cart_id):
    try:
        cart=CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data={'ok':1}
    except Exception as e:
        data={'ok':0}
    return JsonResponse(data)