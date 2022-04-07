from django.contrib import admin
from nickstagram.accounts.models import Profile, NickstagramUser

admin.site.register(NickstagramUser)
admin.site.register(Profile)
