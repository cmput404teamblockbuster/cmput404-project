import factory
from users.models import User
from users.constants import RELATIONSHIP_STATUS_FRIENDS
from users.constants import RELATIONSHIP_STATUS_FOLLOWING


class UserModelFactory(factory.DjangoModelFactory):
    username = factory.Sequence(lambda n: u'User%s' % n)

    class Meta:
        model = User


class BaseUserRelationshipModelFactory(factory.DjangoModelFactory):
    initiator = factory.SubFactory(UserModelFactory)
    receiver = factory.SubFactory(UserModelFactory)


class FriendsUserRelationshipModelFactory(BaseUserRelationshipModelFactory):
    status = RELATIONSHIP_STATUS_FRIENDS


class FollowingUserRelationshipModelFactory(BaseUserRelationshipModelFactory):
    status = RELATIONSHIP_STATUS_FOLLOWING
