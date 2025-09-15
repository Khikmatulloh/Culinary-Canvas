from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_confirmation_email(email, token):
    confirm_url = f"http://127.0.0.1:8000/users/confirm/{token}/"
    subject = "Email confirmation"
    message = f"Click the link to confirm your account: {confirm_url}"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
