from django.contrib import admin
from nickstagram.web.models import Post, Comments, Likes


class PostAdmin(admin.ModelAdmin):
    pass


class CommentsAdmin(admin.ModelAdmin):
    pass


class LikesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Likes, LikesAdmin)
