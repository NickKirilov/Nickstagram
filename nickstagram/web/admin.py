from django.contrib import admin
from nickstagram.web.models import Likes


class LikesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Likes, LikesAdmin)
