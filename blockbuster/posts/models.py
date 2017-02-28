from django.db import models
from core.utils import django_choice_options


class Post(models.model):

    (PRIVATE_TO_ALL_FRIENDS, PRIVATE_TO_ONE_FRIEND, PUBLIC, PRIVATE_TO_FOF) = (
        'private_to_all_friends', 'private_to_one_friend', 'public', 'private_to_fof')

    PRIVACY_TYPES = {
        PRIVATE_TO_ALL_FRIENDS: {
            'name': 'Friends',
        },
        PRIVATE_TO_ONE_FRIEND: {
            'name': 'One Friend'
        },
        PUBLIC: {
            'name': 'Public'
        },
        PRIVATE_TO_FOF: {
            'name': 'Friends-of-Friends'
        },
    }
    PRIVACY_TYPE_OPTIONS = django_choice_options(
        PRIVACY_TYPES, 'name')

    author = models.ForeignKey(User)
    private_to = models.ForeignKey(User, null=True) # if the privacy is PRIVATE_TO_ONE_FRIEND, this is set to the friend
    is_public = models.BooleanField(default=True) # posts are public by default
    privacy = models.CharField(choices=PRIVACY_TYPE_OPTIONS, max_length='256')

    @property
    def viewable_to(self):
        """
        Returns: a qs of users that the post is viewable to
        """
        if self.is_public:
            return

        elif self.privacy == self.PRIVACY_TYPES.PRIVATE_TO_ALL_FRIENDS:
            return self.friends

        elif self.privacy == self.PRIVACY_TYPES.PRIVATE_TO_ONE_FRIEND:
            return [self.private_to]

        elif self.privacy == self.PRIVACY_TYPES.PRIVATE_TO_FOF:
            return # TODO implement this

        return []


