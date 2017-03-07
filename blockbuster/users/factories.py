import factory
from users.models import UserProfile
from users.constants import RELATIONSHIP_STATUS_FRIENDS
from users.constants import RELATIONSHIP_STATUS_FOLLOWING


class UserProfileModelFactory(factory.DjangoModelFactory):
    username = factory.Sequence(lambda n: u'User%s' % n)

    class Meta:
        model = UserProfile


class BaseUserRelationshipModelFactory(factory.DjangoModelFactory):
    initiator = factory.SubFactory(UserProfileModelFactory)
    receiver = factory.SubFactory(UserProfileModelFactory)


class FriendsUserRelationshipModelFactory(BaseUserRelationshipModelFactory):
    status = RELATIONSHIP_STATUS_FRIENDS


class FollowingUserRelationshipModelFactory(BaseUserRelationshipModelFactory):
    status = RELATIONSHIP_STATUS_FOLLOWING
