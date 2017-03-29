from rest_framework import serializers
from users.models import Profile
from django.contrib.auth.models import User
from users.models import UserRelationship
from users.constants import RELATIONSHIP_STATUS_FRIENDS, RELATIONSHIP_STATUS_PENDING


class ProfileSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    displayName = serializers.CharField(source='username', read_only=False)
    id = serializers.CharField(source='api_id')

    class Meta:
        model = Profile
        fields = ('id', 'displayName', 'github', 'host', 'url')


class CondensedProfileSerializer(serializers.ModelSerializer):
    """
    serializes less fields than the ProfileSerializer
    """
    id = serializers.CharField(source='api_id')
    displayName = serializers.CharField(source='username')

    class Meta:
        model = Profile
        fields = ('id', 'host', 'displayName', 'url')


class FullProfileSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    displayName = serializers.CharField(source='username')
    friends = CondensedProfileSerializer(many=True)
    id = serializers.CharField(source='api_id')

    class Meta:
        model = Profile
        fields = ('id', 'displayName', 'github', 'host', 'url', 'friends', 'bio')


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
    author = CondensedProfileSerializer(source='initiator')
    friend = CondensedProfileSerializer(source='receiver')

    class Meta:
        model = UserRelationship
        fields = ('author', 'friend', 'status', 'id')

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
            initiator = Profile.objects.get(username=initiator_data.get('username'))
            receiver = Profile.objects.get(username=receiver_data.get('username'))
            validated_data['initiator'] = initiator
            validated_data['receiver'] = receiver

        existing_relationship, create_friendship = self.get_existing_relationship(validated_data)
        if existing_relationship:
            existing_relationship.initiator = validated_data.get('initiator')
            existing_relationship.receiver = validated_data.get('receiver')
            if create_friendship:
                existing_relationship.status = RELATIONSHIP_STATUS_FRIENDS
            else:
                existing_relationship.status = validated_data.get('status')
            relationship = existing_relationship
            relationship.save()

        else:
            relationship = UserRelationship.objects.create(**validated_data)

        return relationship

    def get_existing_relationship(self, data):
        """
        convenient function that looks for an existing relationship between
        the two given profiles and returns it if found. Otherwise it returns None.

        create_friendship = a boolean indicating a friendship should occur
        """
        create_friendship = False
        qs1 = UserRelationship.objects.filter(initiator=data.get('initiator'),receiver=data.get('receiver'))
        qs2 = UserRelationship.objects.filter(receiver=data.get('initiator'), initiator=data.get('receiver'))
        if qs2: # This means that the author is trying to follow someone currently following them. They should become friends!
            create_friendship = True
        qs = qs1 | qs2
        return qs[0] if qs else None, create_friendship