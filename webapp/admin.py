from django.contrib import admin
from webapp.models import User, Ticket, Review, UserFollows


class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ('user', 'followed_user')


admin.site.register(User)
admin.site.register(Ticket)
admin.site.register(UserFollows, UserFollowsAdmin)
admin.site.register(Review)


