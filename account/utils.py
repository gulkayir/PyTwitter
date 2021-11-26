
from celery import shared_task
from django.core.mail import send_mail
from twitter_api._celery import app

@app.task
def send_confirmation_email(user):
    code = user.activation_code
    full_link = f'http://localhost:8000/api/v1/account/activate/{code}'
    to_email = user.email
    send_mail(
        'Activate your account with following this url',
        full_link,
        'from@example.com',
        [to_email],
        fail_silently=False,
    )

@app.task
def send_activation_code(user):
    activation_url = f'{user.activation_code}'
    message = f"""Restore password use code: {activation_url}"""
    to_email = user.email
    send_mail(
        'Активация аккаунта',
        message,
        'test@my_project.com',
        [to_email],
        fail_silently=False,
    )
