from django.test import TestCase
from users.factories import *
from users.constants import *
from users.models import *
from posts.factories import BasePostModelFactory
from posts.constants import *


# TODO test that UserRelationship delete method works
# Create your tests here.
class ProfileModelTestCase(TestCase):
    def test__get_stream(self):
        user = UserModelFactory()
        friend = UserModelFactory()

        friendship = FriendsUserRelationshipModelFactory(initiator=user.profile, receiver=friend.profile)

        friend_post1 = BasePostModelFactory(author=friend.profile, privacy=PRIVATE_TO_ALL_FRIENDS)
        friend_post2 = BasePostModelFactory(author=friend.profile, privacy=PRIVACY_PUBLIC)
        stream = user.profile.get_stream()

        self.assertTrue(friend_post1 in stream)
        self.assertTrue(friend_post2 in stream)

    def test__friendship(self):
        user = UserModelFactory()
        friend = UserModelFactory()

        friendship = BaseUserRelationshipModelFactory(initiator=user.profile, receiver=friend.profile,
                                                      status=RELATIONSHIP_STATUS_FRIENDS)

        self.assertEqual(friendship.status, RELATIONSHIP_STATUS_FRIENDS)
        self.assertTrue(friend.profile in user.profile.friends)
        self.assertTrue(user.profile in friend.profile.friends)

    def test__following(self):
        user = UserModelFactory()
        friend = UserModelFactory()

        following = FollowingUserRelationshipModelFactory(initiator=user.profile, receiver=friend.profile)
        self.assertEqual(following.status, RELATIONSHIP_STATUS_FOLLOWING)

    # def test__delete_friend(self):
    #     TODO delete method not implemnted yet
    #     user = UserModelFactory()
    #     friend = UserModelFactory()
    #
    #     friendship = FriendsUserRelationshipModelFactory(initiator=user.profile, receiver=friend.profile)
    #
    #     self.assertEqual(friendship.status, RELATIONSHIP_STATUS_FRIENDS)
    #     self.assertTrue(friend.id in user.profile.friends)
    #     self.assertTrue(user.id in friend.profile.friends)
    #
    #     friendship.delete()
    #     assertTrue(UserRelationship.objects.select_related('receiver__id').filter(initiator=user.profile,
    #                                                                               status=RELATIONSHIP_STATUS_FOLLOWING))
