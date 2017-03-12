from rest_framework import viewsets
from users.models import Profile
from users.api.serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """
    refer to http://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
    """
    lookup_field = 'uuid'
    lookup_value_regex = '[^/]+'
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()