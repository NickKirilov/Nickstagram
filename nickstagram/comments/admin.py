from django.contrib import admin
from nickstagram.comments.models import Comments


class CommentsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Comments, CommentsAdmin)

