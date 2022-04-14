from django.db import models
from nickstagram.accounts.models import NickstagramUser, Profile
from nickstagram.posts.models import Post


class Comments(models.Model):
    text = models.TextField()

    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title


class Likes(models.Model):
    like = models.BooleanField()

    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title

