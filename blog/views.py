# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import *
from .models import Post
from .forms  import LoginForm,SignupForm
from django.contrib.auth.decorators import login_required
import  django.contrib.auth as auth
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site

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

def get_token(user):
    return account_activation_token.make_token(user)

def get_uid(user):
    return urlsafe_base64_encode(force_bytes(user.pk))

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': get_uid(user),
                'token': get_token(user),
            })
            print get_uid(user)+"/"+get_token(user)
            mail_subject = 'Подтверждение регистрации.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('На Ваш электронный адрес отправлено письмо с сылкой для подтверждения регистрации. Перейдите по ссылке, чтобы завершить регистрацию.')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return render(request,'signup_success.html')
    else:
        return render(request,'signup_failure.html')