from rest_framework import viewsets
from users.models import Profile
from users.api.serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated


class ProfileViewSet(viewsets.ModelViewSet):
    """
    refer to http://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
    """
    lookup_field = 'uuid'
    lookup_value_regex = '[^/]+'
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Profile.objects.filter(uuid=self.request.user.profile.uuid)