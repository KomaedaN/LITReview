from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from . import models


class LoginForm(forms.Form):
    username = forms.CharField(max_length=25, label='',
                               widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur",
                                                             'class': "login_form"}))
    password = forms.CharField(max_length=100, label='',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe',
                                                                 'class': "login_form"}))


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)

