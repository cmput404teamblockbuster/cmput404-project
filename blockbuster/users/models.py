from django.db import models
from blockbuster.core.utils import django_choice_options
from blockbuster.users.constants import RELATIONSHIP_STATUS_TYPES, RELATIONSHIP_STATUS_PENDING, \
    RELATIONSHIP_STATUS_FRIENDS
from blockbuster.posts.models import Post


class User(models.model):
    username = models.CharField(max_length=50, null=False, unique=True)
    github = models.URLField(null=True, blank=True)  # github url can be null

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
        return self.username


class UserRelationship(models.model):
    RELATIONSHIP_STATUS_OPTIONS = django_choice_options(
        RELATIONSHIP_STATUS_TYPES, 'name')
    initiator = models.ForeignKey(User, null=False)  # person initiating a friendship
    receiver = models.ForeignKey(User, null=False)  # person receiving friend request
    status = models.CharField(RELATIONSHIP_STATUS_OPTIONS, max_length='100', default=RELATIONSHIP_STATUS_PENDING)

    def delete(self):
        """
        overwrite delete method so unfriending keeps the other friend following as the initiator
        """
        if self.status == self.RELATIONSHIP_STATUS_FRIENDS:
            if self.initiator == 'logged in user':  # TODO implement global to keep track of which user is logged in
                new_friendship = UserRelationship(initiator=self.receiver, receiver=self.initiator,
                                                  status=self.RELATIONSHIP_STATUS_FOLLOWING)
                new_friendship.save()

        super(UserRelationship, self).delete()
