from django.test import TestCase
from users.factories import UserModelFactory
from posts.constants import *
from posts.factories import BasePostModelFactory
from posts.models import *
from users.factories import BaseUserRelationshipModelFactory
from users.constants import *


class PostModelTestCase(TestCase):
    """
    To run these tests use the following code
    python manage.py test posts.test_models.PostModelTestCase
    """

    def test__viewable_to_specific_person_returns_that_persons_id_succesfully(self):
        # GIVEN a user
        receiver = UserModelFactory()  # all the factory does is create a user with fields filled in for us, instead of us having to do User(username='bob, github=None,...)
        author = UserModelFactory()
        # AND a post is made that is viewable to one specific person
        post = BasePostModelFactory(author=author.profile, privacy=PRIVATE_TO_ONE_FRIEND,
                                    private_to=receiver.profile)  # i did User.profile because the post expects a Profile() instance instead of a User() instance. Ill come up with a better solution later.

        # print post.viewable_to feel free debug using print statements like this

        # THEN the post's viewable_to property should return the ID of the viewable user
        self.assertEqual(len(post.viewable_to), 1)  # it should only be viewable to one person
        self.assertEqual(post.viewable_to[0], receiver.profile.uuid)  # self.assert statements are what will pass or fail

    def test__viewable_to_all(self):
        user1 = UserModelFactory()
        user2 = UserModelFactory()
        author = UserModelFactory()
        post = BasePostModelFactory(author=author.profile, privacy=PRIVACY_PUBLIC)

        # Public post returns empty list for viewable to
        self.assertEqual(len(post.viewable_to), 0)

    def test__viewable_to_self(self):
        author = UserModelFactory()
        post = BasePostModelFactory(author=author.profile, privacy=PRIVATE_TO_ME)

        self.assertEqual(len(post.viewable_to), 1)
        self.assertEqual(post.viewable_to[0], author.profile.uuid)

    def test__viewable_to_friends(self):
        friend1 = UserModelFactory()
        friend2 = UserModelFactory()
        notFriend = UserModelFactory()
        author = UserModelFactory()
        post = BasePostModelFactory(author=author.profile, privacy=PRIVATE_TO_ALL_FRIENDS)

        # not sure if friends can be added this way
        # author.friends.append(friend1.id)
        # author.friends.append(friend2.id)

        friendship1 = BaseUserRelationshipModelFactory(initiator=author.profile, receiver=friend1.profile,
                                                       status=RELATIONSHIP_STATUS_FRIENDS)
        friendship2 = BaseUserRelationshipModelFactory(initiator=author.profile, receiver=friend2.profile,
                                                       status=RELATIONSHIP_STATUS_FRIENDS)

        self.assertEqual(len(post.viewable_to), 2)
        self.assertTrue(friend1.profile.uuid in post.viewable_to)
        self.assertTrue(friend2.profile.uuid in post.viewable_to)
        self.assertFalse(notFriend.profile.uuid in post.viewable_to)

    # TODO: viewable_to_fof isn't working yet
    # def test__viewable_to_fof(self):
    #     friend1 = UserModelFactory()
    #     friend2 = UserModelFactory()
    #     fof1 = UserModelFactory()
    #     fof2 = UserModelFactory()
    #     notFriend = UserModelFactory()
    #     author = UserModelFactory()
    #
    #     post = BasePostModelFactory(author=author.profile, privacy=PRIVATE_TO_FOF)
    #
    #     # author.friends.append(friend1.id)
    #     # author.friends.append(friend2.id)
    #
    #     # friend1.friends.append(fof1.id)
    #     # friend2.friends.append(fof2.id)
    #
    #     friendship1 = BaseUserRelationshipModelFactory(initiator=author.profile, receiver=friend1.profile,
    #                                                    status=RELATIONSHIP_STATUS_FRIENDS)
    #     friendship2 = BaseUserRelationshipModelFactory(initiator=author.profile, receiver=friend2.profile,
    #                                                    status=RELATIONSHIP_STATUS_FRIENDS)
    #
    #     fof1 = BaseUserRelationshipModelFactory(initiator=friend1.profile, receiver=fof1.profile,
    #                                             status=RELATIONSHIP_STATUS_FRIENDS)
    #     fof2 = BaseUserRelationshipModelFactory(initiator=friend2.profile, receiver=fof2.profile,
    #                                             status=RELATIONSHIP_STATUS_FRIENDS)
    #
    #     self.assertEqual(len(post.viewable_to), 4)
    #     self.assertTrue(friend1.id in post.viewable_to)
    #     self.assertTrue(friend2.id in post.viewable_to)
    #     self.assertTrue(fof1.id in post.viewable_to)
    #     self.assertTrue(fof2.id in post.viewable_to)
    #     self.assertFalse(notFriend.id in post.viewable_to)

    def test__create(self):
        author = UserModelFactory()
        post = BasePostModelFactory(author=author.profile, privacy=PRIVACY_PUBLIC)
        # Make sure post is created
        self.assertTrue(isinstance(post, Post))
        # Make sure uuid is generated
        self.assertTrue(post.uuid)
