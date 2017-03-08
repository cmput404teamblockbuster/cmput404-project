from rest_framework.test import APIRequestFactory, force_authenticate
from django.test import TestCase

from posts.factories import BasePostModelFactory


class PostViewSetTestCase(TestCase):
    def test__post_comment__sucess(self):
        post = BasePostModelFactory()
        factory = APIRequestFactory()
        print post.author.id
        data = dict(

        )
        request = factory.post('/api/posts/', post, format="json")
        force_authenticate(request, user=post.author)


# from http://www.django-rest-framework.org/api-guide/testing/#apirequestfactory