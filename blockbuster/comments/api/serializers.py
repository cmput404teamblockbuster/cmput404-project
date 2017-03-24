from rest_framework import serializers
from comments.models import Comment
from users.api.serializers import CondensedProfileSerializer
from users.models import Profile
# from posts.api.serializers import PostSerializer


class CommentSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    author = CondensedProfileSerializer()
    published = serializers.DateTimeField(source='created', required=False)
    id = serializers.CharField(source='uuid', required=False)
    comment = serializers.CharField(source='body')

    class Meta:
        model = Comment
        fields = ('published', 'comment', 'author', 'id') # These fields will be available to the front end

    def validate(self, data):
        data = super(CommentSerializer, self).validate(data)
        """
        validate data here
        """
        if len(data.get('body')) == 0:
            raise serializers.ValidationError('The comment has no body.')

        return data