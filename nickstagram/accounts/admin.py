from django.contrib import admin
from nickstagram.accounts.models import Profile, NickstagramUser


class NicktagramUserAdmin(admin.ModelAdmin):
    pass


class ProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(NickstagramUser, NicktagramUserAdmin)
admin.site.register(Profile, ProfileAdmin)
