from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

attrs = {'class':'form-control'}

class LoginForm(forms.Form):
	email = forms.CharField(widget=forms.EmailInput(attrs=attrs))
	password = forms.CharField(widget=forms.PasswordInput(attrs=attrs))

class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs=attrs))

class ChangePasswordForm(forms.Form):
	password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs))

class SignupForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs=attrs))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs))