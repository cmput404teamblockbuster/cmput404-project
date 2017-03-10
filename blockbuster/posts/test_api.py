from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase

from posts.factories import BasePostModelFactory

from users.factories import UserModelFactory
from rest_framework import status

from posts.models import Post


class PostViewSetTestCase(APITestCase):
    # from example http://www.django-rest-framework.org/api-guide/testing/#example
    def test__post_comment__sucess(self):
        # post = BasePostModelFactory()
        author = UserModelFactory()
        # from pprint import pprint
        # pprint(vars(post.author))
        # print post.author.profile.user.is_staff
        # print post.author.id
        data = dict(
            author=author.id,
            content='TEST CONTENT'
        )
        url = 'http://127.0.0.1:8000/api/posts/'
        response = self.client.post(url, data, format='json')
        print response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

        # print Post.objects.all()
        # print request


# from http://www.django-rest-framework.org/api-guide/testing/#apirequestfactory