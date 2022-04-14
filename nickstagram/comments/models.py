from django.db import models

# Create your models here.
from nickstagram.accounts.models import Profile
from nickstagram.posts.models import Post


class Comments(models.Model):
    text = models.TextField()

    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title
