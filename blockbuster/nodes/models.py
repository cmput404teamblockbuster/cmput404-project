from django.db import models

# Create your models here.




class node(models.Model):
    url = models.URLField(max_length=500)
    permission = models.BooleanField()
    
