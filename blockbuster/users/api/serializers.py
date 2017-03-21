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
    initiator = ProfileSerializer(required=False, read_only=False)
    receiver = ProfileSerializer(required=False, read_only=False)

    class Meta:
        model = UserRelationship
        fields = ('initiator', 'receiver', 'status', 'id')

    def validate(self, data):
        data = super(UserRelationshipSerializer, self).validate(data)
        """
        validate data here
        """

        return data

    def create(self, validated_data):
        """
        Create and return a UserRelationship instance
        """
        initiator_data = validated_data.pop('initiator', None)
        receiver_data = validated_data.pop('receiver', None)
        if initiator_data and receiver_data:
            initiator = Profile.objects.get(uuid=initiator_data.get('uuid'))
            receiver = Profile.objects.get(uuid=receiver_data.get('uuid'))
            validated_data['initiator'] = initiator
            validated_data['receiver'] = receiver
        defaults = None
        # status isn't required, and if not given then we are creating a relationship with the model defaults
        if 'status' in validated_data:
            defaults = {'status':validated_data.pop('status')}
        relationship, created = UserRelationship.objects.update_or_create(defaults=defaults, **validated_data) # https://docs.djangoproject.com/en/1.9/ref/models/querysets/#update-or-create
        return relationship