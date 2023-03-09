from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
import webapp.views
from webapp.views import flow_view, ask_review, create_original_review, \
    owner_post_view, create_response_review, delete_tickets, add_follower

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', webapp.views.LoginPage.as_view(), name='login'),
    path('signup/', webapp.views.signup_page, name='signup'),
    path('flow/', webapp.views.flow_view, name='flow'),
    path('ask-reviews/', webapp.views.ask_review, name='ask-reviews'),  # Demande ticket
    path('view-posts/', webapp.views.owner_post_view, name='view-posts'),  # Affichage post utilisateur.
    path('create-reviews/', webapp.views.create_original_review, name='create-reviews'),
    path('response-reviews/', webapp.views.create_response_review, name='response-reviews'),
    path('subscribers/', webapp.views.add_follower, name='subscribers'),
    path('subscribers/<int:user_id>', webapp.views.unfollow, name='unfollow'),
    path('delete-tickets/<int:ticket_id>', webapp.views.delete_tickets, name='delete-tickets'),

    # path('critic-modify/', views.critic_modify),
    # path('view_ticket/<int:ticket_id>', webapp.views.view_tickets, name='view_ticket'),
    path('logout/', webapp.views.LogoutPage.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
