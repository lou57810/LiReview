"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import webapp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', webapp.views.LoginPage.as_view(), name='login'),
    # template_name='webapp/login.html',
    # redirect_authenticated_user=True
    path('signup/', webapp.views.signup_page, name='signup'),
    path('flux/', webapp.views.flux, name='flux'),
    path('cover/upload/', webapp.views.cover_upload, name='cover_upload'),
    path('subscribers/', webapp.views.subscribers, name='subscribers'),
    path('posts/', webapp.views.posts, name='posts'),
    # path('tickets/', views.create_ticket, name='ticket),
    # path('critics/', views.critic_create),
    # path('critics_answer/', views.critic_response),
    # path('own-posts/', views.view_own_post),
    # path('critic-modify/', views.critic_modify),
    # path('ticket-modify/', views.ticket_modify),
    path('logout/', webapp.views.LogoutPage.as_view(), name='logout'),

]
