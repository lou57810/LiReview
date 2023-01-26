from django.views.generic import View
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.shortcuts import render, redirect
from . import forms, models
from webapp.models import Ticket


@login_required
def flux(request):
    return render(request, 'webapp/flux.html')


class LoginPage(View):
    form_class = forms.LoginForm
    template_name = 'webapp/login.html'

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(
            request, self.template_name, context={'form': form, 'message': message}
        )

    def post(self, request):
        form = self.form_class(request.POST)
        message = ''
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['user'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('flux')
            message = 'Identifiant ou passe invalides.'
        return render(
            request, self.template_name, context={'form': form, 'message': message}
        )


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


@login_required
def cover_upload(request):
    form = forms.PhotoForm()
    if request.method == 'POST':
        form = forms.PhotoForm(request.POST, request.FILES)
        cover = form.save(commit=False)
        cover.uploader = request.user
        cover.save()
        return redirect('home')
    return render(request, 'webapp/cover_upload.html', context={'form': form})


def subscribers(request):
    return render(request, 'webapp/subscribers.html')


def posts(request):
    return render(request, 'webapp/posts.html')


def create_ticket(request):
    form = TicketForm()
    return render(request, 'add_ticket.html', {'form': form})


def list_ticket(request):
    tickets = Ticket.objects.all()
    return render(request, 'list_tickets.html', {'tickets': tickets})



def critic_create(request):
    return HttpResponse('<h1>Création critique</h1>')


def critic_response(request):
    return HttpResponse('<h1>Création critique en réponse</h1>')


def view_own_post(request):
    return HttpResponse('<h1>Voir vos posts</h1>')


def critic_modify(request):
    return HttpResponse('<h1>Modifier votre propre critique</h1>')


def ticket_modify(request):
    return HttpResponse('<h1>Modifier votre propre ticket</h1>')

"""

def logout_user(request):
    logout(request)
    return redirect('login')



def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                message = 'Identifiants invalides.'
    return render(
        request, 'authentication/login.html', context={'form': form, 'message': message})
"""