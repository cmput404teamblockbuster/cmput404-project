import factory

from users.factories import UserModelFactory
from posts.factories import BasePostModelFactory
from comments.models import Comment


class CommentModelFactory(factory.DjangoModelFactory):
    author = factory.SubFactory(UserModelFactory)
    post = factory.SubFactory(BasePostModelFactory)
    body = factory.Sequence(lambda n: u'%s This is my comment!' % n)

    class Meta:
        model = Comment

