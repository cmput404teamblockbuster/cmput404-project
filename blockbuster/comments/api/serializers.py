from rest_framework import serializers
from comments.models import Comment

from users.api.serializers import ProfileSerializer


class CommentSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    author = ProfileSerializer()
    class Meta:
        model = Comment
        fields = ('created', 'body', 'author', 'uuid') # These fields will be available to the front end
