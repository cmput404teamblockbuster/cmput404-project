import uuid
from django.db import models
from core.utils import django_choice_options
from django.utils import timezone
from posts.constants import PRIVACY_TYPES, PRIVATE_TO_ALL_FRIENDS, PRIVATE_TO_ONE_FRIEND, PRIVATE_TO_ME, PRIVACY_PUBLIC, \
PRIVATE_TO_FOF, PRIVACY_UNLISTED,PRIVACY_SERVER_ONLY,contentchoices,text_markdown,text_plain,binary,png,jpeg
from nodes.models import Node
from blockbuster import settings
import requests


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

        elif self.privacy == PRIVATE_TO_ME:
            return [self.author.uuid]

        return []

    def viewable_to_FOF(self, author_A):
        """
        Checks if the given author is friends of a friend of post's author making 
        it visible to the author
        """
        #print("ATTEMPTING FOF for post with title:", self.title)
        author_C = self.author

        list_A = None
        list_C = None
        author_B = None

        # Get the friends list of author A
        if author_A.host == settings.SITE_URL:
            list_A = author_A.friends
        elif author_A.host != settings.SITE_URL:  # The post's author is foreign
            node = Node.objects.filter(host=author_A.host, is_allowed=True)
            if node:
                node = node[0]

                api_url = '%s%sauthor/%s/friends/' % (author_A.host, node.api_endpoint, author_A.uuid)

                try:
                    #print("Attempting to retrieve friends of author_A= ", author_A)
                    response = requests.get(api_url, auth=(
                        node.username_for_node, node.password_for_node))
                except requests.ConnectionError:
                    response = None

                result = response.json() if response and 199 < response.status_code < 300 else None
                print response.text
                if (result and result.get('authors') != False):
                    list_A = result.get('authors')

        # Get the friends list of author B (Copied from directly above)
        if author_C.host == settings.SITE_URL:
            list_C = author_C.friends
        elif author_C.host != settings.SITE_URL:  # The post's author is foreign
            node = Node.objects.filter(host=author_C.host, is_allowed=True)
            if node:
                node = node[0]

                api_url = '%s%sauthor/%s/friends/' % (author_C.host, node.api_endpoint, author_C.uuid)

                try:
                    #print("Attempting to retrieve friends of author_A= ", author_C)
                    response = requests.get(api_url, auth=(
                        node.username_for_node, node.password_for_node))
                except requests.ConnectionError:
                    response = None

                result = response.json() if response and 199 < response.status_code < 300 else None
                print response.text
                if (result and result.get('authors') != False):
                    list_C = result.get('authors')

        if (list_A and list_C):

            # Look for author C who is in both lists and verify the friendships
            for friend in list_A:
                if friend in list_C:
                    author_B = friend
                    #print("found a friend of friend! - ", author_B)

                    #TODO verify the friendship of foreign servers

                    return True
        return False


    def viewable_for_author(self, author):
        """
        will check to see if the given author can see the post
        Returns: boolean
        """
        if self.privacy == PRIVACY_PUBLIC or author.uuid in self.viewable_to or self.viewable_to_FOF(author):
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
