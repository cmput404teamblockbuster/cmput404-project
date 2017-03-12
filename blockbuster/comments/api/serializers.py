from rest_framework import serializers
from comments.models import Comment
from users.api.serializers import ProfileSerializer
from users.models import Profile
# from posts.api.serializers import PostSerializer


class CommentSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    author = ProfileSerializer()

    class Meta:
        model = Comment
        fields = ('created', 'body', 'author', 'uuid') # These fields will be available to the front end

    def validate(self, data):
        data = super(CommentSerializer, self).validate(data)
        """
        validate data here
        """
        if len(data.get('body')) == 0:
            raise serializers.ValidationError('The comment has no body.')

        return data