from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_activation_code(email, activation_code):

    message = f"""Your activation code for your twitter account:
    http://127.0.0.1:8000/api/v1/account/activation/{activation_code}"""
    send_mail(
        'Аccount activation',
        message,
        'test@pytter.com',
        [email, ],
        fail_silently=False
    )