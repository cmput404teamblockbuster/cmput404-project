from django.test import TestCase
from users.factories import UserModelFactory
from posts.constants import PRIVATE_TO_ONE_FRIEND
from posts.factories import BasePostModelFactory


class PostModelTestCase(TestCase):
    """
    To run these tests use the following code
    python manage.py test posts.test_models.PostModelTestCase
    """
    def test__viewable_to_specific_person_returns_that_persons_id_succesfully(self):
        # GIVEN a user
        receiver = UserModelFactory() # all the factory does is create a user with fields filled in for us, instead of us having to do User(username='bob, github=None,...)
        author = UserModelFactory()
        # AND a post is made that is viewable to one specific person
        post = BasePostModelFactory(author=author.profile, privacy=PRIVATE_TO_ONE_FRIEND, private_to=receiver.profile) # i did User.profile because the post expects a Profile() instance instead of a User() instance. Ill come up with a better solution later.

        # print post.viewable_to feel free debug using print statements like this

        # THEN the post's viewable_to property should return the ID of the viewable user
        self.assertEqual(len(post.viewable_to), 1) # it should only be viewable to one person
        self.assertEqual(post.viewable_to[0], receiver.id) # self.assert statements are what will pass or fail