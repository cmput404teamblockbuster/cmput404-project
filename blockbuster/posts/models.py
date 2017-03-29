import uuid
from django.db import models
from core.utils import django_choice_options
from django.utils import timezone
from posts.constants import PRIVACY_TYPES, PRIVATE_TO_ALL_FRIENDS, PRIVATE_TO_ONE_FRIEND, PRIVATE_TO_ME, PRIVACY_PUBLIC, \
    PRIVATE_TO_FOF, PRIVACY_UNLISTED,contentchoices,text_markdown,text_plain,binary,png,jpeg


class Post(models.Model):
    PRIVACY_TYPE_OPTIONS = django_choice_options(
        PRIVACY_TYPES, 'name')
    title = models.CharField(max_length=100, null=True, blank=True)
    source = models.URLField(max_length=100, null=True, blank=True, help_text='Where the post was last from')
    origin = models.URLField(max_length=100, null=True, blank=True, help_text='Where the post originated')
    description = models.CharField(max_length=150, null=True, blank=True)
    created = models.DateTimeField(null=True, editable=False)
    author = models.ForeignKey('users.Profile', related_name='posts')
    private_to = models.ForeignKey('users.Profile', blank=True, null=True,
                                   related_name='received_private_posts')  # if the privacy is PRIVATE_TO_ONE_FRIEND, this is set to the friend
    privacy = models.CharField(choices=PRIVACY_TYPE_OPTIONS, max_length='256', default=PRIVACY_PUBLIC)
    content = models.CharField(max_length=1000000, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    contentType = models.CharField(
        max_length=50,
        choices=contentchoices,
        default=text_plain,
    )

    @property
    def viewable_to(self):
        """
        Returns: a qs of users that the post is viewable to
        """
        if self.privacy == PRIVATE_TO_ALL_FRIENDS:
            return [friend.uuid for friend in self.author.friends]

        elif self.privacy == PRIVATE_TO_ONE_FRIEND:
            return [self.private_to.uuid]

        # doesn't work
        # elif self.privacy == PRIVATE_TO_FOF:
        #    canView = []
        #    for friend in self.author.friends:
        #        if friend.id not in canView:
        #            canView.append(friend.id)
        #        for fof in friend.friends:
        #            if fof.id not in canView:
        #                canView.append(fof.id)  
        #    return canView

        elif self.privacy == PRIVATE_TO_ME:
            return [self.author.uuid]

        return []

    def viewable_for_author(self, author):
        """
        will check to see if the given author can see the post
        Returns: boolean
        """
        if self.privacy == PRIVACY_PUBLIC or author.uuid in self.viewable_to:
            return True

        return False

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return 'post by %s (type: %s, ID: %s) %s' % (self.author.username, self.contentType, self.id, self.content if self.contentType==text_plain else '')

    class Meta:
        ordering = ('-created',)
