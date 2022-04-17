from celery import shared_task
from django.core.mail import send_mail
from nickstagram.accounts.models import Profile


@shared_task
def send_successful_changing_password_email(profile_pk):
    profile = Profile.objects.get(pk=profile_pk)

    send_mail(
        'Changed password',
        f'Successfully changed your password!',
        '',
        [profile.email],
        fail_silently=False
    )
