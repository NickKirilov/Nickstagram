from django.db import models
from cloudinary import models as cloudinary_models
from nickstagram.accounts.models import NickstagramUser


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

    def __str__(self):
        return self.title
