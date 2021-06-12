import factory
from django.test import TestCase
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

from users.models import Follows
from users.service import get_user_by_id, get_subscribed_status, follow_user, unfollow_user

User = get_user_model()


class UsersManagersTests(TestCase):

    def test_test_create_user(self):
        user = User.objects.create_user(email='kazakovlim@inbox.ru', password='qwerty0810')
        self.assertEqual(user.email, 'kazakovlim@inbox.ru')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='qwerty0810')

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(email='kazazkovlim@gmail.com', password='admin0810')
        self.assertEquals(admin_user.email, 'kazakovlim@gmail.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='kazakovlim@gmail.com', password='admin0810', is_superuser=False)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    password = factory.Faker('password')


class ServiceTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.result = get_user_by_id(self.user.id)

    def test_get_user_by_id_true(self):
        self.assertEquals(self.user, self.result)

    def test_get_user_by_id_false(self):
        new_user = UserFactory()
        self.assertNotEquals(new_user, self.result)


# class FollowsFactory(DjangoModelFactory):
#     class Meta:
#         model = Follows
#
#     user_subscribed = UserFactory()
#     user_signer = UserFactory()


class FollowsTestCase(TestCase):
    def setUp(self):
        self.user_subscribed = UserFactory()
        self.user_signer = UserFactory()

    def test_get_subscribed_status_true(self):
        Follows.objects.create(user_signer=self.user_signer, user_subscribed=self.user_subscribed)
        self.assertTrue(get_subscribed_status(self.user_subscribed, self.user_signer))

    def test_get_subscribed_status_false(self):
        self.assertFalse(get_subscribed_status(self.user_subscribed, self.user_signer))

    def test_follow_user_true(self):
        follow_user(self.user_signer, self.user_subscribed.id)
        self.assertTrue(get_subscribed_status(self.user_subscribed, self.user_signer))

    def test_follow_user_false(self):
        follow_user(self.user_signer, self.user_subscribed.id)
        unfollow_user(self.user_signer, self.user_subscribed.id)
        self.assertFalse(get_subscribed_status(self.user_subscribed, self.user_signer))
