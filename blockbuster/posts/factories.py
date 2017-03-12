import factory

from posts.constants import PRIVACY_PUBLIC
from posts.models import Post

from users.factories import UserModelFactory


class BasePostModelFactory(factory.DjangoModelFactory):
    author = factory.SubFactory(UserModelFactory)
    privacy = PRIVACY_PUBLIC

    class Meta:
        model = Post

