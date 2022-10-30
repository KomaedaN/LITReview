from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from . import models


class LoginForm(forms.Form):
    username = forms.CharField(max_length=25, label="Nom d'utilisateur")
    password = forms.CharField(max_length=100, widget=forms.PasswordInput, label='Mot de passe')



