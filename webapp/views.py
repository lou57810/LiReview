from itertools import chain
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.conf import settings
from django.forms.formsets import formset_factory
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms, models
from webapp.models import Ticket, Review, UserFollows
from webapp.forms import AskReview, TicketForm, ReviewForm,\
     CreateResponseReview, Review, LoginForm, FollowUsersForm  # CreateOriginalReviewTop, CreateOriginalReviewBottom,
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import HttpResponse


# ================== LOGIN =========================================
# Login défini dans url.py

class LoginPage(View):
    form_class = forms.LoginForm
    template_name = 'webapp/login.html'

    def get(self, request):
        form = self.form_class
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        message = ''
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('flow')
            else:
                message = 'identifiants invalides.'
        return render(request, self.template_name, context={'form': form, 'message': message})


class LogoutPage(View):
    def get(self, request):
        logout(request)
        return redirect('login')


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'webapp/signup.html', context={'form': form})


# ============================= PAGES =================================================

@login_required
def flow_view(request):
    tickets = models.Ticket.objects.all() #  filter(
        # Q(contributors__in=request.user.followed_user.all()) |
        # Q(starred=True)
    #)
    reviews = models.Review.objects.all() # filter(
        # uploader__in=request.user.followed_user.all()
    # ).exclude(blog__in=tickets)

    tickets_and_reviews = sorted(chain(tickets, reviews),
                                 key=lambda instance: instance.time_created,
                                 reverse=True)
    return render(request, 'webapp/flow.html', context={'tickets_and_reviews': tickets_and_reviews})


@login_required
def ask_review(request):                # Bouton demander une critique
    # form = forms.AskReview()
    if request.method == "GET":
        form = forms.AskReview()
        return render(request, 'webapp/ask_review.html', context={'form': form})
    if request.method == "POST":
        form = forms.AskReview(request.POST)
        if form.is_valid():
            form.save()
            return redirect('flow')

    # return render(request, 'webapp/ask_review.html', context={'form': form})


@login_required
def create_original_review(request):
    # ticket = get_object_or_404(models.Ticket, id=review_id)
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method =='POST':
        ticket_form = forms.TicketForm(request.POST)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.save()
            return redirect('response-reviews')

    return render(request, 'webapp/original_review.html',
                  context={'ticket_form': ticket_form, 'review_form': review_form})


@login_required
def create_response_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.save()
            return redirect('flow')

    return render(request, 'webapp/response_review.html',
                  context={'ticket_form': ticket_form, 'review_form': review_form})


@login_required
def owner_post_view(request):
    # tickets = models.Ticket.objects.all()
    # reviews = models.Review.objects.all()
    # if request.method == "GET":
    tickets = models.Ticket.objects.filter(user=request.user)
    reviews = models.Review.objects.filter(user=request.user)
    # redirect('view-posts')
    return render(request, "webapp/view_posts.html", {'tickets': tickets, 'reviews:': reviews})


@login_required
def add_follower(request):
    # users = models.User.objects.all()
    if request.method == 'GET':
        followed_form = FollowUsersForm()
        return render(request, 'webapp/follow_users_form.html', {'followed_form': followed_form})

    elif request.method == 'POST':
        followed_form = FollowUsersForm(request.POST)

        if followed_form.is_valid():
            user = request.user
            user_followed = followed_form.cleaned_data['followed_user']
            # follower = models.User.objects.filter(username=user)
            UserFollows.unique_together = (user.username, user_followed.username)
            print('uniquetogether:', UserFollows.unique_together)
            # UserFollows.unique_together.save()
            return redirect('subscribers')
    """
    user = models.User.objects.filter(username=follower)
    # post = UserFollows.objects.create(user=follower)

    # unique_together.save()
    user = request.user
    UserFollows.unique_together = (user.username, follower)
    print('uniquetogether:', UserFollows.unique_together)
    print('u0:', UserFollows.unique_together[1])

    # usr_follow_tuple.follower = follower.username

    # follower = followed_form.save()

    # print('follower:', request.user )
    
    # return HttpResponse(follower)
    """

    # followers = models.UserFollows.objects.all()
    # followed_form = forms.FollowUsersForm(request.POST)
    # return render(request, 'webapp/follow_users_form.html', {'followers': followers, 'followed_form': followed_form})


"""
    if request.method == 'POST':
        followed_form = forms.FollowUsersForm(request.POST)
        if followed_form.is_valid():
            followed_name = followed_form.cleaned_data['user_name']
            follower = UserFollows.objects.create(user_name=followed_name)
            follower.save()
            return HttpResponse('Username:' + follower.followed_name)
            #user = followed_form.save(commit=False)
            # follower.save()
            #print("user:\n", user)
            # unique_together.save()
            # print('unique_together:', unique_together)
            #return redirect('subscribers')
    followed_form = FollowUsersForm()
    return render(request, 'webapp/follow_users_form.html', {'followed_form': followed_form})
    #return render(request, 'webapp/follow_users_form.html',
                  #context={'user': user, 'followers': followers, 'followed_form': followed_form})
"""

@login_required
def modify_review(request, review_id):
    review = Review.objects.get(id=review_id)

    if request.method == 'POST':
        review_modify_form = ReviewForm(request.POST, instance=review)
        if review_modify_form.is_valid():
            # mettre à jour le groupe existant dans la base de données
            review_modify_form.save()
            # rediriger vers la page détaillée du groupe que nous venons de mettre à jour
            return redirect('review-detail', review.id)
    else:
        review = ReviewForm(instance=review)

    return render(request,
                  'webapp/modify_review.html',
                  {'review_modify_form': review_modify_form})


@login_required
def delete_tickets(request, ticket_id):
    pass




