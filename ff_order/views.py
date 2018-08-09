# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import request
from ff_user import user_decorator
from ff_user.models import UserInfo
from ff_cart.models import CartInfo
from ff_order.models import OrderInfo, OrderDetailInfo
from django.shortcuts import render, redirect
from django.db import transaction
from datetime import datetime
from decimal import Decimal
# Create your views here.
@user_decorator.login
def order(request):
    # query user
    user=UserInfo.objects.get(id=request.session['user_id'])
    get = request.GET
    cart_ids=get.getlist('cart_id')
    cart_ids1=[int(item) for item in cart_ids]
    carts=CartInfo.objects.filter(id__in=cart_ids1)

    context={'title':'Submit the Order',
             'page_number':1,
             'carts':carts,
             'user':user,
             'cart_ids':','.join(cart_ids),
             }
    return render(request, 'ff_order/place_order.html', context)
'''
Transaction
1: Create order object
2: Query inventory
3: Create order detail object
4: Update inventory
5: Delete Cart
'''
@transaction.atomic()
@user_decorator.login
def order_handle(request):
    tran_id=transaction.savepoint()
    # Receive cart id
    cart_ids=request.POST.get('cart_ids')
    try:
        # create order object
        order=OrderInfo()
        now=datetime.now()
        uid=request.session['user_id']
        order.oid='%s%d'%(datetime.now().strftime('%Y%m%d%H%M%S'),uid)
        order.user_id=uid
        # print order.oid
        order.odate=now
        order.ototal=Decimal(request.POST.get('total'))
        order.save()
        # create order detail object
        cart_ids1=[int(item) for item in cart_ids.split(',')]
        for id1 in cart_ids1:
            detail=OrderDetailInfo()
            detail.order=order
            # Query ginventory
            cart=CartInfo.objects.get(id=id1)
            # Validate inventory
            goods=cart.goods
            if goods.ginventory>=cart.count: # if ginventory > purchased
                # Decrease inventory
                goods.ginventory=cart.goods.ginventory-cart.count
                goods.save()
                # update order detail
                detail.goods_id=goods.id
                detail.price=goods.gprice
                detail.count=cart.count
                detail.save()
                # Delete Cart
                cart.delete()
            else: # if Inventory < purchased
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print '========================%s'%e
        transaction.savepoint_rollback(tran_id)
    # return HttpResponse('OK)
    return redirect('/user/order/')

@user_decorator.login
def pay(request, oid):
    order=OrderInfo.objects.get(oid=oid)
    order.oIsPay=True
    order.save()
    context={'order':order}
    return render(request, 'ff_order/pay.html', context)



