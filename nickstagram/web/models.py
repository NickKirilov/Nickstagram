from django.contrib.auth.models import User, AbstractUser
from django.db import models

from nickstagram.accounts.models import NickstagramUser
from nickstagram.accounts.validators import file_max_size_validator


class Post(models.Model):
    MAX_LEN_POST_TITLE = 60

    title = models.CharField(
        max_length=MAX_LEN_POST_TITLE,
    )
    description = models.TextField()

    image = models.ImageField(
        validators=(
            file_max_size_validator,
        ),
        upload_to='images/uploaded_post_images',
    )

    date_of_creation = models.DateTimeField(
        auto_now_add=True,
    )

    public = models.BooleanField(
        default=False,
    )

    profile = models.ForeignKey(NickstagramUser, on_delete=models.CASCADE)

