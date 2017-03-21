from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from users.factories import UserModelFactory
from users.factories import FriendsUserRelationshipModelFactory
from users.models import UserRelationship
from users.constants import RELATIONSHIP_STATUS_PENDING, RELATIONSHIP_STATUS_FRIENDS, RELATIONSHIP_STATUS_FOLLOWING
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


class UserRelationshipFriendRequestViewSetTestCase(APITestCase):
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        friendship = UserRelationship.objects.all()[0]
        # AND friendship status should be PENDING by default
        self.assertEqual(friendship.status, RELATIONSHIP_STATUS_PENDING)
        self.assertEqual(friendship.initiator, authed_user.profile)
        self.assertEqual(friendship.receiver, friend.profile)

    def test_accept_friend_request_accepts_friend_request(self):
        # GIVEN a user has pending friend requests
        authed_user = UserModelFactory()
        follower1 = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        friendship1 = BaseUserRelationshipModelFactory(initiator=follower1.profile, receiver=authed_user.profile)
        self.assertEquals(friendship1.status, RELATIONSHIP_STATUS_PENDING)

        url = 'http://127.0.0.1:8000/api/friendrequest/'
        data = dict(
            initiator=dict(
                uuid=follower1.profile.uuid,
                username=follower1.profile.username
            ),
            receiver=dict(
                uuid=authed_user.profile.uuid,
                username=authed_user.profile.username
            ),
            status=RELATIONSHIP_STATUS_FRIENDS
        )

        # WHEN the request is made
        response = self.client.post(url, data, format='json')

        # THEN the relationship is created
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        friendship = UserRelationship.objects.get(id=friendship1.id)
        # AND friendship status should be FRIENDS
        self.assertEqual(friendship.status, RELATIONSHIP_STATUS_FRIENDS)
        self.assertEqual(friendship.initiator, follower1.profile)
        self.assertEqual(friendship.receiver, authed_user.profile)

    def test_decline_friend_request_creates_following_friendship(self):
        # GIVEN a user has pending friend requests
        authed_user = UserModelFactory()
        follower1 = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        friendship1 = BaseUserRelationshipModelFactory(initiator=follower1.profile, receiver=authed_user.profile)
        self.assertEquals(friendship1.status, RELATIONSHIP_STATUS_PENDING)

        url = 'http://127.0.0.1:8000/api/friendrequest/'
        data = dict(
            initiator=dict(
                uuid=follower1.profile.uuid,
                username=follower1.profile.username
            ),
            receiver=dict(
                uuid=authed_user.profile.uuid,
                username=authed_user.profile.username
            ),
            status=RELATIONSHIP_STATUS_FOLLOWING
        )

        # WHEN the request is made
        response = self.client.post(url, data, format='json')

        # THEN the relationship is created
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        friendship = UserRelationship.objects.get(id=friendship1.id)
        # AND friendship status should be FRIENDS
        self.assertEqual(friendship.status, RELATIONSHIP_STATUS_FOLLOWING)
        self.assertEqual(friendship.initiator, follower1.profile)
        self.assertEqual(friendship.receiver, authed_user.profile)

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

    def test_delete_relationship_when_friends__logged_in_user_is_initiator_success(self):
        # GIVEN an authenticated user has a friend and the logged in user initiated that friendship
        authed_user = UserModelFactory()
        friend = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        friendship = FriendsUserRelationshipModelFactory(initiator=authed_user.profile, receiver=friend.profile)
        self.assertEquals(friendship.status, RELATIONSHIP_STATUS_FRIENDS)
        self.assertEquals(friendship.initiator, authed_user.profile)
        self.assertEquals(friendship.receiver, friend.profile)
        # WHEN a delete request is made to the entity url
        url = 'http://127.0.0.1:8000/api/friendrequest/%s/' % friendship.id

        # WHEN the request is made
        response = self.client.delete(url, format='json')

        friendship = UserRelationship.objects.get(id=friendship.id)
        # THEN a successful response is made
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The roles should be switched
        self.assertEquals(friendship.initiator, friend.profile)
        self.assertEquals(friendship.receiver, authed_user.profile)
        self.assertEquals(friendship.status, RELATIONSHIP_STATUS_FOLLOWING)

    def test_delete_relationship_when_friends_logged_in_user_is_receiver_success(self):
        # GIVEN an authenticated user has a friend that the friend initiated
        authed_user = UserModelFactory()
        friend = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        friendship = FriendsUserRelationshipModelFactory(receiver=authed_user.profile, initiator=friend.profile)
        self.assertEquals(friendship.status, RELATIONSHIP_STATUS_FRIENDS)
        self.assertEquals(friendship.receiver, authed_user.profile)
        self.assertEquals(friendship.initiator, friend.profile)
        # WHEN a delete request is made to the entity url
        url = 'http://127.0.0.1:8000/api/friendrequest/%s/' % friendship.id

        # WHEN the request is made
        response = self.client.delete(url, format='json')

        friendship = UserRelationship.objects.get(id=friendship.id)
        # THEN a successful response is made
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The roles should be switched
        self.assertEquals(friendship.initiator, friend.profile)
        self.assertEquals(friendship.receiver, authed_user.profile)
        self.assertEquals(friendship.status, RELATIONSHIP_STATUS_FOLLOWING)

    def test_delete_relationship_when_other_is_following_removes_row_entirely(self):
        # GIVEN an authenticated user has a person following them
        authed_user = UserModelFactory()
        friend = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        friendship = FollowingUserRelationshipModelFactory(initiator=authed_user.profile, receiver=friend.profile)
        self.assertEquals(friendship.status, RELATIONSHIP_STATUS_FOLLOWING)
        self.assertEquals(friendship.initiator, authed_user.profile)
        self.assertEquals(friendship.receiver, friend.profile)
        url = 'http://127.0.0.1:8000/api/friendrequest/%s/' % friendship.id

        # WHEN the request is made
        response = self.client.delete(url, format='json')
        # THEN there should be a successful response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # THEN an error should be raised
        with self.assertRaises(UserRelationship.DoesNotExist):
            friendship2 = UserRelationship.objects.get(id=friendship.id)

    def test_delete_relationship_when_pending_removes_row_entirely(self):
        # GIVEN an authenticated user has a pending relationship that the logged in user initiated
        authed_user = UserModelFactory()
        friend = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        friendship = BaseUserRelationshipModelFactory(initiator=authed_user.profile, receiver=friend.profile)
        self.assertEquals(friendship.status, RELATIONSHIP_STATUS_PENDING)
        self.assertEquals(friendship.initiator, authed_user.profile)
        self.assertEquals(friendship.receiver, friend.profile)
        url = 'http://127.0.0.1:8000/api/friendrequest/%s/' % friendship.id

        # WHEN the request is made
        response = self.client.delete(url, format='json')
        # THEN there should be a successful response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # THEN an error should be raised
        with self.assertRaises(UserRelationship.DoesNotExist):
            friendship2 = UserRelationship.objects.get(id=friendship.id)

    def test_delete_relationship_when_invalid_pk_given(self):
        # GIVEN an authenticated user tries to delete an invalid friendship object
        authed_user = UserModelFactory()
        # friend = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        # friendship = BaseUserRelationshipModelFactory(initiator=authed_user.profile, receiver=friend.profile)
        # self.assertEquals(friendship.status, RELATIONSHIP_STATUS_PENDING)
        # self.assertEquals(friendship.initiator, authed_user.profile)
        # self.assertEquals(friendship.receiver, friend.profile)
        url = 'http://127.0.0.1:8000/api/friendrequest/9999/'

        # WHEN the request is made
        response = self.client.delete(url, format='json')

        # THEN there should be a successful response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_relationship_when_another_relationships_pk_given(self):
        # GIVEN an authenticated user tries to delete an invalid friendship object
        authed_user = UserModelFactory()
        random = UserModelFactory()
        friend = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        friendship = BaseUserRelationshipModelFactory(initiator=random.profile, receiver=friend.profile)
        self.assertEquals(friendship.status, RELATIONSHIP_STATUS_PENDING)
        self.assertEquals(friendship.initiator, random.profile)
        self.assertEquals(friendship.receiver, friend.profile)
        url = 'http://127.0.0.1:8000/api/friendrequest/%s/' % friendship.id

        # WHEN the request is made
        response = self.client.delete(url, format='json')

        # THEN there should be a successful response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, 'You do not have access to this friendship.')


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


