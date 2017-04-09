import requests
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase, APIClient
from users.factories import ProfileModelFactory, UserModelFactory, FriendsUserRelationshipModelFactory
from rest_framework import status
from posts.models import Post
from posts.constants import PRIVACY_PUBLIC, PRIVACY_PRIVATE, PRIVATE_TO_ALL_FRIENDS, PRIVACY_UNLISTED, PRIVACY_SERVER_ONLY
from posts.factories import BasePostModelFactory

from nodes.factories import NodeModelFactory


class ProfilePostDetailViewTestCase(APITestCase):
    client = APIClient

    def test__author_posts_from_requesting_node_gives_all_posts_but_server_only_success(self):
        # GIVEN a bunch of posts by a given author
        author = UserModelFactory()
        post = BasePostModelFactory(privacy=PRIVACY_PRIVATE, author=author.profile)
        post_public = BasePostModelFactory(privacy=PRIVACY_PUBLIC, author=author.profile)
        post_server = BasePostModelFactory(privacy=PRIVACY_SERVER_ONLY, author=author.profile)

        # WHEN a foreign Node requests this users page
        user = UserModelFactory(username='test_node', password='test_node')
        node = NodeModelFactory(user=user)
        url = 'http://127.0.0.1:9000/api/author/9b6d50c4-011a-4753-954c-30ac73b62d81/posts/' # taylor's profile
        response = requests.get(url, auth=('test_node', 'test'))
        print response.text

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
        post = BasePostModelFactory(privacy=PRIVACY_PRIVATE, author=user.profile)
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
            visibility = PRIVACY_PRIVATE
        )
        # WHEN we try to update the post with a new status
        url = '/api/posts/%s/' % post.uuid
        response = self.client.put(url, format='json', data=data)

        # THEN the post should be updated
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(Post.objects.all()[0].privacy, PRIVACY_PRIVATE)

    # def test__update_post_to_private_to_success(self):
    #     # GIVEN a post
    #     author = UserModelFactory()
    #     author2 = UserModelFactory()
    #     self.client.force_authenticate(user=author)
    #     post = BasePostModelFactory(author=author.profile, privacy=PRIVACY_PUBLIC)
    #     self.assertEquals(Post.objects.all().count(), 1)
    #     self.assertEquals(Post.objects.all()[0].privacy, PRIVACY_PUBLIC)
    #
    #     data = dict(
    #         visibility=PRIVATE_TO_ONE_FRIEND,
    #         visibleTo=dict(
    #             id=str(author2.profile.api_id),
    #             github='http://www.test.github.com',
    #             host='http://otherserver.com',
    #             displayName=author2.profile.username,
    #         ),
    #     )
    #     # WHEN we try to update the post with a new status
    #     url = '/api/posts/%s/' % post.uuid
    #     response = self.client.put(url, format='json', data=data)
    #
    #     # THEN the post should be updated
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(Post.objects.all().count(), 1)
    #     self.assertEqual(Post.objects.all()[0].privacy, PRIVATE_TO_ONE_FRIEND)
    #     self.assertEqual(Post.objects.all()[0].private_to, author2.profile)

"""
{"query": "posts", "count": 2, "current": 1, "next": null, "previous": null, "size": 1000, "posts": [
    {"title": "newer post", "source": null, "origin": null, "description": "", "contentType": "text/plain",
     "content": "newer post",
     "author": {"id": "http://127.0.0.1:8000/api/author/9b6d50c4-011a-4753-954c-30ac73b62d81", "displayName": "taylor",
                "github": "http://www.github.com/tdarnett/", "host": "http://127.0.0.1:8000/",
                "url": "http://127.0.0.1:8000/profile/9b6d50c4-011a-4753-954c-30ac73b62d81",
                "bio": "This is my bio :)"}, "comments": [], "published": "2017-04-04 17:39:12.628290+00:00",
     "id": "554e8c73-c8b4-4b2f-abc5-3cc0e98f0f22", "visibility": "privacy_public", "visibleTo": []},
    {"title": "This is a post title", "source": null, "origin": null, "description": "this is a description",
     "contentType": "text/plain", "content": "This is the post content!",
     "author": {"id": "http://127.0.0.1:8000/api/author/9b6d50c4-011a-4753-954c-30ac73b62d81", "displayName": "taylor",
                "github": "http://www.github.com/tdarnett/", "host": "http://127.0.0.1:8000/",
                "url": "http://127.0.0.1:8000/profile/9b6d50c4-011a-4753-954c-30ac73b62d81",
                "bio": "This is my bio :)"}, "comments": [], "published": "2017-04-04 15:12:16.470331+00:00",
     "id": "ef73e05b-fa85-458e-b2cb-ad3bbc848e2a", "visibility": "privacy_public", "visibleTo": []}]}
"""