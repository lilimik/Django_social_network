# Generated by Django 3.1.7 on 2021-03-29 15:08

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_link', models.CharField(max_length=16, unique=True, verbose_name='короткая ссылка')),
                ('original_name', models.CharField(max_length=100, verbose_name='название')),
                ('size', models.BigIntegerField(verbose_name='размер')),
                ('media_type',
                 models.CharField(choices=[('VIDEO', 'VIDEO'), ('PHOTO', 'PHOTO'), ('MUSIC', 'MUSIC')], max_length=5,
                                  verbose_name='тип')),
            ],
        ),
    ]
