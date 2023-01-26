from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from webapp.models import Ticket


class LoginForm(forms.Form):
    user = forms.CharField(max_length=30, label='Nom d’utilisateur')
    password = forms.CharField(max_length=30,
                               widget=forms.PasswordInput,
                               label='Mot de passe')


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username']


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description']
