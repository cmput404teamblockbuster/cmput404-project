from rest_framework import serializers
from users.models import Profile
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/relations/#nested-relationships

    class Meta:
        model = Profile
        fields = ('username', 'github', 'uuid')


class UserSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'profile')
