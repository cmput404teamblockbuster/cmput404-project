import uuid
from django.db import models
from core.utils import django_choice_options
from users.constants import RELATIONSHIP_STATUS_TYPES, RELATIONSHIP_STATUS_PENDING, \
    RELATIONSHIP_STATUS_FRIENDS, RELATIONSHIP_STATUS_FOLLOWING
from posts.models import Post
from posts.constants import PRIVACY_UNLISTED
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from blockbuster.settings import SITE_URL


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE, null=True, blank=True)  # http://stackoverflow.com/questions/44109/extending-the-user-model-with-custom-fields-in-django
    username = models.CharField(max_length=30, blank=False, null=False, default=None,
                                editable=False)  # This will be copied from user.username
    github = models.URLField(null=True, blank=True)  # github url can be null
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    host = models.CharField(max_length=100, default=SITE_URL)
    bio = models.CharField(max_length=150, null=True, blank=True)

    @property
    def url(self):
        """
        returns a link to the users profile on our website
        """
        return '%sprofile/%s' % (str(self.host), str(self.uuid))

    @property
    def api_id(self):
        """
        returns the url to the api to get the profile data
        """
        return '%sapi/author/%s' % (str(self.host), str(self.uuid))

    @property
    def friends(self):
        friend_uuids = []
        for r in UserRelationship.objects.select_related('initiator__uuid').filter(receiver=self.id,
                                                                                 status=RELATIONSHIP_STATUS_FRIENDS):
            friend_uuids.append(r.initiator.uuid)
        for r in UserRelationship.objects.select_related('receiver__uuid').filter(initiator=self.id,
                                                                                status=RELATIONSHIP_STATUS_FRIENDS):
            friend_uuids.append(r.receiver.uuid)

        return Profile.objects.filter(uuid__in=friend_uuids)

    def get_local_stream_and_foreign_friend_list(self):
        """
        Returns:
            local_stream: an array of post objects from our server
            foreign_friend_list: a list of friends from other server so we can get their posts
        """
        assert self.user, "There is no stream for a foreign profile."
        local_stream = [post for post in Post.objects.filter(author=self).exclude(privacy=PRIVACY_UNLISTED)]
        foreign_friend_list = []
        friends_qs = self.friends
        following_ids = (r.receiver.id for r in UserRelationship.objects.filter(initiator=self,
                                                                                status__in=[
                                                                                    RELATIONSHIP_STATUS_FOLLOWING,
                                                                                    RELATIONSHIP_STATUS_PENDING]))
        following_qs = Profile.objects.filter(id__in=following_ids)
        authors = friends_qs | following_qs
        for author in authors:
            if author.host == SITE_URL:
                posts = Post.objects.filter(author=author.id)
                for post in posts:
                    if post.viewable_for_author(author=self):
                        local_stream.append(post)
            else: # we have to get the posts from their server
                foreign_friend_list.append(author)

        return local_stream, foreign_friend_list

    def delete_this(self):
        friends_qs = self.friends
        following_qs = (r.receiver for r in UserRelationship.objects.filter(initiator=self, status__in=[RELATIONSHIP_STATUS_FOLLOWING, RELATIONSHIP_STATUS_PENDING]))
        authors = friends_qs | following_qs
    def __str__(self):
        return self.username  # TODO this should be the url of their profile

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        '''
            from https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
        '''
        if created:
            u_p = Profile.objects.create(user=instance, username=instance.username)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        Profile.objects.get(user=instance, username=instance.username).save()


class UserRelationship(models.Model):
    """
    we must create a user on our db for every friend outside our db
    """
    RELATIONSHIP_STATUS_OPTIONS = django_choice_options(
        RELATIONSHIP_STATUS_TYPES, 'name')
    initiator = models.ForeignKey('users.Profile', null=False,
                                  related_name='initiated_relationships')  # person initiating a friendship
    receiver = models.ForeignKey('users.Profile', null=False,
                                 related_name='received_relationships')  # person receiving friend request
    status = models.CharField(choices=RELATIONSHIP_STATUS_OPTIONS, max_length='100',
                              default=RELATIONSHIP_STATUS_PENDING)

    class Meta:
        unique_together = (('initiator', 'receiver'),)

    def __str__(self):
        return '%s -> %s' % (self.initiator, self.receiver)
