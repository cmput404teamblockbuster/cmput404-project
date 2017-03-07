from django.db import models
from core.utils import django_choice_options
from posts.constants import PRIVACY_TYPES, PRIVATE_TO_ALL_FRIENDS, PRIVATE_TO_ONE_FRIEND, PRIVATE_TO_ME, PRIVACY_PUBLIC


class Post(models.Model):

    PRIVACY_TYPE_OPTIONS = django_choice_options(
        PRIVACY_TYPES, 'name')

    author = models.ForeignKey('users.UserProfile', related_name='posts_created')
    private_to = models.ForeignKey('users.UserProfile', null=True, related_name='received_private_posts')  # if the privacy is PRIVATE_TO_ONE_FRIEND, this is set to the friend
    is_public = models.BooleanField(default=True)  # posts are public by default
    privacy = models.CharField(choices=PRIVACY_TYPE_OPTIONS, max_length='256', default=PRIVACY_PUBLIC)

    @property
    def viewable_to(self):
        """
        Returns: a qs of users that the post is viewable to
        """
        if self.is_public:
            return

        elif self.privacy == PRIVATE_TO_ALL_FRIENDS:
            return self.author.friends

        elif self.privacy == PRIVATE_TO_ONE_FRIEND:
            return [self.private_to]

        # elif self.privacy == self.PRIVATE_TO_FOF:
        #     return # TODO implement this

        elif self.privacy == PRIVATE_TO_ME:
            return self.author

        return []