class AuthenticatedUserRelationshipViewTestCase(APITestCase):
    def test_check_relationship_exists__as_receiver_success(self):
        # GIVEN an authenticated user is friends with another person
        authed_user = UserModelFactory()
        follower1 = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        friendship1 = BaseUserRelationshipModelFactory(initiator=follower1.profile, receiver=authed_user.profile)
        self.assertEquals(friendship1.status, RELATIONSHIP_STATUS_PENDING)
        url = 'http://127.0.0.1:8000/api/author/me/relationship/%s/' % follower1.profile.uuid

        # WHEN the request is made
        response = self.client.get(url)

        # THEN a successful response is made
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fields = ['status', 'initiator', 'receiver']
        for field in fields:
            self.assertTrue(field in response.data)

    def test_check_relationship_exists__as_initiator_success(self):
        # GIVEN an authenticated user is friends with another person
        authed_user = UserModelFactory()
        follower1 = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        friendship1 = BaseUserRelationshipModelFactory(initiator=authed_user.profile, receiver=follower1.profile)
        self.assertEquals(friendship1.status, RELATIONSHIP_STATUS_PENDING)
        url = 'http://127.0.0.1:8000/api/author/me/relationship/%s/' % follower1.profile.uuid

        # WHEN the request is made
        response = self.client.get(url)

        # THEN a successful response is made
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fields = ['status', 'initiator', 'receiver']
        for field in fields:
            self.assertTrue(field in response.data)

    def test_relationship_when_no_relationship_exists(self):
        # GIVEN an authenticated user has no relationship with another person
        authed_user = UserModelFactory()
        follower1 = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        url = 'http://127.0.0.1:8000/api/author/me/relationship/%s/' % follower1.profile.uuid

        # WHEN the request is made
        response = self.client.get(url)

        # THEN a successful response is made
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "No Relationship Found.")

    def test_relationship_when_own_uuid_given(self):
        # GIVEN an authenticated user requests a relationship with themself
        authed_user = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        url = 'http://127.0.0.1:8000/api/author/me/relationship/%s/' % authed_user.profile.uuid

        # WHEN the request is made
        response = self.client.get(url)

        # THEN a successful response is made
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "The profile with the given UUID is your own.")
