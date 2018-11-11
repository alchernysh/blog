# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import *
from .models import Note
from .forms  import LoginForm,SignupForm,EmailForm,ChangePasswordForm,NoteForm
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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.context_processors import csrf
from django.utils import timezone

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
    return redirect('notes')

def login(request):
    form = LoginForm(request.POST or None)
    context = {'form':form}
    if request.POST and form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = User.objects.get(email=email)
        user = auth.authenticate(username=user.username, password=password)
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
    return redirect(reverse('index'))

def signup(request):
    form = SignupForm(request.POST or None)
    context = {'form':form}
    if request.POST and form.is_valid():
        user_email = form.cleaned_data.get('email')
        users_with_email = User.objects.filter(email=user_email)
        if len(users_with_email)>0:
            context['invalid_email'] = True
            return render(request, './registration/signup.html',context)
        user_password1 = form.cleaned_data.get('password1')
        user_password2 = form.cleaned_data.get('password2')
        if user_password1 != user_password2:
            context['different_passwords'] = True
            return render(request, './registration/signup.html',context)
        user = User.objects.create_user(username=user_email,password=user_password1,email=user_email)
        #user = form.save(commit=False)
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
        #auth.login(request, user)
        return render(request,'./registration/signup_success.html')
    else:
        return render(request,'./registration/signup_failure.html')

def change_password(request, uidb64, token):
    form = ChangePasswordForm(request.POST or None)
    context = {'form':form}
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is None or confirmation_token.check_token(user, token) == False:
        return render(request,'./changing_password/change_password_failure.html')
    else:
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
        return render(request, './changing_password/change_password.html',context)

@login_required
def notes(request):
    current_user = request.user
    note_list = Note.objects.filter(user=current_user).order_by('-posted_date')
    paginator = Paginator(note_list, 2)
    page = request.GET.get('page')
    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        notes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        notes = paginator.page(paginator.num_pages)
    return render(request,'./notes/notes_list.html', {"notes": notes} )

@login_required
def note_new(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        note = form.save(commit=False)
        note.user = request.user
        note.published_date = timezone.now()
        note.save()
        context = {
        "form":form
        }
        context.update(csrf(request))
        return redirect('notes')
    else:
        form = NoteForm( initial = {})
        context = {
        "form":form
        }
        context.update(csrf(request))
        return render(request,'./notes/note_new.html',context)

@login_required
def note_edit(request, id=None):
    if id:
        note = get_object_or_404(Note, id=id)
    form = NoteForm(request.POST or None, instance=note)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('notes')
    return render(request,'./notes/note_edit.html', {'form': form})

@login_required
def note_detail(request, id):
    note = get_object_or_404(Note, id=id)
    return render(request, './notes/note_detail.html', {'note': note})

@login_required
def note_delete(request, id=None):
    if id:
        note = get_object_or_404(Note, id=id)
        note.delete()
    return redirect('notes')