import uuid
from django.db import models
from core.utils import django_choice_options
from users.constants import RELATIONSHIP_STATUS_TYPES, RELATIONSHIP_STATUS_PENDING, \
    RELATIONSHIP_STATUS_FRIENDS, RELATIONSHIP_STATUS_FOLLOWING
from posts.models import Post
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)  # http://stackoverflow.com/questions/44109/extending-the-user-model-with-custom-fields-in-django
    username = models.CharField(max_length=30, blank=False, null=False, default=None,
                                editable=False)  # This will be copied from user.username
    github = models.URLField(null=True, blank=True)  # github url can be null
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

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

    def get_stream(self):
        """
        Returns: the user's stream
        """
        # TODO this should be optimized eventually
        stream = [post for post in Post.objects.filter(author=self)]
        for friend in self.friends:
            posts = Post.objects.filter(author=friend.id)
            for post in posts:
                if post.viewable_for_author(author=self):
                    stream.append(post)

        return stream

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

    # def delete(self):
    #     """
    #     overwrite delete method so unfriending keeps the other friend following as the initiator
    #     """
    #     if self.status == RELATIONSHIP_STATUS_FRIENDS:
    #         if self.initiator == 'logged in user':  # TODO this will have to be done in a serializer
    #             new_friendship = UserRelationship(initiator=self.receiver, receiver=self.initiator,
    #                                               status=RELATIONSHIP_STATUS_FOLLOWING)
    #             new_friendship.save()
    #
    #     super(UserRelationship, self).delete()

    def __str__(self):
        return '%s -> %s' % (self.initiator, self.receiver)
