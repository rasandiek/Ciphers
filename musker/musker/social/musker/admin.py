from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Ciphers
# Unregister Groups
admin.site.unregister(Group)


# Mix profile info into user info
class ProfileInline(admin.StackedInline):
    model = Profile


# Extend user model
class UserAdmin(admin.ModelAdmin):
    model=User
    #Just display username fields on admin page
    fields = ["username"]
    inlines = [ProfileInline]


# Unregister initial user as it was previously registered and we need to remove certain parts of it
admin.site.unregister(User)
# Reregister new user and profile
admin.site.register(User, UserAdmin)

#Register Ciphers
admin.site.register(Ciphers)