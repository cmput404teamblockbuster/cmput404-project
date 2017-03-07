import factory

from users.factories import UserProfileModelFactory
from posts.factories import BasePostModelFactory
from comments.models import Comment


class CommentModelFactory(factory.DjangoModelFactory):
    author = factory.SubFactory(UserProfileModelFactory)
    post = factory.SubFactory(BasePostModelFactory)
    body = factory.Sequence(lambda n: u'%s This is my comment!' % n)

    class Meta:
        model = Comment

