from django.db import models

# Create your models here.




class node(models.Model):
    host = models.URLField(max_length=500)
    is_allowed = models.BooleanField(default = True)
    
