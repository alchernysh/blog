# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import *
from .models import Post
from .forms  import LoginForm,SignupForm,EmailForm,ChangePasswordForm
from django.contrib.auth.decorators import login_required
import  django.contrib.auth as auth
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import confirmation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site

def get_token(user):
    return confirmation_token.make_token(user)

def get_uid(user):
    return urlsafe_base64_encode(force_bytes(user.pk))

def get_email_message(request,user_email,email_template,email_subject):
    current_site = get_current_site(request)
    user = User.objects.get(email=user_email)
    parameters = {}
    parameters['user'] = user
    parameters['domain'] = current_site.domain
    parameters['uid'] = get_uid(user)
    parameters['token'] = get_token(user)
    message = render_to_string(email_template,parameters)
    return EmailMessage(email_subject,message,to=[user_email])

@login_required
def index(request):
    return render(request, 'index.html')

def login(request):
    form = LoginForm(request.POST or None)
    context = {'form':form}
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
        else:
            context['invalid'] = True
            return render(request, './authentication/login.html',context)        
    return render(request, './authentication/login.html', context)

def email_confirmation(request):
    form = EmailForm(request.POST or None)
    context = {'form':form}
    if request.POST and form.is_valid():
        user_email =  form.cleaned_data["email"]
        try:
            email_subject = 'Смена пароля.'
            email_template = './changing_password/change_password_email.html'
            email = get_email_message(request,user_email,email_template,email_subject)
            email.send()
            return render(request,'./changing_password/email_confirmation_success.html')
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            context['invalid'] = True
            return render(request, './changing_password/email_confirmation.html',context)
    return render(request, './changing_password/email_confirmation.html', context)

@login_required
def logout(request):
    auth.logout(request)
    return render(request,'./authentication/logout.html')

def signup(request):
    form = SignupForm(request.POST or None)
    context = {'form':form}
    if request.POST and form.is_valid():
        user_email = form.cleaned_data.get('email')
        users_with_email = User.objects.filter(email=user_email)
        if len(users_with_email)>0:
            context['invalid'] = True
            return render(request, './registration/signup.html',context)
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        email_subject = 'Подтверждение регистрации.'
        email_template = './registration/acc_active_email.html'
        email = get_email_message(request,user_email,email_template,email_subject)
        email.send()
        return render(request,'./registration/create_user_success.html')
    return render(request, './registration/signup.html',context)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and confirmation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return render(request,'./registration/signup_success.html')
    else:
        return render(request,'./registration/signup_failure.html')

def change_password(request, uidb64, token):
    form = ChangePasswordForm(request.POST or None)
    context = {'form':form}
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    if user is not None and confirmation_token.check_token(user, token):
        if request.POST and form.is_valid():
            password1 = request.POST["password1"]
            password2 = request.POST["password2"]
            if password1 != password2:
                context['invalid'] = True
                return render(request, './changing_password/change_password.html',context)
            user.set_password(password1)
            user.save()
            return render(request,'./changing_password/change_password_success.html')
        else:
            return render(request, './changing_password/change_password.html',context)
    else:
        return render(request,'./changing_password/change_password_failure.html')
    return render(request, './changing_password/change_password.html',context)
