from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
import webapp.views

from webapp.views import flow_view, create_ticket, create_review, \
    owner_post_view, create_response_review, add_follower, update_ticket

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', webapp.views.LoginPage.as_view(), name='login'),
    path('signup/', webapp.views.signup_page, name='signup'),
    path('flow/', webapp.views.flow_view, name='flow'),
    path('create-tickets/', webapp.views.create_ticket, name='create-tickets'),  # create ticket
    path('create-reviews/', webapp.views.create_review, name='create-reviews'),
    path('view-posts/', webapp.views.owner_post_view, name='view-posts'),  # Affichage post utilisateur.
    path('update-tickets/<int:ticket_id>', webapp.views.update_ticket, name='update-tickets'),
    path('update-reviews/<int:review_id>', webapp.views.update_review, name='update-reviews'),
    # path('update-reviews/<int:ticket_id>', webapp.views.update_review, name='update-reviews'),
    path('response-reviews/<int:ticket_id>', webapp.views.create_response_review, name='response-reviews'),
    path('response-reviews/', webapp.views.create_response_review, name='response-reviews'),
    path('subscribers/', webapp.views.add_follower, name='subscribers'),
    path('subscribers/<int:user_id>', webapp.views.unfollow, name='unfollow'),
    path('delete-tickets/<int:ticket_id>', webapp.views.delete_ticket, name='delete-tickets'),
    path('delete-reviews/<int:review_id>', webapp.views.delete_review, name='delete-reviews'),
    path('logout/', webapp.views.LogoutPage.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
