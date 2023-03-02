from django.forms import ModelForm , TextInput, EmailInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *
class Creationcompte(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']



