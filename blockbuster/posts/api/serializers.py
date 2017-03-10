from rest_framework import serializers
from posts.models import Post
from comments.api.serializers import CommentSerializer

from users.api.serializers import ProfileSerializer


class PostSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    author = ProfileSerializer()
    comments = CommentSerializer(many=True, read_only=True)

    def validate(self, attrs):
        attrs = super(PostSerializer, self).validate(attrs)
        if not self._errors:
            print attrs

        return attrs

    class Meta:
        model = Post
        fields = ('author', 'comments', 'content', 'uuid') # These fields will be available to the front end
