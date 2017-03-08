from rest_framework import serializers
from comments.models import Comment

from users.api.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    author = UserSerializer()
    class Meta:
        model = Comment
        fields = ('created', 'body', 'author') # These fields will be available to the front end
