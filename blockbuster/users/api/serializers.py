from rest_framework import serializers
from users.models import Profile
from django.contrib.auth.models import User

from users.models import UserRelationship


class ProfileSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    username = serializers.CharField(read_only=False)
    uuid = serializers.CharField(read_only=False)

    class Meta:
        model = Profile
        fields = ('username', 'github', 'uuid')


class UserSerializer(serializers.ModelSerializer):
    """
    Warning: This is returning the users unhashed password to the front end. Definitely not secure.
    """
    # http://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('username', 'profile', 'email', 'password')

    def validate(self, data):
        data = super(UserSerializer, self).validate(data)
        """
        validate data here
        """

        return data

class UserRelationshipSerializer(serializers.ModelSerializer):
    initiator = ProfileSerializer(required=False)
    receiver = ProfileSerializer(required=False)

    class Meta:
        model = UserRelationship
        fields = ('initiator', 'receiver', 'status',)

    def validate(self, data):
        data = super(UserRelationship, self).validate(data)
        """
        validate data here
        """

        return data