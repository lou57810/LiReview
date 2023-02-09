from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django.forms import ModelForm
from webapp.models import Ticket
from webapp.models import Review

from . import models


User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label='Nom d’utilisateur')
    password = forms.CharField(max_length=30,
                               widget=forms.PasswordInput,
                               label='Mot de passe')


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username']


class AskReview(ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['user', 'title', 'description']


class CreateReview(ModelForm):
    class Meta:
        model = models.Review
        fields = ['ticket', 'rating', 'user', 'headline', 'body']


class TicketViewForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'user')


class SubscribersForm(ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ['user', 'followed_user']


class DeleteTicketView(ModelForm):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)







