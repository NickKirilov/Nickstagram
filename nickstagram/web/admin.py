from django.contrib import admin
from nickstagram.web.models import Comments, Likes


class CommentsAdmin(admin.ModelAdmin):
    pass


class LikesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Comments, CommentsAdmin)
admin.site.register(Likes, LikesAdmin)
