from django.contrib.auth.models import User, AbstractUser
from django.db import models
from cloudinary import models as cloudinary_models
from nickstagram.accounts.models import NickstagramUser, Profile


class Post(models.Model):
    MAX_LEN_POST_TITLE = 60

    title = models.CharField(
        max_length=MAX_LEN_POST_TITLE,
    )
    description = models.TextField()

    image = cloudinary_models.CloudinaryField('image')

    date_of_creation = models.DateTimeField(
        auto_now_add=True,
    )

    public = models.BooleanField(
        default=False,
    )

    profile = models.ForeignKey(NickstagramUser, on_delete=models.CASCADE)


class Comments(models.Model):
    text = models.TextField()

    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Likes(models.Model):
    like = models.BooleanField()

    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

