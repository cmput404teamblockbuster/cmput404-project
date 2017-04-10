import uuid
import datetime
from django.db import models
from core.utils import django_choice_options
from posts.constants import PRIVACY_TYPES, PRIVATE_TO_ALL_FRIENDS, PRIVACY_PRIVATE, PRIVACY_PRIVATE, PRIVACY_PUBLIC, \
PRIVATE_TO_FOAF, PRIVACY_UNLISTED,PRIVACY_SERVER_ONLY,contentchoices,text_markdown,text_plain,binary,png,jpeg
from django.contrib.sites.models import Site
site_name = Site.objects.get_current().domain
from users.utils import determine_if_foaf


class Post(models.Model):
    PRIVACY_TYPE_OPTIONS = django_choice_options(
        PRIVACY_TYPES, 'name')
    title = models.CharField(max_length=100, null=True, blank=True)
    source = models.URLField(max_length=100, null=True, blank=True, help_text='Where the post was last from')
    origin = models.URLField(max_length=100, null=True, blank=True, help_text='Where the post originated')
    description = models.CharField(max_length=150, null=True, blank=True)
    created = models.DateTimeField(null=True, editable=False)
    author = models.ForeignKey('users.Profile', related_name='posts')

    private_to = models.ManyToManyField('users.Profile',related_name="allowed_author",blank=True)
    unlisted = models.BooleanField(default=False)

    
      # if the privacy is PRIVATE_TO_ONE_FRIEND, this is set to the friend
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
        if self.privacy == PRIVATE_TO_ALL_FRIENDS or self.privacy == PRIVATE_TO_FOAF:
            return [friend.uuid for friend in self.author.friends]

        elif self.privacy == PRIVACY_SERVER_ONLY:
            viewList = []
            site_name = Site.objects.get_current().domain
            for friend in self.author.friends:
                if friend.host == site_name:
                    viewList.append(friend.uuid)
            return viewList

        elif self.privacy == PRIVACY_PRIVATE:
            array = [author.uuid for author in self.private_to.all()]
            array.append(self.author.uuid)
            return array

        return []

    def viewable_for_author(self, author):
        """
        will check to see if the given author can see the post
        Returns: boolean
        """
        if self.author == author and self.privacy != PRIVACY_UNLISTED: # authors can always see their own posts
            return True

        if self.privacy == PRIVACY_SERVER_ONLY and author.host == site_name and author in author.friends:
            return True

        if self.privacy == PRIVACY_PUBLIC or author.uuid in self.viewable_to:
            return True

        if self.privacy == PRIVATE_TO_FOAF:
            if determine_if_foaf(self.author, author):
                return True

        return False

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.now().isoformat()
            self.source = '%sposts/%s/' % (site_name, self.uuid)
            self.origin = '%sposts/%s/' % (site_name, self.uuid)
        else:
            if self.privacy != PRIVACY_PRIVATE:
                self.private_to = []

        if self.privacy == PRIVACY_UNLISTED:
            self.unlisted = True
        else:
            self.unlisted = False
            
        return super(Post, self).save(*args, **kwargs)


    def __str__(self):
        return 'post by %s (type: %s, ID: %s) %s' % (self.author.username, self.contentType, self.id, self.content if self.contentType==text_plain else '')

    class Meta:
        ordering = ('-created',)
