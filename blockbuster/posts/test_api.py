from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase, APIClient
from users.factories import ProfileModelFactory, UserModelFactory, FriendsUserRelationshipModelFactory
from rest_framework import status
from posts.models import Post
from posts.constants import PRIVACY_PUBLIC, PRIVATE_TO_ME, PRIVATE_TO_ALL_FRIENDS, PRIVACY_UNLISTED
from posts.factories import BasePostModelFactory


class PostViewSetTestCase(APITestCase):
    client = APIClient()

    # from example http://www.django-rest-framework.org/api-guide/testing/#example

    def test__create_post_success(self):
        # author = ProfileModelFactory()
        # GIVEN an authenticated user chooses to make a post
        author = UserModelFactory()
        self.client.force_authenticate(
            user=author)  # http://www.django-rest-framework.org/api-guide/testing/#force_authenticateusernone-tokennone
        data = dict(
            author=dict(
                id=str(author.profile.api_id),
                github='http://www.test.github.com',
                host='http://otherserver.com',
                displayName=author.profile.username,
            ),
            visibility=PRIVACY_PUBLIC,
            content='TEST CONTENT',
            contentType='text/plain',
        )
        url = '/api/posts/'

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    def test_retrieve_private_post_anon_user_fails(self):
        # GIVEN an unauthed user
        user = UserModelFactory()
        user2 = UserModelFactory()
        post = BasePostModelFactory(privacy=PRIVATE_TO_ME, author=user.profile)
        self.client.force_authenticate(user=user2)


        # WHEN they try to view details of the post
        url = '/api/posts/%s/' % post.uuid
        response = self.client.get(url)

        # THEN an error should be raised
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, 'You do not have permission to see this post.')

    def test_retrieve_private_post_authed_user_fails(self):
        # GIVEN an authed user that is not friends with a user that makes a friend post
        user = UserModelFactory()
        post = BasePostModelFactory(privacy=PRIVATE_TO_ALL_FRIENDS, author=user.profile)
        self.client.force_authenticate(user=user)

        # WHEN they try to view details of the post
        url = '/api/posts/%s/' % post.uuid
        response = self.client.get(url)

        # THEN an error should be raised
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, 'You do not have permission to see this post.')

    def test_retrieve__post_authed_user_friends_success(self):
        # GIVEN an authed user that is friends with a user that makes a friend post
        user = UserModelFactory()
        authed_user = UserModelFactory()
        post = BasePostModelFactory(privacy=PRIVATE_TO_ALL_FRIENDS, author=user.profile)
        friendship = FriendsUserRelationshipModelFactory(initiator=user.profile, receiver=authed_user.profile)
        self.client.force_authenticate(user=authed_user)

        # WHEN they try to view details of the post
        url = '/api/posts/%s/' % post.uuid
        response = self.client.get(url)

        # THEN the post should be retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), str(post.uuid))

    def test_retrieve_unlisted_post_anon_user_success(self):
        # GIVEN an unauthed user requests a post that an author made to be unlisted
        user = UserModelFactory()
        post = BasePostModelFactory(privacy=PRIVACY_UNLISTED, author=user.profile)
        self.client.force_authenticate(user=user)

        # WHEN they try to view details of the post
        url = '/api/posts/%s/' % post.uuid
        response = self.client.get(url)

        # THEN the post should be retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), str(post.uuid))

    def test_unlisted_post_does_not_show_up_in_posts_endpoint(self):
        # GIVEN an unlsited post
        user = UserModelFactory()
        unlisted_post = BasePostModelFactory(privacy=PRIVACY_UNLISTED, author=user.profile)
        public_post = BasePostModelFactory(author=user.profile)
        self.client.force_authenticate(user=user)


        # WHEN they try to view a list of posts
        url = '/api/posts/'
        response = self.client.get(url)

        # THEN the unlisted post should not be returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('id'), str(public_post.uuid))

    def test__delete_post_success(self):
        # GIVEN a post is in the db
        author = UserModelFactory()
        self.client.force_authenticate(user=author)
        post = BasePostModelFactory(author=author.profile)
        self.assertEquals(Post.objects.all().count(), 1)

        # WHEN we try to delete the post
        url = '/api/posts/%s/' % post.uuid
        response = self.client.delete(url)

        # THEN the post should be deleted
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.all().count(), 0)

    def test__update_post_success(self):
        # GIVEN a post
        author = UserModelFactory()
        self.client.force_authenticate(user=author)
        post = BasePostModelFactory(author=author.profile, privacy=PRIVACY_PUBLIC)
        self.assertEquals(Post.objects.all().count(), 1)
        self.assertEquals(Post.objects.all()[0].privacy, PRIVACY_PUBLIC)

        data = dict(
            visibility = PRIVATE_TO_ME
        )
        # WHEN we try to update the post with a new status
        url = '/api/posts/%s/' % post.uuid
        response = self.client.put(url, format='json', data=data)

        # THEN the post should be deleted
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(Post.objects.all()[0].privacy, PRIVATE_TO_ME)
