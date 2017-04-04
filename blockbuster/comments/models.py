import uuid
from django.db import models
from django.utils import timezone
from posts.constants import contentchoices, text_markdown, text_plain, binary, png, jpeg

class Comment(models.Model):
    created = models.DateTimeField(null=True, editable=False)
    author = models.ForeignKey('users.Profile', null=False)
    body = models.CharField(max_length=500)
    post = models.ForeignKey('posts.Post', null=False, related_name='comments')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    contentType = models.CharField(
        max_length=50,
        choices=contentchoices,
        default=text_plain,
    )


    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        # http://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add/1737078#1737078 Muhammad Usman
        if not self.id:
            self.created = timezone.now()
        return super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return self.body

    class Meta:
        ordering = ('created',)
