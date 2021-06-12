from django.contrib.auth.models import AbstractUser
from django.db import models
from djchoices import DjangoChoices, ChoiceItem

from users.managers import CustomUserManager


class Role(DjangoChoices):
    admin = ChoiceItem()
    user = ChoiceItem()


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    instagram = models.URLField(verbose_name='инста', null=True, blank=True)
    insta_status = models.BooleanField(verbose_name='статус инсты', null=True, blank=True)
    birthday = models.DateTimeField(verbose_name='День рождения', null=True, blank=True)
    patronymic = models.CharField(max_length=150, verbose_name='Отчество', blank=True)
    avatar_path = models.CharField(max_length=150, verbose_name='Аватар', blank=False, default='twitter/default.jpg')
    file = models.ImageField(upload_to='files_from_users', verbose_name='файл', null=True, blank=True)
    phone_number = models.CharField(max_length=11, verbose_name='Телефон', blank=True)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.user)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email} - {self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Follows(models.Model):
    user_subscribed = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='подписался на',
                                        related_name='subscriptions', null=False, blank=False)
    user_signer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='подписался',
                                    related_name="subscribers", null=False, blank=False)
    data = models.DateTimeField(auto_now_add=True, verbose_name='дата подписки', null=False, blank=False)

    def __str__(self):
        return f'{self.user_signer} подписан на {self.user_subscribed}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'


class PasswordToken(models.Model):
    token = models.CharField(max_length=36, verbose_name='токен смены пароля', null=False, blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='token', null=False, blank=False)
    validity_status = models.BooleanField(verbose_name='статус токена', null=False, blank=False, default=True)
    hash_password = models.CharField(max_length=250, verbose_name='пароль', null=False, blank=False)
    date_of_creation = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name='дата создания')
    date_of_updating = models.DateTimeField(auto_now_add=True, verbose_name='дата обновления', null=False, blank=False)

    def __str__(self):
        return f'Токен - {self.token}. Последнее обновление: {self.date_of_updating}. Статус'

    class Meta:
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'
