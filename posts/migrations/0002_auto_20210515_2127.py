# Generated by Django 3.1.10 on 2021-05-15 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_of_creation',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='like',
            name='date_of_creation',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='post',
            name='date_of_creation',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата создания'),
        ),
    ]