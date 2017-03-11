from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase, APIClient
from users.factories import ProfileModelFactory, UserModelFactory
from rest_framework import status
from posts.models import Post
from posts.constants import PRIVACY_PUBLIC


class PostViewSetTestCase(APITestCase):
    client = APIClient()
    # from example http://www.django-rest-framework.org/api-guide/testing/#example

    def test__create_post_sucess(self):
        # author = ProfileModelFactory()
        # GIVEN an authenticated user chooses to make a post
        author = UserModelFactory()
        self.client.force_authenticate(user=author) # http://www.django-rest-framework.org/api-guide/testing/#force_authenticateusernone-tokennone
        data = dict(
            author=dict(
                uuid=str(author.profile.uuid),
                github='http://www.test.github.com',
                username='bradley',
                privacy=PRIVACY_PUBLIC
            ),
            content='TEST CONTENT'
        )
        url = 'http://127.0.0.1:8000/api/posts/'

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)