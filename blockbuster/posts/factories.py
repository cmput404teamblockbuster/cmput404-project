import factory

from posts.constants import PRIVACY_PUBLIC
from posts.models import Post

from users.factories import UserProfileModelFactory


class BasePostModelFactory(factory.DjangoModelFactory):
    author = factory.SubFactory(UserProfileModelFactory)
    is_public = True
    privacy = PRIVACY_PUBLIC

    class Meta:
        model = Post

