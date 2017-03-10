import uuid
from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from core.utils import django_choice_options
from django.utils import timezone
from posts.constants import PRIVACY_TYPES, PRIVATE_TO_ALL_FRIENDS, PRIVATE_TO_ONE_FRIEND, PRIVATE_TO_ME, PRIVACY_PUBLIC


class Post(models.Model):

    PRIVACY_TYPE_OPTIONS = django_choice_options(
        PRIVACY_TYPES, 'name')

    created = models.DateTimeField(null=True, editable=False)
    author = models.ForeignKey('users.Profile', related_name='posts')
    private_to = models.ForeignKey('users.Profile', blank=True, null=True, related_name='received_private_posts')  # if the privacy is PRIVATE_TO_ONE_FRIEND, this is set to the friend
    is_public = models.BooleanField(default=True)  # posts are public by default
    privacy = models.CharField(choices=PRIVACY_TYPE_OPTIONS, max_length='256', default=PRIVACY_PUBLIC)
    content = models.CharField(max_length=500, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


    @property
    def viewable_to(self):
        """
        Returns: a qs of users that the post is viewable to
        """
        if self.is_public:
            return

        elif self.privacy == PRIVATE_TO_ALL_FRIENDS:
            return [friend for friend in self.author.friends]

        elif self.privacy == PRIVATE_TO_ONE_FRIEND:
            return [self.private_to.id]

        # elif self.privacy == self.PRIVATE_TO_FOF:
        #     return # TODO implement this

        elif self.privacy == PRIVATE_TO_ME:
            return [self.author.id]

        return []

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ('created',)