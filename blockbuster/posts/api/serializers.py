from rest_framework import serializers
from posts.models import Post
from users.api.serializers import AuthorSerializer
from comments.api.serializers import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    author = AuthorSerializer(required=False)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('author', 'comments', 'content') # These fields will be available to the front end
