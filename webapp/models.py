from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone


# import uuid


class User(AbstractUser):
    pass


"""
    
    CREATOR = "CREATOR"
    SUBSCRIBER = "SUBSCRIBER"

    ROLE_CHOICES = (
        (CREATOR, "followed_by"),
        (SUBSCRIBER, "following"),
         )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='rôle')
    
"""


class Ticket(models.Model):
    # Your Ticket model definition goes here
    # user = models.ManyToManyField(User)
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    # user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # image

    def __str__(self):
        return self.title  # + ' | ' + str(self.user)

    """
    def get_absolute_url(self):
        return reverse('my_tickets' , args=(str(self.id)))
        # return reverse('flow')
    """


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5  ? starred = models.BooleanField(default=False)
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128, help_text='Titre')
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headline  #  + ' | ' + str(self.user)


class UserFollows(models.Model):
    # Your UserFollows model definition goes here
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='following')
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='followed_by')

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user',)
    """
    def __str__(self):
        # return str(followed_user)
        return '{} follows  {}'.format(self.user, self.followed_user)
    """


