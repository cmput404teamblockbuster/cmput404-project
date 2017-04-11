from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.api.serializers import UserSerializer, UserRelationshipSerializer
from users.models import Profile, UserRelationship, NewUser
from users.api.serializers import ProfileSerializer, CondensedProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from users.constants import RELATIONSHIP_STATUS_FOLLOWING, RELATIONSHIP_STATUS_PENDING
from django.contrib.sites.models import Site
from users.utils import verify_friends

class RegisterUserView(APIView):
    """
    a POST will create a user in the BlockBuster system
    """
    def post(self, request):
        # From Cahlan Sharp http://stackoverflow.com/questions/16857450/how-to-register-users-in-django-rest-framework on March 11, 2017
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            NewUser.objects.create(
                email=serializer.data['email'],
                username=serializer.data['username'],
                password=serializer.data['password']
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthenticatedUserProfileView(APIView):
    """
    Returns the currently authenticated users profile information
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, TokenAuthentication)

    def get(self, request):
        profile = Profile.objects.get(uuid=request.user.profile.uuid)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthenticatedUserRelationshipView(APIView):
    """
    returns the UserRelationship object with the current user and a specified user
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, TokenAuthentication)

    def get(self, request, uuid):
        auth_user = request.user.profile
        if str(auth_user.uuid) == uuid:
            return Response(data='The profile with the given UUID is your own.', status=status.HTTP_200_OK)
        try:
            other_user = Profile.objects.get(uuid=uuid)
        except Profile.DoesNotExist:
            return Response(data='No Relationship Found.', status=status.HTTP_200_OK)

        site_name = Site.objects.get_current().domain
        for friend in auth_user.friends:
            if (friend.host != site_name):
                verify_friends(friend, self.request.user.profile)

        qs1 = UserRelationship.objects.filter(initiator=auth_user, receiver=other_user)
        qs2 = UserRelationship.objects.filter(initiator=other_user, receiver=auth_user)
        result = qs1 | qs2
        if result:
            serializer = UserRelationshipSerializer(result[0])
            if serializer.is_valid:
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors)
        else:
            return Response(data='No Relationship Found.', status=status.HTTP_200_OK)


class AuthenticatedUserFollowingListView(APIView):
    """
    returns a list of all the people the authenticated user is following but they arent friends
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, TokenAuthentication)

    def get(self, request):
        auth_user = request.user.profile
        result = UserRelationship.objects.filter(initiator=auth_user, status__in=[RELATIONSHIP_STATUS_FOLLOWING, RELATIONSHIP_STATUS_PENDING])
        if result:
            serializer = CondensedProfileSerializer((r.receiver for r in result), many=True)
            if serializer.is_valid:
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors)
        else:
            return Response(data='Not following any users.', status=status.HTTP_200_OK)


class AuthenticatedUserFollowersListView(APIView):
    """
    returns a list of all the authenticated user's followers
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, TokenAuthentication)

    def get(self, request):
        auth_user = request.user.profile
        result = UserRelationship.objects.filter(receiver=auth_user, status__in=[RELATIONSHIP_STATUS_FOLLOWING, RELATIONSHIP_STATUS_PENDING])
        if result:
            serializer = CondensedProfileSerializer((r.initiator for r in result), many=True)
            if serializer.is_valid:
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors)
        else:
            return Response(data='User has no followers.', status=status.HTTP_200_OK)


class UserRelationshipCheckView(APIView):
    """
    Returns a boolean checking if two Users are friends
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, TokenAuthentication)

    def get(self, request, uuid, uuid_2):
        user1 = Profile.objects.get(uuid=uuid)
        user2 = Profile.objects.get(uuid=uuid_2)

        if user2 in user1.friends:
            return Response(data={'query':'friends', 'authors': [user1.api_id, user2.api_id], 'friends': True}, status=status.HTTP_200_OK)
        else:
            return Response(data={'query':'friends', 'authors': [user1.api_id, user2.api_id], 'friends': False}, status=status.HTTP_200_OK)
