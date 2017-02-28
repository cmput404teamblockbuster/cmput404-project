from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50, required=True, unique=True)
    github = models.URLField(null=True, blank=True) # github url can be null


