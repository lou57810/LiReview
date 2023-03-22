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
from webapp.models import Ticket, Review, User, UserFollows
from webapp.forms import CreateTicket, TicketForm, CreateOriginalReviewForm, \
    CreateResponseReviewForm, Review, LoginForm, FollowUsersForm
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
        Q(user=request.user) | Q(user=request.user) | Q(user__in=followed_users_list)
    )

    ordered_tickets_and_reviews = sorted(chain(tickets, reviews),
                                         key=lambda instance: instance.time_created,
                                         reverse=True)

    paginator = Paginator(ordered_tickets_and_reviews, 3)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    return render(request, 'webapp/flow.html', context={'ordered_tickets_and_reviews': page_obj, 'page_obj': page_obj})


@login_required
def create_ticket(request, ticket_id=None):  # Bouton demander une critique(ask review)
    ticket_instance = (
        Ticket.objects.get(pk=ticket_id) if ticket_id is not None else None)

    if request.method == "GET":
        form = forms.CreateTicket(instance=ticket_instance)
        return render(request, 'webapp/create_ticket.html', context={'form': form})
    if request.method == "POST":
        form = forms.CreateTicket(request.POST, instance=ticket_instance)
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


@login_required
def owner_post_view(request):
    tickets = models.Ticket.objects.filter(user=request.user).order_by('-time_created')
    reviews = models.Review.objects.filter(user=request.user).order_by('-time_created')
    # redirect('view-posts')
    return render(request, "webapp/view_posts.html", {'tickets': tickets, 'reviews:': reviews})


@login_required
def add_follower(request):
    # followed_form = FollowUsersForm()
    # user = UserFollows()
    # UserFollows.followed_user = User()
    # instance = (
        # UserFollows.objects.get(pk=user_id) if user_id is not None else None)

    followed_model_users = models.UserFollows.objects.filter(user=request.user)
    following_model_users = models.UserFollows.objects.filter(followed_user=request.user)

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
            print('pos:', pos)


            # print('entry:', type(followed_user), new_followed_user)
            new_entry = UserFollows(user=request.user, followed_user=pos)
            new_entry.save()

            return redirect('subscribers')

    return render(request, 'webapp/follow_users_form.html',
                  {'followed_users': followed_users, 'followed_form': followed_form, 'follower_users': follower_users})
"""
    if request.method == "POST":
        followed_form = FollowUsersForm(request.POST)

        if followed_form.is_valid():
            followed_form.save(commit=False)
            # new_followed_user = followed_form.cleaned_data
            new_followed_user = get_object_or_404(UserFollows, id=follow_form.cleaned_data['new_followed_user'])
            if request.user.follows.filter(id=followed_user.id).exists():
                new_user = request.user

            new_entry = UserFollows(user=new_user, followed_user=new_followed_user)
            new_entry.save()
            # print('new_followed_user', new_followed_user.id)
            return redirect('subscribers')
        
        # followed_form = form.save(commit=False)

        
        if username != f'{request.user}':
            user = models.User.objects.get(id=request.user.id)
            followed_user = models.User.objects.filter(username=username)[0]
            if followed_user is not None:
                add_follower = models.UserFollows(user=user, followed_user=followed_user)
                add_follower.save()
        else:
        




@receiver(pre_save, sender=UserFollows)
def check_self_following(sender, instance, **kwargs):
    if instance.follower == instance.user:
        raise ValidationError('You can not follow yourself')
"""


@login_required
def unfollow(request, user_id):
    follower = UserFollows.objects.filter(Q(followed_user_id=user_id) & Q(user_id=request.user.id))
    follower.delete()
    # messages.success(request, "Abonné supprimé.")
    return redirect('subscribers')



@login_required
def delete_tickets(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.delete()
    return redirect('flow')
