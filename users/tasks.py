from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from twitter import settings
from twitter.celery import app


User = get_user_model()

@app.task(queue='default')
def change_password_task(email, token_url):
    send_mail(
        'Письмо с localhost\'a',
        f'Для подтверждения смены пароля, перейдите по ссылке: {token_url}',
        settings.EMAIL_FROM_EMAIL,
        [email],
    )


@app.task(queue="default")
def check_insta_status():
    print('я и это делаю да')
