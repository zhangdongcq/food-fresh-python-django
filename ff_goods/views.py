# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.paginator import Paginator, Page
from models import TypeInfo, GoodsInfo
from ff_cart.models import CartInfo
# Create your views here.
def index(request):
    typelist = TypeInfo.objects.all()
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]
    context={
        'title': 'Home',
        'type0': type0, 'type01': type01,
        'type1': type1, 'type11': type11,
        'type2': type2, 'type21': type21,
        'type3': type3, 'type31': type31,
        'type4': type4, 'type41': type41,
        'type5': type5, 'type51': type51,
    }
    return render(request, 'ff_goods/index.html', context)

def list(request, tid, pindex, sort):
    # Type Id, Page Index, Sort Criteria
    typeinfo=TypeInfo.objects.get(pk=int(tid))
    news=typeinfo.goodsinfo_set.order_by('-id')[0:2]
    if sort == '1': #Default newest
        goods_list=GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
    elif sort == '2':#Price
        goods_list=GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
    elif sort == '3': #popularity
        goods_list=GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')
    paginator=Paginator(goods_list, 4)
    page=paginator.page(int(pindex))
    context={
        'title':typeinfo.ttitle,
        'page': page,
        'paginator': paginator,
        'typeinfo': typeinfo,
        'sort': sort,
        'news': news,
    }
    return render(request, 'ff_goods/list.html', context)

def detail(request, id):
    goods = GoodsInfo.objects.get(pk=int(id))
    goods.gclick=goods.gclick+1
    goods.save()
    news=goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {'ttitle':goods.gtype.ttitle, 'guest_cart':1,
               'title': 'Order Detail',
               'g': goods, 'news':news, 'id':id,
               'cart_count':cart_count(request),
               }
    response = render(request, 'ff_goods/detail.html', context)

    # Record visit history
    goods_ids=request.COOKIES.get('goods_ids','')
    goods_id='%d'%goods.id
    if goods_ids!='': # records exist?
        goods_ids1=goods_ids.split(',') # split to list
        if goods_ids1.count(goods_id)>=1: # remove goods record if already exists
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0, goods_id) # Add as first
        if len(goods_ids1)>=6: # remove last one if exceed six items
            del goods_ids1[5]
        goods_ids=','.join(goods_ids1)
    else:
        goods_ids=goods_id # add if no record yet
    response.set_cookie('goods_ids', goods_ids) # write into Cookies
    return response

def cart_count(request):
    if request.session.has_key('user_id'):
        return CartInfo.objects.filter(user_id=request.session['user_id']).count()
    else:
        return 0
