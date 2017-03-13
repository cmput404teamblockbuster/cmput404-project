from rest_framework import viewsets, status
from users.models import Profile, UserRelationship
from users.api.serializers import ProfileSerializer, UserRelationshipSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.constants import RELATIONSHIP_STATUS_PENDING


class ProfileViewSet(viewsets.ModelViewSet):
    """
    refer to http://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
    """
    lookup_field = 'uuid'
    lookup_value_regex = '[^/]+'
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        The current users friends list
        """
        return self.request.user.profile.friends


class UserRelationshipViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    lookup_value_regex = '[^/]+'
    serializer_class = UserRelationshipSerializer
    model = UserRelationship
    permission_classes = (IsAuthenticated,)

    def list(self, request, uuid):
        requested_profile = Profile.objects.get(uuid=uuid)
        friends = requested_profile.friends
        serializer = ProfileSerializer(friends, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserRelationshipFriendRequestViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    lookup_value_regex = '[^/]+'
    serializer_class = UserRelationshipSerializer
    model = UserRelationship
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        """
        lists all authed users pending friend requests
        """
        return UserRelationship.objects.filter(receiver=self.request.user.profile, status=RELATIONSHIP_STATUS_PENDING)

    def create(self, *args, **kwargs):
        """
        creates a user relationship via a post request to `api/friendrequest/`
        required params:
            initiator = dict containing initiating users uuid
            receiver = dict containing receiving users uuid
        """
        data = self.request.data
        serializer = UserRelationshipSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

