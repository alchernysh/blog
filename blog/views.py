# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import *
from .models import Post
from .forms  import LoginForm
from django.contrib.auth.decorators import login_required
import  django.contrib.auth as auth

@login_required
def index(request):
    return render(request, 'index.html')

def login(request):
    form = LoginForm(request.POST or None)
 
    if request.POST and form.is_valid():
        username = form.cleaned_data["login"]
        password = form.cleaned_data["password"]
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
 
            if request.GET.get('next') is not None:
                return redirect(request.GET['next'])
            else:
                return redirect(reverse('index'))
 
    return render(request, 'login.html', {'form': form})

@login_required
def logout(request):
    auth.logout(request)
    return render(request,'logout.html')