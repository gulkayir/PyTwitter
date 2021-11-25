
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_activation_code(email, activation_code):
    activation_url = f'http://localhost:8000/api/v1/account/activate/{activation_code}'
    message = f"""
        Thanks for your registration
        Please, activate your account.
        Activation link: {activation_url}
    """
    send_mail(
        'Activate you account',
        message,
        'test@test.com',
        [email, ],
        fail_silently=False)

@shared_task
def send_activation_mail(email, activation_code):
    activation_url = f'http://localhost:8000/api/v1/account/forgot-password-complete/{activation_code}'
    message = f"""To reset password, follow this url: {activation_url}"""
    send_mail(
        'Resetting password',
        message,
        'test@test.com',
        [email, ],
        fail_silently=False
    )