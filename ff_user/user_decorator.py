#coding=utf-8
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

# If invalid attempt, redirect to login page
def login(func):
    def login_fun(request, *args, **kwargs):
        if request.session.get('user_id'):
            return func(request, *args, **kwargs)
        else:
            red = HttpResponseRedirect('/user/login')
            red.set_cookie('url', request.get_full_path())
            '''
                127.0.0.1:8080/200/?type=10
                request.path: current path  /200
                request.get_full_path : Full path  /200/?type=10
            '''
            return red
    return login_fun