from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django.forms import ModelForm, TextInput, PasswordInput
from webapp.models import User, Ticket, Review, UserFollows

from . import models

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"}),
                               label='')
    password = forms.CharField(max_length=30,
                               widget=forms.PasswordInput(attrs={'placeholder': "Mot de passe"}),
                               label='')


# ======================================= Logging ========================================


class SignupForm(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'}))
    password1 = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Mot de passe'}))
    password2 = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Confirmer Mot de passe'}))

    # class Meta(UserCreationForm.Meta):
    class Meta:
        # model = get_user_model()
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {'username': forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur', }),
                   'password1': forms.PasswordInput(attrs={'placeholder': "Mot de passe", }),
                   'password2': forms.PasswordInput(attrs={'placeholder': "Confirmer Mot de passe"}), }

# ============================================================================================


class TicketForm(ModelForm):
    title = forms.CharField(max_length=30, label='Titre')
    image = forms.ImageField(required=False)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']

        """
        def __init__(self, *args, **kwargs):
            super(TicketForm, self).__init__(*args, **kwargs)
            self.fields['image'].required = False
        """


class CreateReviewForm(ModelForm):
    CHOICES = [
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('3', 'Option 3'),
        ('4', 'Option 4'),
        ('5', 'Option 5'),
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
        ('5', 'Option 5'),
    ]

    headline = forms.CharField(max_length=30, label='Titre')
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, label="Note")
    body = forms.CharField(label="Commentaire", widget=forms.Textarea(attrs={}))

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']


class FollowUsersForm(forms.Form):
    followed_user = forms.CharField(label='', max_length=800,
                                    widget=forms.TextInput(
                                        attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"}))


class DeleteTicketForm(ModelForm):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
