from rest_framework import serializers
from users.models import UserProfile


class AuthorSerializer(serializers.ModelSerializer):
    # http://www.django-rest-framework.org/api-guide/relations/#nested-relationships

    class Meta:
        model = UserProfile
        fields = ('username', 'github')
