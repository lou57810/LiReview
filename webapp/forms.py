from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django.forms import ModelForm, TextInput
from webapp.models import User, Ticket, Review, UserFollows

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
        fields = ['title', 'description']


class TicketForm(ModelForm):
    # edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description']


class ReviewForm(ModelForm):
    # edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']


class CreateResponseReview(ModelForm):
    class Meta:
        model = models.Review
        fields = ['ticket', 'rating', 'user', 'headline', 'body']


class FollowUsersForm(ModelForm):
    # follower = forms.CharField(label='',
                           # widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"}),
                           # required=True)

    class Meta:
        model = UserFollows
        fields = ['followed_user']

    """
    class Meta:
        model = models.UserFollows
        fields = ['user', ]
        widgets = {
            'Follow': forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"}), }
    """

    """
    class Meta:
        model = models.UserFollows
        fields = ['follower']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.user = self.request.user
        return super().save(commit)

    """


class DeleteTicketForm(ModelForm):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
