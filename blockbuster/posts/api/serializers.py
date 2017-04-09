from rest_framework import serializers
from posts.models import Post
from comments.api.serializers import CommentSerializer
from users.api.serializers import ProfileSerializer, CondensedProfileSerializer
from users.models import Profile
from posts.constants import PRIVACY_TYPES, PRIVATE_TO_ALL_FRIENDS, PRIVACY_PRIVATE, PRIVACY_PRIVATE, PRIVACY_PUBLIC, \
    PRIVATE_TO_FOAF, PRIVACY_UNLISTED,contentchoices,text_markdown,text_plain,binary,png,jpeg
import urllib2
from collections import OrderedDict
import json
from django.contrib.sites.models import Site

site_name = Site.objects.get_current().domain


    
                        

class PostSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    author = ProfileSerializer(required=False)
    comments = CommentSerializer(many=True, read_only=True)
    count = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    next = serializers.SerializerMethodField()
    id = serializers.CharField(source='uuid', required=False)
    visibility = serializers.CharField(source='privacy')
    contentType = serializers.ChoiceField(choices=contentchoices, required=False)
    published = serializers.CharField(source='created', required=False)
    visibleTo = serializers.SlugRelatedField(many=True, read_only=True, slug_field='url', source='private_to')

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

    def get_count(self,obj):
        #print(str(site_name+"posts/"+str(obj.uuid)+"/comments?size=5"))
        try:
            comments = urllib2.urlopen(site_name+"posts/"+str(obj.uuid)+"/comments?size=5").read()
            result = json.loads(comments)
            return len(OrderedDict(result)['comment'])
        except:
            return 1

        return len(result)
    def get_size(self,obj):
        #print(str(site_name+"posts/"+str(obj.uuid)+"/comments?size=5"))
        try: 
            comments = urllib2.urlopen(site_name+"posts/"+str(obj.uuid)+"/comments?size=5").read()
            result = json.loads(comments)
            return OrderedDict(result)['size']
        except:
            return 5


    def get_next(self,obj):
        #print(str(site_name+"posts/"+str(obj.uuid)+"/comments?size=5"))
        try:
            comments = urllib2.urlopen(site_name+"posts/"+str(obj.uuid)+"/comments?size=5").read()
            result = json.loads(comments)
            return OrderedDict(result)['next']
        except:
            return "http://random.com"

    class Meta:
        model = Post
        fields = ('title', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'comments', 'published', 'id', 'visibility', 'visibleTo', 'unlisted')  # These fields will be available to the front end
