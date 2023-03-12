from itertools import chain
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.conf import settings
from django.forms.formsets import formset_factory
# from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms, models
from webapp.models import Ticket, Review, UserFollows
from webapp.forms import AskReview, TicketForm, CreateOriginalReviewForm, \
    CreateResponseReviewForm, Review, LoginForm, FollowUsersForm  # CreateOriginalReviewTop, CreateOriginalReviewBottom,
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from webapp.admin import UserFollowsAdmin


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
    user_id = request.user.id
    followed_users = UserFollows.objects.filter(user=user_id)
    str_followed_users = []
    for user in followed_users:
        str_followed_users.append(str(user.followed_user))

    print(models.UserFollows.objects.filter(user=request.user).values())
    print('str:', str_followed_users)

    tickets = models.Ticket.objects.order_by('-time_created')
    reviews = models.Review.objects.order_by('-time_created')
    tickets_and_reviews = []

    for ticket in tickets:
        if str(ticket.user) in str_followed_users or str(ticket.user) == str(request.user):
            for review in reviews:
                if ticket == review.ticket:
                    ticket.done = True
            tickets_and_reviews.append(ticket)

    for review in reviews:
        if str(review.user) in str_followed_users or str(review.user) == str(request.user):
            tickets_and_reviews.append(review)

    ordered_tickets_and_reviews = sorted(tickets_and_reviews,
                                         key=lambda instance: instance.time_created,
                                         reverse=True)
    return render(request, 'webapp/flow.html', context={'ordered_tickets_and_reviews': ordered_tickets_and_reviews})


@login_required
def ask_review(request, ticket_id=None):  # Bouton demander une critique
    ticket_instance = (
        Ticket.objects.get(pk=ticket_id) if ticket_id is not None else None)

    if request.method == "GET":
        form = forms.AskReview(instance=ticket_instance)
        return render(request, 'webapp/ask_review.html', context={'form': form})
    if request.method == "POST":
        form = forms.AskReview(request.POST)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()
            return redirect('flow')


@login_required
def create_original_review(request):

    if request.method == "GET":
        ticket_form = forms.TicketForm()
        review_form = forms.CreateOriginalReviewForm()
        return render(request, 'webapp/original_review.html',
                      context={'ticket_form': ticket_form, 'review_form': review_form})

    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.time_created = timezone.now()
            ticket.save()

            reviews_form = forms.CreateOriginalReviewForm(request.POST)
            reviews_ticket = Ticket.objects.get(id=ticket.id)
            review = reviews_form.save(commit=False)
            review.ticket = reviews_ticket
            review.user = request.user
            review.time_created = timezone.now()
            review.save()
            return redirect('flow')


"""
@login_required
def create_original_review(request, ticket_id=None):
    original_ticket_instance = (
        Review.objects.get(pk=ticket_id) if ticket_id is not None else None)
    if request.method == "GET":
        ticket_form = forms.TicketForm(instance=original_ticket_instance)
        review_form = forms.ReviewForm()
        return render(request, 'webapp/original_review.html',
                      context={'ticket_form': ticket_form, 'review_form': review_form})

    elif request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('flow')

@login_required
def create_response_review(request, review_id=None, ticket_id=None):
    review_instance = (
        Review.objects.get(pk=review_id) if review_id is not None else None
    )
    ticket_instance = (
        Ticket.objects.get(pk=ticket_id) if ticket_id is not None else None
    )

    if request.method == "GET":
        ticket_form = forms.TicketForm(instance=ticket_instance)  # , initial={"ticket": ticket_instance})
        review_form = forms.ReviewForm(instance=review_instance)  # , initial={"review": review_instance})
        context = {"ticket_form": ticket_form, "review_form": review_form}
        return render(request, 'webapp/response_review.html',
                      context=context)

    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.save()
            review = review_form.save(commit=False)
            # review.ticket = ticket
            name = request.user
            print('user: ', name)
            review.save()
            return redirect('flow')

"""


def create_response_review(request, ticket_id=None):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "GET":
        review_form = forms.CreateResponseReviewForm()
        return render(request, 'webapp/response_review.html', {
            'ticket': ticket, 'review_form': review_form})

    elif request.method == 'POST':
        review_form = forms.CreateResponseReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.time_created = timezone.now()
            review.save()
            return redirect('flow')
"""
if request.method == "GET":
    review_form = forms.CreateResponseReview()
    

elif request.method == 'POST':
    review_form = forms.CreateResponseReview(request.POST)

    if review_form.is_valid:
        post = review_form.save(commit=False)
        post.ticket = ticket
        post.user = request.user
        post.time_created = timezone.now()
        post.save()
"""
    # return redirect('flow')


@login_required
def owner_post_view(request):
    tickets = models.Ticket.objects.filter(user=request.user).order_by('-time_created')
    reviews = models.Review.objects.filter(user=request.user).order_by('-time_created')
    # redirect('view-posts')
    return render(request, "webapp/view_posts.html", {'tickets': tickets, 'reviews:': reviews})


@login_required
def add_follower(request):
    user_id = request.user.id
    followed_model_users = models.UserFollows.objects.filter(user=user_id)
    following_model_users = UserFollows.objects.filter(followed_user=user_id)

    follower_users = []
    followed_users = []
    for user in followed_model_users:
        followed_users.append(user)
    for user in following_model_users:
        follower_users.append(user)

    if request.method == "GET":
        followed_form = FollowUsersForm()
        return render(request, 'webapp/follow_users_form.html',
                      {'followed_users': followed_users, 'followed_form': followed_form, 'follower_users': follower_users})

    elif request.method == "POST":
        followed_form = FollowUsersForm(request.POST)
        if followed_form.is_valid():
            new_followed_user = followed_form.cleaned_data['followed_user']
            user = request.user
            # Exception: " didn't return an HttpResponse object. It returned None instead"
            # new_followed_user = followed_form.save(commit=False)
            # new_followed_user.user = request.user

            print('user:', user)
            print('new_followed_user:', new_followed_user)

            follow_relations = UserFollows(user=user, followed_user=new_followed_user)
            follow_relations.save()

            return redirect('subscribers')


@login_required
def unfollow(request, user_id):
    post = get_object_or_404(UserFollows, id=user_id)
    post.followed_user.delete()
    return redirect('subscribers')


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

"""


@login_required
def delete_tickets(request, ticket_id):
    pass
