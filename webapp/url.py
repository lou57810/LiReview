from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
import webapp.views
from webapp.views import flow_view, ask_review, create_original_review,\
    owner_post_view, create_response_review, delete_tickets, add_follower


urlpatterns = [
    path('webapp/', include('webapp.urls')),
    path('admin/', admin.site.urls),
    path('', views.LoginPage.as_view(), name='login'),
    path('signup/', views.signup_page, name='signup'),
    path('flow/', views.flow_view, name='flow'),
    path('ask-reviews/', views.ask_review, name='ask-reviews'),  # Demande ticket
    path('view-posts/', views.owner_post_view, name='view-posts'),          # Affichage post utilisateur.
    path('create-reviews/', views.create_original_review, name='create-reviews'),
    path('response-reviews/', views.create_response_review, name='response-reviews'),
    path('subscribers/', views.add_follower, name='subscribers'),
    path('delete-tickets/<int:ticket_id>', views.delete_tickets, name='delete-tickets'),

    # path('critic-modify/', views.critic_modify),
    # path('view_ticket/<int:ticket_id>', webapp.views.view_tickets, name='view_ticket'),
    path('logout/', views.LogoutPage.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
