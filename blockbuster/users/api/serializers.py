from rest_framework import serializers
from users.models import Profile
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    username = serializers.CharField(read_only=False)
    uuid = serializers.CharField(read_only=False)

    class Meta:
        model = Profile
        fields = ('username', 'github', 'uuid')


class UserSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'profile')

    # TODO might need this def create(self, validated_data):
    #     profile_data = validated_data.pop('profile')
    #     user = User.objects.create(**validated_data)
    #     Profile.objects.create(user=user, **profile_data)
    #     return user
