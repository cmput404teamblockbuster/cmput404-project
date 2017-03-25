"""
This script will populate your DB with nodes that are accessible by the class. You must change their hosts in the admin panel afterward.

How to use this:

open the shell:
    python manage.py shell

copy and paste this document
"""
from django.contrib.auth.models import User
from nodes.models import Node

NUM_CLASS_GROUPS = 8

for i in range(1, NUM_CLASS_GROUPS + 1):
    host = "http://127.0.0.1:700%d/" % i
    team = 'team%d' % i
    user = User.objects.create(username=team, password=team)
    Node.objects.create(user=user, host=host)
    print '...%s created' % team

print Node.objects.all()  # should return a list containing new entries
print User.objects.all()  # should return a list containing new entries
