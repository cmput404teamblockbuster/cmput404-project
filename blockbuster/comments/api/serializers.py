from rest_framework import serializers
from comments.models import Comment
from users.api.serializers import AuthorSerializer


class CommentSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    author = AuthorSerializer()
    class Meta:
        model = Comment
        fields = ('created', 'body',) # These fields will be available to the front end
