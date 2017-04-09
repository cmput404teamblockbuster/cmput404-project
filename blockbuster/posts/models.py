import uuid
import datetime
from django.db import models
from core.utils import django_choice_options
from posts.constants import PRIVACY_TYPES, PRIVATE_TO_ALL_FRIENDS, PRIVACY_PRIVATE, PRIVACY_PRIVATE, PRIVACY_PUBLIC, \
PRIVATE_TO_FOAF, PRIVACY_UNLISTED,PRIVACY_SERVER_ONLY,contentchoices,text_markdown,text_plain,binary,png,jpeg
from nodes.models import Node
import requests
from django.contrib.sites.models import Site
site_name = Site.objects.get_current().domain


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


    def __F_verify(self, foreign, local):
        """
        Verifies that the given ids are friends by sending a /author/{author_id}/friends/{author_id}/ request
        """
        node = Node.objects.filter(host=foreign.host, is_allowed=True)
        if node:
            node = node[0]

            api_url = '%s%sauthor/%s/friends/%s' % (foreign.host, node.api_endpoint, foreign.uuid, local.uuid)

            try:
                #print("Attempting to verify friendship between:", author_B, "and", author)
                response = requests.get(api_url, auth=(
                    node.username_for_node, node.password_for_node))
            except requests.ConnectionError:
                response = None

            result = response.json() if response and 199 < response.status_code < 300 else None
            if (result and result.get('friends') != False):
                #print("friendship verified by host:", author_B.host)
                return result.get('friends')

        return False


    def __FOAF_verify(self, A, B, C):
        """
        Verifies that author B is friends of A and C. B is just the id of the author
        """

        site_name = Site.objects.get_current().domain

        #print("FOAF verifying author_B:", B)

        #if B is foreign
        if B.host != site_name:
            if self.__F_verify(B, A) == self.__F_verify(B, C) == True:
                return True

        #if B is local
        elif B.host == site_name:
            if (A in B.friends) and (C in B.friends):
                return True
        return False


    def __check_for_FOAF(self, local, foreign):
        """
        Sends an api POST request to author/{author_id}/friends/ to get a list of common friends
        """
        list_local = local.friends

        node = Node.objects.filter(host=foreign.host, is_allowed=True)
        if node:
            node = node[0]

            data = dict(
                query = "friends",
                author = foreign.api_id,
                authors = list_local
            )
            api_url = '%s%sauthor/%s/friends/' % (foreign.host, node.api_endpoint, foreign.uuid)

            try:
                #print("Attempting to retrieve common freinds from foreign author= ", foreign)
                response = requests.post(api_url, json=data, auth=(
                    node.username_for_node, node.password_for_node))
            except requests.ConnectionError:
                response = None

            result = response.json() if response and 199 < response.status_code < 300 else None
            if (result and result.get('authors') != False):
                #print("found common friends!:", result.get('authors'))
                return result.get('authors')

        return []



    def viewable_to_FOAF(self, author_A):
        """
        Checks if the given author is friends of a friend of post's author making 
        it visible to the author. Assumes that the 2 authors are not friends
        """

        if self.privacy != PRIVATE_TO_FOAF:
            return False

        print("FOAF ATTEMPTING FOAF for post with title:", self.title)
        author_C = self.author

        #list_A = None
        #list_C = None
        list_B = None
        site_name = Site.objects.get_current().domain

        # If both are local
        if author_A.host == site_name and author_C.host == site_name:
            #print("FOAF A and C are local")
            for friend in author_A.friends:
                #print("FOAF checking if:", friend, "is a common friend by using its id:", friend.api_id)
                if friend in author_C.friends:
                    author_B = friend
                    print("FOAF B found!:", author_B, "from host:", author_B.host)
                    return self.__FOAF_verify(author_A, author_B, author_C)

        local = None
        foreign = None
        if author_A.host == site_name and author_C.host != site_name:
            list_B = self.__check_for_FOAF(author_A, author_C)
            local = author_A
            foreign = author_C

        elif author_A.host != site_name and author_C.host == site_name:
            list_B = self.__check_for_FOAF(author_C, author_A)
            local = author_C
            foreign = author_A

        else: #both are not local
            return False

        if len(list_B) < 1:
            return False

        for author_B in list_B:
            for friend in local.friends:
                if author_B == friend.api_id:
                    author_B = friend
                    continue

            if(author_B.host):
                if self.__FOAF_verify(local, author_B, foreign):
                    return True

        return False


    def viewable_for_author(self, author):
        """
        will check to see if the given author can see the post
        Returns: boolean
        """
        if self.privacy == PRIVACY_SERVER_ONLY and author.host == site_name and author in author.friends:
            return True

        if self.privacy == PRIVACY_PUBLIC or author.uuid in self.viewable_to:
            return True

        if self.privacy == PRIVATE_TO_FOAF:
            if self.viewable_to_FOAF(author):
                return True
            
            
        return False

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.now().isoformat()
            self.source = '%sposts/%s/' % (site_name, self.uuid)
            self.origin = '%sposts/%s/' % (site_name, self.uuid)
        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return 'post by %s (type: %s, ID: %s) %s' % (self.author.username, self.contentType, self.id, self.content if self.contentType==text_plain else '')

    class Meta:
        ordering = ('-created',)
