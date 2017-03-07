from django.db import models
from django.utils import timezone


class Comment(models.Model):
    created = models.DateTimeField(null=True, editable=False)
    author = models.ForeignKey('users.UserProfile', null=False)
    body = models.CharField(max_length=500)
    post = models.ForeignKey('posts.Post', null=False, related_name='comments')

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        # http://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add/1737078#1737078 Muhammad Usman
        if not self.id:
            self.created = timezone.now()
        return super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return self.body
