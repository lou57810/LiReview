from django.contrib import admin
from webapp.models import User, Ticket, Review, UserFollows


class UserFollowsAdmin(admin.ModelAdmin):
    # Affiche liaison user et followed_user en deux colonnes dans administration
    list_display = ('user', 'followed_user')


# Affiche les elts de models.py dans administration
admin.site.register(User)
admin.site.register(Ticket)
admin.site.register(UserFollows, UserFollowsAdmin)
admin.site.register(Review)
