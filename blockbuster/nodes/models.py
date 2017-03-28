from django.db import models
from django.contrib.auth.models import User


class Node(models.Model):
    host = models.URLField(max_length=500, unique=True)
    is_allowed = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    username_for_node = models.CharField(max_length=60, null=True, blank=True)
    password_for_node = models.CharField(max_length=60, null=True, blank=True)
    api_endpoint = models.CharField(max_length=30, blank=True, help_text="the root for their api access.")

    def save(self, *args, **kwargs):
        try:
            if self.user.profile:
                self.user.profile.delete()
        except:
            pass
        super(Node, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user.username)

