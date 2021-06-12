from urllib.error import HTTPError

from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import requests

from posts.models import Post

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    instagram_status = serializers.SerializerMethodField()
    phone = serializers.CharField(source='phone_number')

    @swagger_serializer_method(
        serializer_or_field=serializers.CharField(help_text='Статус страницы инсты')
    )
    def get_instagram_status(self, instance):
        status = True
        try:
            requests.get(instance.instagram).raise_for_status()
        except HTTPError:
            status = False
        return status

    def validate_instagram(self, value):
        if (len(value) < 27) and ('https://www.instagram.com/' not in value):
            raise ValidationError('это точно не URL инсты')
        return value

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'instagram', 'instagram_status', 'phone', 'date_joined')
        read_only_fields = ('phone_number', 'instagram',)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'date_of_creation', 'text')


class PostFullSerializer(PostSerializer):
    owner = UserSerializer()

    class Meta:
        model = Post
        fields = (*PostSerializer.Meta.fields, 'owner')
