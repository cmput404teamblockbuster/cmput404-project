from rest_framework import serializers
from posts.models import Post
from comments.api.serializers import CommentSerializer

from users.api.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    author = UserSerializer()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('author', 'comments', 'content') # These fields will be available to the front end
