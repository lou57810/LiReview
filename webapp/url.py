from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
import webapp.views
from webapp.views import flow_view, create_ticket, create_review,\
    owner_post_view, create_response_review, delete_tickets, add_follower


urlpatterns = [
    path('webapp/', include('webapp.urls')),
    path('admin/', admin.site.urls),
    path('', views.LoginPage.as_view(), name='login'),
    path('signup/', views.signup_page, name='signup'),
    path('flow/', views.flow_view, name='flow'),
    path('create-ticket/', views.create_ticket, name='create-ticket'),  # Demande ticket
    path('create-ticket/<int:ticket_id>', views.create_ticket, name='create-ticket'),  # Modifie ticket prérempli
    path('view-posts/', views.owner_post_view, name='view-posts'),
    path('create-reviews/', views.create_review, name='create-reviews'),
    path('response-reviews/', views.create_response_review, name='response-reviews'),
    path('response-reviews/<int:review_id>', views.create_response_review, name='response-reviews'),
    path('subscribers/', views.add_follower, name='subscribers'),
    path('delete-tickets/<int:ticket_id>', views.delete_tickets, name='delete-tickets'),
    path('delete-reviews/<int:review_id>', views.delete_reviews, name='delete-reviews'),
    path('logout/', views.LogoutPage.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
