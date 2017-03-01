from django.db import models
from django.utils import timezone

from blockbuster.users.models import User


class Comment(models.model):
    created = models.DateTimeField(null=True, editable=False)
    author = models.ForeignKey(User, null=False)
    message = models.CharField(max_length=500)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        # http://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add/1737078#1737078 Muhammad Usman
        if not self.id:
            self.created = timezone.now()
        return super(Comment, self).save(*args, **kwargs)
