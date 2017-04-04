from rest_framework import serializers
from posts.models import Post
from comments.api.serializers import CommentSerializer
from users.api.serializers import ProfileSerializer, CondensedProfileSerializer
from users.models import Profile
from posts.constants import PRIVACY_TYPES, PRIVATE_TO_ALL_FRIENDS, PRIVATE_TO, PRIVATE_TO_ME, PRIVACY_PUBLIC, \
    PRIVATE_TO_FOF, PRIVACY_UNLISTED,contentchoices,text_markdown,text_plain,binary,png,jpeg



class PostSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    author = ProfileSerializer(required=False)
    comments = CommentSerializer(many=True, read_only=True)
    id = serializers.CharField(source='uuid', required=False)
    visibility = serializers.CharField(source='privacy')
    contentType = serializers.ChoiceField(choices=contentchoices, required=False)
    published = serializers.CharField(source='created', required=False)
    visibleTo = serializers.SlugRelatedField(many=True,read_only=True,slug_field='url', source='private_to')
    query = serializers.SerializerMethodField('query_type')

    def query_type(self, obj):
        return 'posts'

    def validate(self, data):
        data = super(PostSerializer, self).validate(data)
        """
        validate data here
        """
        return data

    def create(self, validated_data):
        """
        Create and return a Post instance
        """
        # from http://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
        author_data = validated_data.pop('author', None)
        private_to_data = validated_data.pop('private_to', None)
        author_data.pop('api_id') # ignore this field
        if private_to_data:
            private_to_data.pop('api_id')  # ignore this field
            private_to, created = Profile.objects.get_or_create(**private_to_data)
            validated_data['private_to'] = private_to
        if author_data:
            author, created = Profile.objects.get_or_create(**author_data)
            validated_data['author'] = author
        return Post.objects.create(**validated_data)

    class Meta:
        model = Post
        fields = ('query', 'title', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'comments', 'published', 'id', 'visibility', 'visibleTo')  # These fields will be available to the front end
