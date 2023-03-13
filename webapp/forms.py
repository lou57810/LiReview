from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django.forms import ModelForm, TextInput, PasswordInput
from webapp.models import User, Ticket, Review, UserFollows

from . import models

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"}), label='')
    password = forms.CharField(max_length=30,
                               widget=forms.PasswordInput(attrs={'placeholder': "Mot de passe"}),
                               label='')


class SignupForm(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'}))
    password1 = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Mot de passe'}))
    password2 = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Confirmer Mot de passe'}))

    # class Meta(UserCreationForm.Meta):
    class Meta:
        # model = get_user_model()
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={

                'placeholder': 'Nom d\'utilisateur',
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': "Mot de passe"
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': "Confirmer Mot de passe"
            }),
        }


class AskReview(ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description']


class TicketForm(ModelForm):
    # edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description']


class CreateOriginalReviewForm(ModelForm):
    CHOICES = [
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('3', 'Option 3'),
        ('4', 'Option 4'),
        ('4', 'Option 4'),
    ]

    headline = forms.CharField(max_length=30, label='Titre')
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, label="Note")
    body = forms.CharField(label="Commentaire", widget=forms.Textarea(attrs={}))

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']


class CreateResponseReviewForm(forms.ModelForm):
    CHOICES = [
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('3', 'Option 3'),
        ('4', 'Option 4'),
        ('4', 'Option 4'),
    ]

    headline = forms.CharField(max_length=30, label='Titre')
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, label="Note")
    body = forms.CharField(label="Commentaire", widget=forms.Textarea(attrs={}))  #     {'label': 'Commentaire'}))

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
        # widgets = {'Note': forms.NumberInput(attrs={'class': 'Stars'})}
        # labels = {'Note': ''}


class FollowUsersForm(ModelForm):
    # followed_user = forms.CharField(label='')
    # widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"}),
    # required=True)

    class Meta:
        model = models.UserFollows
        fields = ['followed_user']
        # labels = {'followed_user': ' ', }       # 'Suivre d'autres utilisateurs'
        # widgets = {'followed_user': forms.TextInput(
        # attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"})}


class DeleteTicketForm(ModelForm):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
