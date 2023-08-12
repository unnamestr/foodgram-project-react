from django.contrib import admin

from .models import User, Follower


class UserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'email',)
    list_filter = ('username', 'email',)

admin.site.register(User, UserAdmin)
admin.site.register([Follower,])
