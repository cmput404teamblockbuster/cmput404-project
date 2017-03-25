from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from users.models import Profile, UserRelationship
from users.api.serializers import FullProfileSerializer, UserRelationshipSerializer, CondensedProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.constants import RELATIONSHIP_STATUS_PENDING, RELATIONSHIP_STATUS_FRIENDS, RELATIONSHIP_STATUS_FOLLOWING


class ProfileViewSet(viewsets.ModelViewSet):
    """
    refer to http://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
    """
    lookup_field = 'uuid'
    lookup_value_regex = '[^/]+'
    serializer_class = FullProfileSerializer
    queryset = Profile.objects.all()


class MyFriendsProfilesViewSet(viewsets.ModelViewSet):
    """
    returns the authenticated users friends list
    """
    serializer_class = CondensedProfileSerializer
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
    queryset = Profile.objects.all()

    def list(self, request, uuid):
        """
        lists a given users friends
        """
        requested_profile = Profile.objects.get(uuid=uuid)
        friends = requested_profile.friends
        data = dict(
            query='friends',
            authors=list((friend.url for friend in friends))
        )
        return Response(data=data, status=status.HTTP_200_OK)


class UserRelationshipFriendRequestViewSet(viewsets.ModelViewSet):
    serializer_class = UserRelationshipSerializer
    model = UserRelationship
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        lists all authed users pending friend requests
        """
        return UserRelationship.objects.filter(receiver=self.request.user.profile, status=RELATIONSHIP_STATUS_PENDING)

    def create_or_update(self, *args, **kwargs):
        """
        creates a user relationship via a post request to `api/friendrequest/` if initiator/receiver pair not in the DB
        required params:
            author = dict containing initiating users info
            friend = dict containing receiving users info

        otherwise it will update the UserRelationship represented by initiator/receiver pair
            to update you need to add the status param
        """
        data = self.request.data
        serializer = UserRelationshipSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def destroy(self, *args, **kwargs):
        """
        Depending on the status of the relationship, we either remove the instance entirely, or change the status around
        If friends --> the deleting user becomes receiver of a "following" relationship
        If following --> The entire UserRelationship object is removed
        """
        pk = kwargs.get('pk', None)
        instance = get_object_or_404(UserRelationship, pk=pk)
        if self.request.user.profile == instance.initiator:
            other_user_in_relationship = instance.receiver
        elif self.request.user.profile == instance.receiver:
            other_user_in_relationship = instance.initiator
        else: # otherwise the user shouldn't have access to this object
            return Response(data='You do not have access to this friendship.', status=status.HTTP_403_FORBIDDEN)

        if instance.status == RELATIONSHIP_STATUS_FRIENDS:
            # If friends then we change to following so other user can still see posts
            instance.initiator = other_user_in_relationship
            instance.receiver = self.request.user.profile
            instance.status = RELATIONSHIP_STATUS_FOLLOWING
            instance.save()

        else:
            instance.delete()

        return Response(data="success",status=status.HTTP_200_OK)

