from rest_framework import serializers
from posts.models import Post
from comments.api.serializers import CommentSerializer
from users.api.serializers import ProfileSerializer
from users.models import Profile


class PostSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    author = ProfileSerializer()
    comments = CommentSerializer(many=True, read_only=True)
    id = serializers.CharField(source='uuid', required=False)
    visibility = serializers.CharField(source='privacy')

    def validate(self, data):
        data = super(PostSerializer, self).validate(data)
        """
        validate data here
        """
        if len(data.get('content')) == 0:
            raise serializers.ValidationError('The post has no body.')

        return data

    def create(self, validated_data):
        """
        Create and return a Post instance
        """
        # from http://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
        author_data = validated_data.pop('author', None)
        if author_data:
            author, created = Profile.objects.get_or_create(**author_data)
            validated_data['author'] = author
        return Post.objects.create(**validated_data)

    class Meta:
        model = Post
        fields = ('author', 'comments', 'content', 'id', 'visibility')  # These fields will be available to the front end
