import requests
import unittest

from django.contrib.sites.models import Site
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from users.models import UserRelationship, NewUser
from users.constants import RELATIONSHIP_STATUS_PENDING, RELATIONSHIP_STATUS_FRIENDS, RELATIONSHIP_STATUS_FOLLOWING
from users.factories import UserModelFactory, BaseUserRelationshipModelFactory, FollowingUserRelationshipModelFactory, FriendsUserRelationshipModelFactory, ProfileModelFactory
from nodes.factories import NodeModelFactory
from blockbuster import settings
from posts.factories import BasePostModelFactory
from users.models import Profile


class ProfilePostsListViewTestCase(APITestCase):
    def test_get_stream_success_no_foreign_posts(self):
        # Given a user is authenticated
        authed_user = UserModelFactory()
        local_friend = UserModelFactory()
        friendship = FriendsUserRelationshipModelFactory(initiator=authed_user.profile, receiver=local_friend.profile)
        post = BasePostModelFactory(author=local_friend.profile)
        self.client.force_authenticate(user=authed_user)

        url = '/api/author/posts/'

        # WHEN the request is made
        response = self.client.get(url)
        # THEN posts are returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)

    @unittest.skipIf(not settings.NODE_TESTING, 'must allow node testing')
    def test_get_stream_success_with_foreign_post(self):
        """
        WARNING must have local server running on port 9000 with a user in db with the credentials below!
        """
        # Given a user is authenticated
        authed_user = UserModelFactory()
        node = NodeModelFactory(host='http://127.0.0.1:9000/')
        foreign_friend = Profile.objects.create(username='random', host=node.host, uuid='21d39f4d-0bd8-4602-be39-4d0534b3a02c')
        local_friend = UserModelFactory()
        friendship1 = FriendsUserRelationshipModelFactory(initiator=authed_user.profile, receiver=local_friend.profile)
        post = BasePostModelFactory(author=local_friend.profile)
        friendship2 = FriendsUserRelationshipModelFactory(initiator=authed_user.profile, receiver=foreign_friend)
        self.client.force_authenticate(user=authed_user)

        url = '/api/author/posts/'

        # WHEN the request is made
        response = self.client.get(url)

        # THEN posts are returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class ProfileViewTestCase(APITestCase):
    def test_get_local_user_is_successful(self):
        # Given an authed user tries to view a local users profile
        authed_user = UserModelFactory()
        stranger = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        url = '/api/author/%s/' % stranger.profile.uuid

        # WHEN the request is made
        response = self.client.get(url)

        # THEN the appropriate profile is returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('displayName'), stranger.username)

    @unittest.skipIf(not settings.NODE_TESTING, 'must allow node testing')
    def test_get_remote_user_is_successful(self):
        # Given an authed user tries to view a local users profile
        authed_user = UserModelFactory()
        stranger_uuid = '217458a6-618a-4301-8263-73b005ba814e' # This must be an actual user's id on a running server
        stranger = ProfileModelFactory(username='taylor', user=None, host='http://127.0.0.1:9000/', uuid=stranger_uuid)
        node = NodeModelFactory(host='http://127.0.0.1:9000/', username_for_node='pleasework', password_for_node='test')
        self.client.force_authenticate(user=authed_user)

        url = '/api/author/%s/' % (stranger.uuid)

        # WHEN the request is made
        response = self.client.get(url)

        # THEN the appropriate profile is returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('displayName'), stranger.username)


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
        url = '/api/register/'
        # WHEN the request is made
        response = self.client.post(url, data, format='json')
        #print("response is: " + str(response))
        user = NewUser.objects.get(username=username)
        # THEN the user is in the system
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.email, email)
        # AND they have a profile, no they don't, new user who are not approved does not have profiles
        #self.assertTrue(user.profile)

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
        url = '/api/register/'
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
        url = '/api/register/'
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
        friend2 = UserModelFactory()
        friendship = FriendsUserRelationshipModelFactory(initiator=authed_user.profile, receiver=friend.profile)
        friendship = FriendsUserRelationshipModelFactory(initiator=authed_user.profile, receiver=friend2.profile)
        self.client.force_authenticate(user=authed_user)

        # WHEN they request the api to view their friends list
        url = '/api/author/%s/friends/' % authed_user.profile.uuid

        response = self.client.get(url)

        # THEN the response will contain their friends
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('query'), 'friends')
        self.assertEqual(len(response.data.get('authors')), len(authed_user.profile.friends))

    def test__post_list_of_users__some_are_friends_success(self):
        # GIVEN a user has a friend
        authed_user = UserModelFactory()
        friend = UserModelFactory()
        stranger = UserModelFactory()
        friendship = FriendsUserRelationshipModelFactory(initiator=authed_user.profile, receiver=friend.profile)
        self.client.force_authenticate(user=authed_user)

        data = dict(
            query='friends',
            author=authed_user.profile.api_id,
            authors=[friend.profile.api_id, stranger.profile.api_id]
        )
        # WHEN they request the api to check a list of friends
        url = '/api/author/%s/friends/' % authed_user.profile.uuid

        response = self.client.post(url, data=data, format='json')

        # THEN the response will contain their friends
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('query'), 'friends')
        self.assertEqual(response.data.get('author'), authed_user.profile.api_id)
        self.assertEqual(response.data.get('authors')[0], friend.profile.api_id)

    def test__post_list_of_users__none_are_friends_success(self):
        # GIVEN a user has a friend
        authed_user = UserModelFactory()
        stranger = UserModelFactory()
        stranger2 = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        data = dict(
            query='friends',
            author=authed_user.profile.api_id,
            authors=[stranger2.profile.api_id, stranger.profile.api_id]
        )
        # WHEN they request the api to view their friends list
        url = '/api/author/%s/friends/' % authed_user.profile.uuid

        response = self.client.post(url, data=data, format='json')

        # THEN the response will be successful and no friends will be returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('query'), 'friends')
        self.assertEqual(response.data.get('author'), authed_user.profile.api_id)
        self.assertEqual(response.data.get('authors'), [])


class UserRelationshipFriendRequestViewSetTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        site = 'http://127.0.0.1:8000/'
        site_ob = Site.objects.get(domain='example.com')
        site_ob.domain = site
        site_ob.save()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_local_friend_request_creates_friend_request(self):
        # GIVEN an authenticated user makes a friend request for another user
        authed_user = UserModelFactory()
        friend = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        url = '/api/friendrequest/'
        data = dict(
            query='friendrequest',
            author=dict(
                id=authed_user.profile.api_id,
                displayName=authed_user.profile.username
            ),
            friend=dict(
                id=friend.profile.api_id,
                displayName=friend.profile.username
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

    def test_accept_local_friend_request_accepts_friend_request(self):
        # GIVEN a user has pending friend requests
        authed_user = UserModelFactory()
        follower1 = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        friendship1 = BaseUserRelationshipModelFactory(initiator=follower1.profile, receiver=authed_user.profile)
        self.assertEquals(friendship1.status, RELATIONSHIP_STATUS_PENDING)

        url = '/api/friendrequest/'
        data = dict(
            author=dict(
                id=follower1.profile.api_id,
                displayName=follower1.profile.username
            ),
            friend=dict(
                id=authed_user.profile.api_id,
                displayName=authed_user.profile.username
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

    def test_decline_local_friend_request_creates_following_friendship(self):
        # GIVEN a user has pending friend requests
        authed_user = UserModelFactory()
        follower1 = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        friendship1 = BaseUserRelationshipModelFactory(initiator=follower1.profile, receiver=authed_user.profile)
        self.assertEquals(friendship1.status, RELATIONSHIP_STATUS_PENDING)

        url = '/api/friendrequest/'
        data = dict(
            author=dict(
                id=follower1.profile.api_id,
                displayName=follower1.profile.username
            ),
            friend=dict(
                id=authed_user.profile.api_id,
                displayName=authed_user.profile.username
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

    def test_local_befriend_a_following_person_becomes_friends(self):
        authed_user = UserModelFactory()
        follower1 = UserModelFactory()
        self.client.force_authenticate(user=authed_user)
        # GIVEN a logged in user has someone following them
        friendship1 = FollowingUserRelationshipModelFactory(initiator=follower1.profile, receiver=authed_user.profile)
        self.assertEquals(friendship1.status, RELATIONSHIP_STATUS_FOLLOWING)

        # WHEN the logged in user wants to follow the person already following them
        url = '/api/friendrequest/'
        data = dict(
            friend=dict(
                id=follower1.profile.api_id,
                displayName=follower1.profile.username
            ),
            author=dict(
                id=authed_user.profile.api_id,
                displayName=authed_user.profile.username
            ),
        )

        # WHEN the request is made
        response = self.client.post(url, data, format='json')

        # THEN the relationship is created
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        friendship = UserRelationship.objects.get(id=friendship1.id)
        # AND friendship status should be FRIENDS
        self.assertEqual(friendship.status, RELATIONSHIP_STATUS_FRIENDS)
        self.assertEqual(friendship.receiver, follower1.profile)
        self.assertEqual(friendship.initiator, authed_user.profile)

    def test_local_get_users_friend_requests_list(self):
        # GIVEN an authenticated user has friend requests
        authed_user = UserModelFactory()
        follower1 = UserModelFactory()
        follower2 = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        friendship1 = BaseUserRelationshipModelFactory(initiator=follower1.profile, receiver=authed_user.profile)
        friendship2 = BaseUserRelationshipModelFactory(initiator=follower2.profile, receiver=authed_user.profile)
        self.assertEquals(friendship1.status, RELATIONSHIP_STATUS_PENDING)
        self.assertEquals(friendship2.status, RELATIONSHIP_STATUS_PENDING)
        url = '/api/friendrequest/'

        # WHEN the request is made
        response = self.client.get(url)

        # THEN a successful response is made
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_local_delete_relationship_when_friends__logged_in_user_is_initiator_success(self):
        # GIVEN an authenticated user has a friend and the logged in user initiated that friendship
        authed_user = UserModelFactory()
        friend = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        friendship = FriendsUserRelationshipModelFactory(initiator=authed_user.profile, receiver=friend.profile)
        self.assertEquals(friendship.status, RELATIONSHIP_STATUS_FRIENDS)
        self.assertEquals(friendship.initiator, authed_user.profile)
        self.assertEquals(friendship.receiver, friend.profile)
        # WHEN a delete request is made to the entity url
        url = '/api/friendrequest/%s/' % friendship.id

        # WHEN the request is made
        response = self.client.delete(url, format='json')

        friendship = UserRelationship.objects.get(id=friendship.id)
        # THEN a successful response is made
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The roles should be switched
        self.assertEquals(friendship.initiator, friend.profile)
        self.assertEquals(friendship.receiver, authed_user.profile)
        self.assertEquals(friendship.status, RELATIONSHIP_STATUS_FOLLOWING)

    def test_local_delete_relationship_when_friends_logged_in_user_is_receiver_success(self):
        # GIVEN an authenticated user has a friend that the friend initiated
        authed_user = UserModelFactory()
        friend = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        friendship = FriendsUserRelationshipModelFactory(receiver=authed_user.profile, initiator=friend.profile)
        self.assertEquals(friendship.status, RELATIONSHIP_STATUS_FRIENDS)
        self.assertEquals(friendship.receiver, authed_user.profile)
        self.assertEquals(friendship.initiator, friend.profile)
        # WHEN a delete request is made to the entity url
        url = '/api/friendrequest/%s/' % friendship.id

        # WHEN the request is made
        response = self.client.delete(url, format='json')

        friendship = UserRelationship.objects.get(id=friendship.id)
        # THEN a successful response is made
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The roles should be switched
        self.assertEquals(friendship.initiator, friend.profile)
        self.assertEquals(friendship.receiver, authed_user.profile)
        self.assertEquals(friendship.status, RELATIONSHIP_STATUS_FOLLOWING)

    def test_local_delete_relationship_when_other_is_following_removes_row_entirely(self):
        # GIVEN an authenticated user has a person following them
        authed_user = UserModelFactory()
        friend = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        friendship = FollowingUserRelationshipModelFactory(initiator=authed_user.profile, receiver=friend.profile)
        self.assertEquals(friendship.status, RELATIONSHIP_STATUS_FOLLOWING)
        self.assertEquals(friendship.initiator, authed_user.profile)
        self.assertEquals(friendship.receiver, friend.profile)
        url = '/api/friendrequest/%s/' % friendship.id

        # WHEN the request is made
        response = self.client.delete(url, format='json')
        # THEN there should be a successful response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # THEN an error should be raised
        with self.assertRaises(UserRelationship.DoesNotExist):
            friendship2 = UserRelationship.objects.get(id=friendship.id)

    def test_local_delete_relationship_when_pending_removes_row_entirely(self):
        # GIVEN an authenticated user has a pending relationship that the logged in user initiated
        authed_user = UserModelFactory()
        friend = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        friendship = BaseUserRelationshipModelFactory(initiator=authed_user.profile, receiver=friend.profile)
        self.assertEquals(friendship.status, RELATIONSHIP_STATUS_PENDING)
        self.assertEquals(friendship.initiator, authed_user.profile)
        self.assertEquals(friendship.receiver, friend.profile)
        url = '/api/friendrequest/%s/' % friendship.id

        # WHEN the request is made
        response = self.client.delete(url, format='json')
        # THEN there should be a successful response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # THEN an error should be raised
        with self.assertRaises(UserRelationship.DoesNotExist):
            friendship2 = UserRelationship.objects.get(id=friendship.id)

    def test_local_delete_relationship_when_invalid_pk_given(self):
        # GIVEN an authenticated user tries to delete an invalid friendship object
        authed_user = UserModelFactory()
        # friend = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        # friendship = BaseUserRelationshipModelFactory(initiator=authed_user.profile, receiver=friend.profile)
        # self.assertEquals(friendship.status, RELATIONSHIP_STATUS_PENDING)
        # self.assertEquals(friendship.initiator, authed_user.profile)
        # self.assertEquals(friendship.receiver, friend.profile)
        url = '/api/friendrequest/9999/'

        # WHEN the request is made
        response = self.client.delete(url, format='json')

        # THEN there should be a successful response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_local_delete_relationship_when_another_relationships_pk_given(self):
        # GIVEN an authenticated user tries to delete an invalid friendship object
        authed_user = UserModelFactory()
        random = UserModelFactory()
        friend = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        friendship = BaseUserRelationshipModelFactory(initiator=random.profile, receiver=friend.profile)
        self.assertEquals(friendship.status, RELATIONSHIP_STATUS_PENDING)
        self.assertEquals(friendship.initiator, random.profile)
        self.assertEquals(friendship.receiver, friend.profile)
        url = '/api/friendrequest/%s/' % friendship.id

        # WHEN the request is made
        response = self.client.delete(url, format='json')

        # THEN there should be a successful response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, 'You do not have access to this friendship.')

    @unittest.skipIf(not settings.NODE_TESTING, 'must allow node testing')
    def test_foreign_friend_request_creates_friend_request(self):
        """
        TRUST ME THIS WORKS. ITS A HEADACHE TO TEST
        you must run you live server, use valid friend info, and foreign_author info must match a node
        """
        # GIVEN a foreign user asks to befriend a user on our server. The foreign host is trusted
        node = NodeModelFactory(user=user, host='http://127.0.0.1:8005/')
        foreign_author = dict(
            id = '%sapi/author/de305d54-75b4-431b-adb2-eb6b9e546011' % node.host,
            displayName='bro',
            host=node.host,
        )
        # This friend must be a profile on the local server
        friend = dict(
            id = 'http://127.0.0.1:8000/api/author/217458a6-618a-4301-8263-73b005ba814e',
            displayName='taylor',
            host='http://127.0.0.1:8000/'
        )

        url = 'http://127.0.0.1:8000/api/friendrequest/'
        data = dict(
            author=foreign_author,
            friend=friend
        )

        # WHEN the request is made
        response = requests.post(url, json=data, auth=('pleasework', 'test'))

        # THEN the relationship is created
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @unittest.skipIf(not settings.NODE_TESTING, 'must allow node testing')
    def test_live_site_friending(self):
        """
        TRUST ME THIS WORKS. ITS A HEADACHE TO TEST
        you must run you live server, use valid friend info, and foreign_author info must match a node
        """
        # GIVEN a foreign user asks to befriend a user on our server. The foreign host is trusted
        node = NodeModelFactory(host='http://warm-hollows-14698.herokuapp.com/')
        server1 = dict(
            id='%sapi/author/385cbe9b-e95c-4251-a2c1-9a6a08e5797e' % node.host,
            displayName='aaron',
            host=node.host,
        )
        # This friend must be a profile on the local server
        server2 = dict(
            id='http://radiant-beyond-17792.herokuapp.com/api/author/cc3c8875-49ca-4b65-8519-cce58e9ed919',
            displayName='aaron2',
            host='http://radiant-beyond-17792.herokuapp.com/'
        )

        url = 'http://radiant-beyond-17792.herokuapp.com/api/friendrequest/'
        data = dict(
            author=server1,
            friend=server2
        )

        # WHEN the request is made
        response = requests.post(url, json=data, auth=('aaron3', '123456'))

        # THEN the relationship is created
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_foreign_friend_request_creates_friend_request_untrusted_node_fails(self):
        # GIVEN a foreign user asks to befriend a user on our server. The foreign host is NOT trusted
        foreign_author = dict(
            id = 'http://www.untristed.com/api/author/de305d54-75b4-431b-adb2-eb6b9e546013',
            displayName='foreigner'
        )
        friend = UserModelFactory()

        url = '/api/friendrequest/'
        data = dict(
            author=foreign_author,
            friend=dict(
                id=friend.profile.api_id,
                displayName=friend.profile.username
            ),
        )

        # WHEN the request is made
        response = self.client.post(url, data, format='json')

        # THEN an error is raised
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    @unittest.skipIf(not settings.NODE_TESTING, 'must allow node testing')
    def test_request_to_foreign_user_friend_success(self):
        # GIVEN a local authed user asks to befriend a user on another trusted server.
        node = NodeModelFactory(host='http://127.0.0.1:9000/', username_for_node='pleasework', password_for_node='test')
        friend = dict(
            displayName='taylor',
            id = '%s/api/author/217458a6-618a-4301-8263-73b005ba814e' % node.host,
            host=node.host
        )
        author = UserModelFactory()
        self.client.force_authenticate(user=author)

        url = '/api/friendrequest/'
        data = dict(
            friend=friend,
            author=dict(
                id=author.profile.api_id,
                displayName=author.profile.username,
                host=author.profile.host
            ),
        )

        # WHEN the request is made
        response = self.client.post(url, data, format='json')

        # THEN the relationship is created
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        friendship = UserRelationship.objects.all()[0]
        # AND friendship status should be PENDING by default
        self.assertEqual(friendship.status, RELATIONSHIP_STATUS_PENDING)
        self.assertEqual(friendship.initiator.api_id, author.profile.api_id)
        self.assertEqual(friendship.receiver.api_id, friend['id'])


class UserRelationshipCheckViewTestCase(APITestCase):
    def test_check_two_uuids_are_friends_success(self):
        # GIVEN two users are friends
        friend1 = UserModelFactory()
        friend2 = UserModelFactory()
        authed = UserModelFactory()

        self.client.force_authenticate(user=authed)

        friendship = FriendsUserRelationshipModelFactory(initiator=friend1.profile, receiver=friend2.profile)
        url = '/api/author/%s/friends/%s/' % (friend1.profile.uuid, friend2.profile.uuid)

        # WHEN the request is made
        response = self.client.get(url)

        # THEN a successful response is made and the boolean is true
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('friends'))

    def test_check_two_uuids_are_friends_fails(self):
        # GIVEN two users are not friends
        friend1 = UserModelFactory()
        friend2 = UserModelFactory()
        authed = UserModelFactory()
        self.client.force_authenticate(user=authed)

        friendship = FollowingUserRelationshipModelFactory(initiator=friend1.profile, receiver=friend2.profile)
        url = '/api/author/%s/friends/%s/' % (friend1.profile.uuid, friend2.profile.uuid)

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
        url = '/api/author/me/relationship/%s/' % follower1.profile.uuid

        # WHEN the request is made
        response = self.client.get(url)

        # THEN a successful response is made
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fields = ['status', 'author', 'friend']
        for field in fields:
            self.assertTrue(field in response.data)

    def test_check_relationship_exists__as_initiator_success(self):
        # GIVEN an authenticated user is friends with another person
        authed_user = UserModelFactory()
        follower1 = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        friendship1 = BaseUserRelationshipModelFactory(initiator=authed_user.profile, receiver=follower1.profile)
        self.assertEquals(friendship1.status, RELATIONSHIP_STATUS_PENDING)
        url = '/api/author/me/relationship/%s/' % follower1.profile.uuid

        # WHEN the request is made
        response = self.client.get(url)

        # THEN a successful response is made
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fields = ['status', 'author', 'friend']
        for field in fields:
            self.assertTrue(field in response.data)

    def test_relationship_when_no_relationship_exists(self):
        # GIVEN an authenticated user has no relationship with another person
        authed_user = UserModelFactory()
        follower1 = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        url = '/api/author/me/relationship/%s/' % follower1.profile.uuid

        # WHEN the request is made
        response = self.client.get(url)

        # THEN a successful response is made
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "No Relationship Found.")

    def test_relationship_when_own_uuid_given(self):
        # GIVEN an authenticated user requests a relationship with themself
        authed_user = UserModelFactory()
        self.client.force_authenticate(user=authed_user)

        url = '/api/author/me/relationship/%s/' % authed_user.profile.uuid

        # WHEN the request is made
        response = self.client.get(url)

        # THEN a successful response is made
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "The profile with the given UUID is your own.")
