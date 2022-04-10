from cloudinary import models as cloudinary_models
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.contrib.auth import models as auth_models
from nickstagram.accounts.managers import NickstagramUserManager
from nickstagram.common_utils.validators import validate_date_of_birth, validate_last_name, \
    validate_first_name


class NickstagramUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_MAX_LEN = 25

    username = models.CharField(
        max_length=USERNAME_MAX_LEN,
        unique=True,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'username'

    objects = NickstagramUserManager()


class Profile(models.Model):
    USERNAME_MAX_LEN = 20
    USERNAME_MIN_LEN = 4
    USERNAME_PATTERN = r'[a-z\_0-9]+'
    USERNAME_ERROR_PATTERN_MESSAGE = 'The username must contains only lowercase letters, underscores and numbers!'
    USERNAME_ERROR_MIN_LEN_MESSAGE = f'The username must be at least {USERNAME_MIN_LEN} characters long.'

    PASSWORD_MAX_LEN = 30
    PASSWORD_MIN_LEN = 8

    FIRST_NAME_MAX_LEN = 30
    FIRST_NAME_MIN_LEN = 2
    FIRST_NAME_ERROR_MIN_LEN_MESSAGE = f'The first name must be at least {FIRST_NAME_MIN_LEN} characters long.'

    LAST_NAME_MAX_LEN = 30
    LAST_NAME_MIN_LEN = 2
    LAST_NAME_ERROR_MIN_LEN_MESSAGE = f'The first name must be at least {LAST_NAME_MIN_LEN} characters long.'

    EMAIL_MAX_LEN = 60

    MALE = 'Male'
    FEMALE = 'Female'
    DON_NOT_SHOW = 'Do not show'

    GENDERS = [(x, x) for x in (MALE, FEMALE, DON_NOT_SHOW)]

    username = models.CharField(
        max_length=USERNAME_MAX_LEN,
        validators=(
            RegexValidator(USERNAME_PATTERN, USERNAME_ERROR_PATTERN_MESSAGE),
            MinLengthValidator(USERNAME_MIN_LEN, USERNAME_ERROR_MIN_LEN_MESSAGE)
        ),
        unique=True,
    )

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LEN,
        validators=(
            validate_first_name,
            MinLengthValidator(FIRST_NAME_MIN_LEN, FIRST_NAME_ERROR_MIN_LEN_MESSAGE),
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LEN,
        validators=(
            validate_last_name,
            MinLengthValidator(LAST_NAME_MIN_LEN, LAST_NAME_ERROR_MIN_LEN_MESSAGE),
        )
    )

    email = models.EmailField(
        max_length=EMAIL_MAX_LEN,
    )

    date_of_birth = models.DateField(
        validators=(
            validate_date_of_birth,
        ),
    )

    gender = models.CharField(
        null=True,
        blank=True,
        max_length=max(len(x) for x, _ in GENDERS),
        choices=GENDERS,
        default=DON_NOT_SHOW,
    )

    image = cloudinary_models.CloudinaryField(
        'image',
        blank=True,
        null=True,
        default='image/upload/v1649599331/default_gzreya.png',
    )

    user = models.OneToOneField(
        NickstagramUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.username
