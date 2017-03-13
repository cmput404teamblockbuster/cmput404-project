from django.http import JsonResponse
from rest_framework import viewsets
from users.models import Profile
from users.api.serializers import ProfileSerializer
from users.api.serializers import UserRelationshipSerializer
from users.models import UserRelationship
from users.constants import RELATIONSHIP_STATUS_FRIENDS


class ProfileViewSet(viewsets.ModelViewSet):
    """
    refer to http://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
    """
    lookup_field = 'uuid'
    lookup_value_regex = '[^/]+'
    serializer_class = ProfileSerializer
    model = Profile
    queryset = Profile.objects.all()


class UserRelationshipViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    lookup_value_regex = '[^/]+'
    serializer_class = UserRelationshipSerializer
    model = UserRelationship

    def list(self, request, uuid):
        requested_profile = Profile.objects.get(uuid=uuid)
        qs1 = UserRelationship.objects.filter(initiator=requested_profile, status=RELATIONSHIP_STATUS_FRIENDS)
        qs2 = UserRelationship.objects.filter(receiver=requested_profile, status=RELATIONSHIP_STATUS_FRIENDS)
        result = qs1 | qs2
        serializer = UserRelationshipSerializer(result, many=True)
        return JsonResponse(serializer.data, safe=False)
