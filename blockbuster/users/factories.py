import factory
from django.db.models.signals import post_save
from users.models import UserProfile
from users.constants import RELATIONSHIP_STATUS_FRIENDS
from users.constants import RELATIONSHIP_STATUS_FOLLOWING
from django.contrib.auth.models import User


class UserProfileModelFactory(factory.DjangoModelFactory):
    user = factory.SubFactory('users.factories.UserFactory') # from http://factoryboy.readthedocs.io/en/latest/recipes.html?highlight=UserModelFactory

    class Meta:
        model = UserProfile


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Sequence(lambda n: "user_%d" % n)

    # We pass in 'user' to link the generated Profile to our just-generated User
    # This will call UserProfileModelFactory(user=our_new_user), thus skipping the SubFactory.
    # user_profile = factory.RelatedFactory(UserProfileModelFactory, 'user')

    profile = factory.RelatedFactory(UserProfileModelFactory, 'user')
    @classmethod
    def _generate(cls, create, attrs):
        """Override the default _generate() to disable the post-save signal."""

        # Note: If the signal was defined with a dispatch_uid, include that in both calls.
        post_save.disconnect(User)
        user = super(UserFactory, cls)._generate(create, attrs)
        post_save.connect(User)
        return user


class BaseUserRelationshipModelFactory(factory.DjangoModelFactory):
    initiator = factory.SubFactory(UserProfileModelFactory)
    receiver = factory.SubFactory(UserProfileModelFactory)


class FriendsUserRelationshipModelFactory(BaseUserRelationshipModelFactory):
    status = RELATIONSHIP_STATUS_FRIENDS


class FollowingUserRelationshipModelFactory(BaseUserRelationshipModelFactory):
    status = RELATIONSHIP_STATUS_FOLLOWING
