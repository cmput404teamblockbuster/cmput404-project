from django.db import models


class Node(models.Model):
    host = models.URLField(max_length=500)
    is_allowed = models.BooleanField(default=True)
