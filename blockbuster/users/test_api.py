from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from users.factories import UserModelFactory
from users.factories import FriendsUserRelationshipModelFactory
from users.models import UserRelationship
from users.constants import RELATIONSHIP_STATUS_PENDING
from users.factories import BaseUserRelationshipModelFactory, FollowingUserRelationshipModelFactory


class UserViewTestCase(APITestCase):
    def test__create_user_is_successful(self):
        # GIVEN a request to create a new user with the required fields
        username = 'testuser'
        password = 'blockbuster'
        email = 'blockbuster@test.com'
        data = dict(
            username=username,
            password=password,
            email=email
        )
        url = 'http://127.0.0.1:8000/api/register/'
        # WHEN the request is made
        response = self.client.post(url, data, format='json')
        user = User.objects.get(username=username)
        # THEN the user is in the system
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.email, email)
        # AND they have a profile
        self.assertTrue(user.profile)

    def test__create_user_with_invalid_email_fails(self):
        # GIVEN a request to create a new user but the email is invalid
        username = 'testuser'
        password = 'blockbuster'
        email = 'blockbustersss'
        data = dict(
            username=username,
            password=password,
            email=email
        )
        url = 'http://127.0.0.1:8000/api/register/'
        # WHEN the request is made
        response = self.client.post(url, data, format='json')

        # THEN the error message is displayed
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("email")[0], "Enter a valid email address.")

    def test__create_user_with_missing_required_field_fails(self):
        # GIVEN a request to create a new user but the request doesnt contain some needed info
        password = 'blockbuster'
        email = 'blockbusters@test.com'
        data = dict(
            password=password,
            email=email
        )
        url = 'http://127.0.0.1:8000/api/register/'
        # WHEN the request is made
        response = self.client.post(url, data, format='json')

        # THEN the error message is displayed
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("username")[0], "This field is required.")


class UserRelationshipViewTestCase(APITestCase):
    def test__users_friends_are_returned(self):
        # GIVEN a user has a friend
        authed_user = UserModelFactory()
        friend = UserModelFactory()
        friendship = FriendsUserRelationshipModelFactory(initiator=authed_user.profile, receiver=friend.profile)
        self.client.force_authenticate(user=authed_user)

        # WHEN they request the api to view their friends list
        url = 'http://127.0.0.1:8000/api/author/%s/friends/' % authed_user.profile.uuid

        response = self.client.get(url)

        # THEN the response will contain their friends
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get('uuid'), str(friend.profile.uuid))
        self.assertEqual(len(response.data), len(authed_user.profile.friends))


class UserRelationshipFriendRequestViewSet(APITestCase):
    def test_friend_request_creates_friend_request(self):
        # GIVEN an authenticated user makes a friend request for another user
        authed_user = UserModelFactory()
        friend = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        url = 'http://127.0.0.1:8000/api/friendrequest/'
        data = dict(
            initiator=dict(
                uuid=authed_user.profile.uuid,
                username=authed_user.profile.username
            ),
            receiver=dict(
                uuid=friend.profile.uuid,
                username=friend.profile.username
            ),
        )

        # WHEN the request is made
        response = self.client.post(url, data, format='json')

        # THEN the relationship is created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        friendship = UserRelationship.objects.all()[0]
        # AND friendship status should be PENDING by default
        self.assertEqual(friendship.status, RELATIONSHIP_STATUS_PENDING)
        self.assertEqual(friendship.initiator, authed_user.profile)
        self.assertEqual(friendship.receiver, friend.profile)

    def test_get_users_friend_requests_list(self):
        # GIVEN an authenticated user has friend requests
        authed_user = UserModelFactory()
        follower1 = UserModelFactory()
        follower2 = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        friendship1 = BaseUserRelationshipModelFactory(initiator=follower1.profile, receiver=authed_user.profile)
        friendship2 = BaseUserRelationshipModelFactory(initiator=follower2.profile, receiver=authed_user.profile)
        self.assertEquals(friendship1.status, RELATIONSHIP_STATUS_PENDING)
        self.assertEquals(friendship2.status, RELATIONSHIP_STATUS_PENDING)
        url = 'http://127.0.0.1:8000/api/friendrequest/'

        # WHEN the request is made
        response = self.client.get(url)

        # THEN a successful response is made
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserRelationshipCheckViewTestCase(APITestCase):
    def test_check_two_uuids_are_friends_success(self):
        # GIVEN two users are friends
        friend1 = UserModelFactory()
        friend2 = UserModelFactory()

        friendship = FriendsUserRelationshipModelFactory(initiator=friend1.profile, receiver=friend2.profile)
        url = 'http://127.0.0.1:8000/api/author/%s/friends/%s/' % (friend1.profile.uuid, friend2.profile.uuid)

        # WHEN the request is made
        response = self.client.get(url)

        # THEN a successful response is made and the boolean is true
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('friends'))

    def test_check_two_uuids_are_friends_fails(self):
        # GIVEN two users are not friends
        friend1 = UserModelFactory()
        friend2 = UserModelFactory()

        friendship = FollowingUserRelationshipModelFactory(initiator=friend1.profile, receiver=friend2.profile)
        url = 'http://127.0.0.1:8000/api/author/%s/friends/%s/' % (friend1.profile.uuid, friend2.profile.uuid)

        # WHEN the request is made
        response = self.client.get(url)

        # THEN a successful response is made and the boolean is true
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data.get('friends'))
