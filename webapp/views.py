from itertools import chain
from django.views.generic import View
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms, models
from webapp.models import Ticket, Review, User, UserFollows
from webapp.forms import TicketForm, CreateReviewForm, \
    CreateResponseReviewForm, LoginForm, FollowUsersForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from webapp.admin import UserFollowsAdmin
from django.core.paginator import Paginator
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib import messages


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
    followed_users_list = []
    for user in UserFollows.objects.filter(user=request.user):
        followed_users_list.append(user.followed_user)

    tickets = Ticket.objects.filter(
        Q(user=request.user) | Q(user__in=followed_users_list)
    )
    reviews = Review.objects.filter(
        Q(user=request.user) | Q(user=request.user) | Q(user__in=followed_users_list))

    ordered_tickets_and_reviews = sorted(chain(tickets, reviews),
                                        key=lambda instance: instance.time_created,
                                        reverse=True)

    paginator = Paginator(ordered_tickets_and_reviews, 3)
    page = request.GET.get('page')
    page_post = paginator.get_page(page)

    return render(request, 'webapp/flow.html', context={'tickets': tickets, 'page_post': page_post})


@login_required
def create_ticket(request):
    if request.method == "GET":
        ticket_form = forms.TicketForm()
        return render(request, 'webapp/create_ticket.html', context={'ticket_form': ticket_form})

    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            new_ticket = ticket_form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()
            return redirect('flow')


@login_required
def create_review(request):
    if request.method == "GET":
        ticket_form = forms.TicketForm()
        review_form = forms.CreateReviewForm()
        return render(request, 'webapp/create_review.html',
                      context={'ticket_form': ticket_form, 'review_form': review_form})

    if request.method == "POST":
        review_form = forms.CreateReviewForm(request.POST)
        ticket_form = forms.TicketForm(request.POST, request.FILES)

        if any([review_form.is_valid(), ticket_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            # post.time_created = timezone.now()
            ticket.save()

            review_ticket = Ticket.objects.get(id=ticket.id)
            review = review_form.save(commit=False)
            review.ticket = review_ticket
            review.user = request.user
            # post.time_created = timezone.now()
            review.save()
            return redirect('flow')


def create_response_review(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    review_form = forms.CreateResponseReviewForm(request.POST)

    if request.method == "GET":
        # review_form = forms.CreateResponseReviewForm()
        return render(request, 'webapp/response_review.html', context={
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


@login_required
def owner_post_view(request):
    tickets = models.Ticket.objects.filter(user=request.user).order_by('-time_created')
    reviews = models.Review.objects.filter(user=request.user).order_by('-time_created')
    ordered_tickets_and_reviews = sorted(chain(tickets, reviews),
                                         key=lambda instance: instance.time_created,
                                         reverse=True)

    paginator = Paginator(ordered_tickets_and_reviews, 3)
    page = request.GET.get('page')
    page_post = paginator.get_page(page)

    return render(request, "webapp/view_posts.html", context={'page_post': page_post, 'tickets': tickets, 'reviews': reviews})


@login_required
def add_follower(request):

    followed_model_users = models.UserFollows.objects.filter(user=request.user)
    following_model_users = models.UserFollows.objects.filter(followed_user=request.user)
    followed_form = FollowUsersForm()

    follower_users = []
    followed_users = []
    for user in followed_model_users:
        followed_users.append(user)
    for user in following_model_users:
        follower_users.append(user)
    # ======================================
    if request.method == "GET":
        followed_form = FollowUsersForm()
    # ======================================
    elif request.method == 'POST':
        followed_form = FollowUsersForm(request.POST)
        # print('followed_form:', followed_form)
        if followed_form.is_valid():
            followed_user = followed_form.cleaned_data['followed_user']

            pos = User.objects.filter(username=followed_user)[0]

            new_entry = UserFollows(user=request.user, followed_user=pos)
            new_entry.save()

            return redirect('subscribers')

    return render(request, 'webapp/follow_users_form.html',
                  {'followed_users': followed_users,
                   'followed_form': followed_form,
                   'follower_users': follower_users})


@login_required
def unfollow(request, user_id):
    follower = UserFollows.objects.filter(Q(followed_user_id=user_id) & Q(user_id=request.user.id))
    follower.delete()
    # messages.success(request, "Abonné supprimé.")
    return redirect('subscribers')


@login_required
def update_ticket(request, ticket_id):
    ticket_instance = get_object_or_404(Ticket, id=ticket_id)
    if request.method == "GET":
        ticket_form = forms.TicketForm(instance=ticket_instance)
        return render(request, 'webapp/update_ticket.html', context={'ticket_form': ticket_form})

    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES, instance=ticket_instance)
        if ticket_form.is_valid():
            new_ticket = ticket_form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()
            return redirect('view-posts')



@login_required
def update_review(request, review_id):
    review_instance = get_object_or_404(Review, id=review_id)
    if request.method == "GET":
        review_form = forms.CreateReviewForm(instance=review_instance)
        return render(request, 'webapp/update_review.html', context={'review_form': review_form})

    if request.method == "POST":
        review_form = forms.CreateReviewForm(request.POST, request.FILES, instance=review_instance)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.user = request.user
            new_review.save()
            return redirect('view-posts')


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.delete()
    return redirect('flow')


@login_required
def delete_review(request, review_id):
    # ticket = get_object_or_404(Ticket, id=ticket_id)
    review = get_object_or_404(Review, id=review_id)
    # ticket.delete()
    review.delete()
    return redirect('flow')
