import factory

from posts.constants import PRIVACY_PUBLIC
from posts.models import Post

from users.factories import UserModelFactory

from posts.constants import PRIVATE_TO_ONE_FRIEND

from users.factories import ProfileModelFactory


class BasePostModelFactory(factory.DjangoModelFactory):
    author = factory.SubFactory(UserModelFactory)
    privacy = PRIVACY_PUBLIC
    content = 'This is a post!'

    class Meta:
        model = Post
