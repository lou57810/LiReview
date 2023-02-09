from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
import webapp.views
from webapp.views import flow_view, ask_review, owner_post_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', webapp.views.LoginPage.as_view(), name='login'),
    # path('', LoginView.as_view(template_name='webapp/login.html',
    # redirect_authenticated_user=True), name='login'),

    path('signup/', webapp.views.signup_page, name='signup'),
    path('flow/', webapp.views.flow_view, name='flow'),
    path('ask-reviews/', webapp.views.ask_review, name='ask-reviews'),  # Demande ticket
    path('view-tickets', webapp.views.owner_post_view, name='view-tickets'),          # Affichage post utilisateur.
    path('create-reviews/', webapp.views.create_review, name='create-reviews'),
    # path('update-tickets/', TicketUpdateView.as_view(), name='update-tickets'),
    #path('cover/upload/', webapp.views.cover_upload, name='cover_upload'),
    path('subscribers/', webapp.views.subscribers, name='subscribers'),
    #path('delete_ticket/<int:ticket_id>', webapp.views.delete_ticket, name='delete_ticket'),
    #path('add-reviews/', login_required(webapp.views.AddReview.as_view()), name ='add-reviews'),
    # path('critics_answer/', views.critic_response),

    # path('critic-modify/', views.critic_modify),
    #path('view_ticket/<int:ticket_id>', webapp.views.view_tickets, name='view_ticket'),
    path('logout/', webapp.views.LogoutPage.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
