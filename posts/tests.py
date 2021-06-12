from django.test import TestCase
import factory
from factory.django import DjangoModelFactory

from posts.models import Post
from posts.service import get_post_with_owner
from users.tests import UserFactory


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    text = factory.Faker('text')


class PostsTestCase(TestCase):
    def setUp(self):
        user = UserFactory()
        self.post = PostFactory(owner=user)

    def test_get_post_with_owner_true(self):
        founded_post = get_post_with_owner(self.post.id)
        self.assertEquals(self.post, founded_post)

    def test_get_post_with_owner_false(self):
        new_post = PostFactory()
        founded_post = get_post_with_owner(new_post.id)
        self.assertEquals(new_post, founded_post)
