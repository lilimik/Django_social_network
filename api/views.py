from django.db.models import Subquery
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from api.serializer import PostSerializer, PostFullSerializer
from posts.models import Post
from users.models import Follows


@api_view(['GET'])
def main_api_view(request):
    """Метод проверки api"""
    return Response({
        'status': 'ok'
    })


class PostChangeOnlyForOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return obj.owner_id == request.user.id


# @method_decorator(swagger_auto_schema(request_body=PostFullSerializer), name='retrieve')
class PostsViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = [PostChangeOnlyForOwnerPermission]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostFullSerializer
        return PostSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Post.objects.annotate_likes_comments().select_related('owner')

        if user.is_authenticated:
            follows = Follows.objects.filter(user_signer_id=self.request.user.id)
            qs = Post.objects.filter(
                id__in=Subquery(follows.values('user_subscribed__posts'))
            )
        return qs

    @swagger_auto_schema(
        operation_summary='Posts list',
        responses={
            200: 'Posts list success'
        }
    )
    def list(self, request, *args, **kwargs):
        """Выводит список постов"""
        return super(PostsViewSet, self).list(request, *args, **kwargs)

    @swagger_auto_schema(
        method='post',
        request_body=no_body,
        operation_summary='Post check',
        operation_description='Проверка поста',
        responses={
            200: 'Post checked'
        }
    )
    @action(['POST'], detail=True)
    def check(self, request, *args, **kwargs):
        obj = self.get_object()
        return Response({
            'status': 'ok',
            'post id': obj.id,
        })
