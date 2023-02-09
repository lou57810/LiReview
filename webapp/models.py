from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone


class User(AbstractUser):
    USER = 'USER'


class Ticket(models.Model):
    # Your Ticket model definition goes here
    # user = models.ManyToManyField(User)
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    edition_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # image
    """
    def __str__(self):
        return self.title + ' | ' + str(self.user)
    
    def get_absolute_url(self):
        return reverse('my_tickets' , args=(str(self.id)))
        # return reverse('flow')
    """


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5  ? starred = models.BooleanField(default=False)
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    # Your UserFollows model definition goes here
    # REQUIRED_FIELDS = ('username')
    # username = models.OneToManyField(User, related_name='profile', unique=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    followed_user = models.IntegerField()

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user',)
