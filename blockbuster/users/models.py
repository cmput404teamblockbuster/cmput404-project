from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from core.utils import django_choice_options
from users.constants import RELATIONSHIP_STATUS_TYPES, RELATIONSHIP_STATUS_PENDING, \
    RELATIONSHIP_STATUS_FRIENDS, RELATIONSHIP_STATUS_FOLLOWING
from posts.models import Post
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    # TODO add fields from example-article.json
    user = models.OneToOneField(User, on_delete=models.CASCADE)# http://stackoverflow.com/questions/44109/extending-the-user-model-with-custom-fields-in-django
    github = models.URLField(null=True)  # github url can be null

    @property
    def friends(self):
        friend_ids = []
        for r in UserRelationship.objects.select_related('initiator__id').filter(receiver=self.id,
                                                                                 status=RELATIONSHIP_STATUS_FRIENDS):
            friend_ids.append(r.initiator.id)
        for r in UserRelationship.objects.select_related('receiver__id').filter(initiator=self.id,
                                                                                status=RELATIONSHIP_STATUS_FRIENDS):
            friend_ids.append(r.receiver.id)

        return User.objects.filter(pk__in=friend_ids)

    def get_stream(self):
        # TODO this needs to be optimized. This will result in a ton of DB queries
        stream = []
        for friend in self.friends:
            posts = Post.objects.filter(author=friend.id)
            for post in posts:
                if self.id in post.viewable_to or post.is_public:
                    stream.append(post)

    def __str__(self):
        return self.user.username # TODO this should be the url of their profile

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        '''
            from https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
        '''
        if created:
            u_p = Profile.objects.create(user=instance)


    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        # instance.user_profile.save() TODO figure out profile save http://factoryboy.readthedocs.io/en/latest/recipes.html?highlight=UserModelFactory
        Profile.objects.get(user=instance).save()


class UserRelationship(models.Model):
    RELATIONSHIP_STATUS_OPTIONS = django_choice_options(
        RELATIONSHIP_STATUS_TYPES, 'name')
    initiator = models.ForeignKey(AUTH_USER_MODEL, null=False, related_name='initiated_relationships')  # person initiating a friendship
    receiver = models.ForeignKey(AUTH_USER_MODEL, null=False, related_name='received_relationships')  # person receiving friend request
    status = models.CharField(RELATIONSHIP_STATUS_OPTIONS, max_length='100', default=RELATIONSHIP_STATUS_PENDING)

    class Meta:
        unique_together = (('initiator', 'receiver'),)

    def delete(self):
        """
        overwrite delete method so unfriending keeps the other friend following as the initiator
        """
        if self.status == RELATIONSHIP_STATUS_FRIENDS:
            if self.initiator == 'logged in user':  # TODO implement global to keep track of which user is logged in
                new_friendship = UserRelationship(initiator=self.receiver, receiver=self.initiator,
                                                  status=RELATIONSHIP_STATUS_FOLLOWING)
                new_friendship.save()

        super(UserRelationship, self).delete()
