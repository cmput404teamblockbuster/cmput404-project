import factory

from posts.constants import PRIVACY_PUBLIC, text_plain
from posts.models import Post
from users.factories import UserModelFactory


class BasePostModelFactory(factory.DjangoModelFactory):
    author = factory.SubFactory(UserModelFactory)
    privacy = PRIVACY_PUBLIC
    content = 'This is a post!'
    contentType = text_plain

    class Meta:
        model = Post
