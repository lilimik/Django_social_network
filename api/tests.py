# import requests
# from django.test import TestCase
#
# from api.views import PostsViewSet
# from posts.tests import PostFactory
# from posts.service import get_post_with_owner
# from users.tests import UserFactory
#
#
# class PostsTestCase(TestCase):
#     def setUp(self):
#         user = UserFactory()
#         self.post1 = PostFactory(owner=user)
#         self.post2 = PostFactory(owner=user)
#         self.post3 = PostFactory(owner=user)
#         self.list = (self.post1, self.post2, self.post3)
#
#     def test_list_true(self):
#         check_list = requests.get('')
#         self.assertEquals(self.list, check_list)
#
#     def test_get_post_with_owner_false(self):
#         new_post = PostFactory()
#         founded_post = get_post_with_owner(new_post.id)
#         self.assertEquals(new_post, founded_post)