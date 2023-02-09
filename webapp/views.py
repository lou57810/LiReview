from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.conf import settings
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms, models
from webapp.models import Ticket, Review
from webapp.forms import AskReview, TicketViewForm, CreateReview, LoginForm

from django.shortcuts import get_object_or_404


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
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()
    return render(request, 'webapp/flow.html', context={'tickets': tickets, 'reviews': reviews})


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
def create_review(request):
    form = forms.AskReview()
    review = forms.CreateReview()

    if request.method == "GET":
        form = forms.AskReview()
        review = forms.CreateReview()
        context = {'form': form,
                   'review': review}
        return render(request, 'webapp/create_review.html', context=context)

    if request.method == "POST":
        form = forms.AskReview(request.POST)
        review = forms.CreateReview(request.POST)
        if all([form.is_valid(), review.is_valid()]):
            # ticket = form.save(commit=False)
            # ticket.user = request.user
            form.save()
            review.save()
            return redirect('flow')

    return render(request, 'webapp/create_review.html', context=context)


def owner_post_view(request):
    ticket = Ticket
    return render(request, 'webapp/view_tickets.html', {'ticket': ticket})


class DeleteTicketView(DeleteView):
    model = Ticket
    template_name = 'webapp/delete_post.html'


def subscribers(request):
    form = forms.SubscribersForm()
    if request.method == "GET":
        form = forms.SubscribersForm()
        return render(request, 'webapp/subscribers.html', context={'form': form})
    if request.method == "POST":
        form = forms.SubscribersForm(request.POST)
        if form.is_valid():
            # ticket = form.save(commit=False)
            # ticket.user = request.user
            form.save()
            # return redirect('flow')
    return render(request, 'webapp/subscribers.html')


# ===================================== RESERVE ================================================


"""
class AddReview(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'webapp/add_review.html'

    def post(self, request):
        form = self.form_class(request.POST)
        message = ''
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['user'],
                # password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('add-reviews')
            message = 'Identifiant ou passe invalides.'
        return render(
            request, self.template_name, context={'form': form, 'message': message}
        )
        
        
def view_tickets(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    return render(request, 'webapp/view_tickets.html', context={'ticket': ticket})



def critic_response(request):
    return HttpResponse('<h1>Création critique en réponse</h1>')


def view_own_post(request):
    return HttpResponse('<h1>Voir vos posts</h1>')


def critic_modify(request):
    return HttpResponse('<h1>Modifier votre propre critique</h1>')


def ticket_modify(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    return render(request, 'webapp/flow.html')


def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    ticket.delete()
    return redirect('flow')



class AddPostView(CreateView):
    model = Ticket
    form_class = TicketPost
    template_name = 'add_post.html'


def cover_upload(request):
    form = forms.PhotoForm()
    if request.method == 'POST':
        form = forms.PhotoForm(request.POST, request.FILES)
        cover = form.save(commit=False)
        cover.uploader = request.user
        cover.save()
        return redirect('home')
    return render(request, 'webapp/cover_upload.html', context={'form': form})
    
    
class AddTicketView(LoginRequiredMixin, CreateView):

    form_class = forms.TicketPostForm
    template_name = 'webapp/add_ticket.html'

    def post(self, request):
        self.form_class = TicketPostForm
        form = self.form_class(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.uploader = request.user
            form.save()
            return redirect('flow')

        return render(request, self.template_name, context={'form': form})

# @login_required
def post_tickets(request, ticket_id=None):
    instance_ticket = Ticket.objects.get(pk=ticket_id) if ticket_id is not None else None
    if request.method == "GET":
        form = TicketForm(instance=instance_ticket)
        return render(request, 'webapp/post_tickets.html', context={'form': form})
    elif request.method == "POST":
        form = TicketForm(request.POST, instance=instance_ticket)
        if form.is_valid():
            instance = form.save()
            return redirect('flow')
            
            
class TicketUpdateView(CreateView):
    model = Ticket
    form_class = TicketPostForm
    template_name = 'webapp/ticket_update.html'
    # fields = ['title', 'description']
"""
