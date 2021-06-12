from django.db import models


class Media(models.Model):
    VIDEO = 'VIDEO'
    PHOTO = 'PHOTO'
    MUSIC = 'MUSIC'
    CHOICES = [
        (VIDEO, VIDEO),
        (PHOTO, PHOTO),
        (MUSIC, MUSIC),
    ]
    short_link = models.CharField(max_length=16, verbose_name='короткая ссылка', null=False, blank=False, unique=True)
    original_name = models.CharField(max_length=100, verbose_name='название', null=False, blank=False)
    size = models.BigIntegerField(verbose_name='размер', null=False, blank=False)
    media_type = models.CharField(max_length=5, verbose_name='тип', null=False, blank=False, choices=CHOICES)

