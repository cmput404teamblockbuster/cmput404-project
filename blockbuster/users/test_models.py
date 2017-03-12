from django.test import TestCase
from users.factories import *
from users.constants import *
from users.models import *
from posts.factories import BasePostModelFactory

# TODO test that UserRelationship delete method works
# Create your tests here.
class ProfileModelTestCase(TestCase):
    def test__get_stream(self):
        user = UserModelFactory()
        friend = UserModelFactory()
        #user.friends.append(friend.id)
        friendship = FriendsUserRelationshipModelFactory(initiator = user.profile, receiver = friend.profile)
        
        friend_post1 = BasePostModelFactory(author = friend.proifle, privacy = PRIVATE_TO_ALL_FRIENDS)
        friend_post2 = BasePostModelFactory(author = friend.proifle, privacy = PRIVACY_PUBLIC)
        
        stream = user.get_stream()
        self.assertTrue(friend_post1 in stream)
        self.assertTrue(friend_post2 in stream)

    def test__friendship(self):
        user = UserModelFactory()
        friend = UserModelFactory()

        friendship = FriendsUserRelationshipModelFactory(initiator = user.profile, receiver = friend.profile)

        self.assertEqual(friendship.status, RELATIONSHIP_STATUS_FRIENDS)
        self.assertTrue(friend.id in user.friends)
        self.assertTrue(user.id in friend.friends)

    def test__following(self):
        user = UserModelFactory()
        friend = UserModelFactory()
        
        following = FollowingUserRelationshipModelFactory(initiator = user.profile, receiver = friend.profile)
        self.assertEqual(following.status, RELATIONSHIP_STATUS_FOLLOWING)

    def test__delete_friend(self):
        user = UserModelFactory()
        friend = UserModelFactory()

        friendship = FriendsUserRelationshipModelFactory(initiator = user.profile, receiver = friend.profile)

        self.assertEqual(friendship.status, RELATIONSHIP_STATUS_FRIENDS)
        self.assertTrue(friend.id in user.friends)
        self.assertTrue(user.id in friend.friends)

        friendship.delete()
        assertTrue(UserRelationship.objects.select_related('receiver__id').filter(initiator = user.profile, status = RELATIONSHIP_STATUS_FOLLOWING))
