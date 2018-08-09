# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator, Page
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from ff_goods.models import GoodsInfo
from ff_order.models import OrderInfo
from hashlib import sha1

from models import *
from hashlib import sha1
import user_decorator
# Create your views here.
def register(request):
    context = {'title': 'User Signup'}
    return render(request, 'ff_user/register.html', context)
def register_handle(request):
    # Get user input
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('pwd')
    ucpwd=post.get('cpwd')
    uemail=post.get('email')
    uphone= post.get('phone')
    # validate password consistency
    if upwd != ucpwd:
        return redirect('/user/register/')
    # Encrpy password
    s1=sha1()
    s1.update(upwd)
    upwd3=s1.hexdigest()
    # create object
    user=UserInfo()
    user.uname=uname
    user.upwd=upwd3
    user.uemail=uemail
    user.uphone=uphone
    user.save()
    # Register successfully
    return redirect('/user/login/')

def register_exist(request):
    user_name=request.GET.get('user_name')
    count=UserInfo.objects.filter(uname=user_name).count()
    # print count
    # print uname
    return JsonResponse({'count': count})

# Login Screen
def login(request):
    uname=request.COOKIES.get('uname','')
    context={'title':'User Login', 'error_name': 0, 'error_pwd': 0, 'uname':uname}
    return render(request, 'ff_user/login.html', context)
def login_handle(request):
    # Get user input
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('pwd')
    # print upwd
    # print uname
    rememberMe=post.get('rememberMe', 0)
    # Query user info
    users=UserInfo.objects.filter(uname=uname)  # return [] if no record
    # print uname
    # Wrong username if no such user in database entry exists.
    # Wrong password?
    # Redirect to User Portal
    if len(users) == 1:
        s1=sha1()
        s1.update(upwd)
        if s1.hexdigest()==users[0].upwd:
            red = HttpResponseRedirect('/user/info/')
            # Remember Username
            if rememberMe!=0:
                red.set_cookie('user_name', uname)
            else:
                red.set_cookie('user_name', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {'title': 'User Login', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'ff_user/login.html', context)
    else:
        context = {'title': 'User Login', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'ff_user/login.html', context)

#Logout
def logout(request):
    request.session.flush()
    return redirect("/goods/")


@user_decorator.login
def info(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    goods_ids = request.COOKIES.get('goods_ids','')
    goods_ids1 = goods_ids.split(',')
    # goods_list = GoodsInfo.objects.filter(id__in=goods_ids)
    goods_list=[]
    if len(goods_ids):
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))
    context = {'text': 'User Center',
               'user_email': user.uemail,
               'user_phone': user.uphone,
               'user_address': user.uaddress,
               'user_receipt': user.ureceipt,
               'user_name': request.session['user_name'],
               'goods_list': goods_list,
               'page_name': 1,
               }
    return render(request, 'ff_user/user_center_info.html', context)
@user_decorator.login
def order(request, pindex):
    order_list=OrderInfo.objects.filter(user_id=request.session['user_id']).order_by('-oid')
    paginator=Paginator(order_list, 1)
    if pindex=="":
        pindex=1
    page=paginator.page(int(pindex))
    context={'title':'User Center',
             'paginator':paginator,
             'page': page,}
    return render(request, 'ff_user/user_center_order.html', context)
@user_decorator.login
def site(request):
    user=UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ureceipt=post.get('ureceipt')
        user.uaddress=post.get('uaddress')
        user.uzip=post.get('uzip')
        user.uphone=post.get('uphone')
        user.save()
    context = {'title':'User Center', 'user': user}
    return render(request, 'ff_user/user_center_site.html', context)

