from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from users.api.serializers import UserSerializer
from users.models import Profile
from users.api.serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated


class RegisterUserView(APIView):
    """
    a POST will create a user in the BlockBuster system
    """
    def post(self, request):
        # From Cahlan Sharp http://stackoverflow.com/questions/16857450/how-to-register-users-in-django-rest-framework on March 11, 2017
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(
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

    def get(self, request):
        profile = Profile.objects.get(uuid=request.user.profile.uuid)
        serializer = ProfileSerializer(profile)
        return JsonResponse(serializer.data, safe=False)


class UserRelationshipCheckView(APIView):
    """
    Returns a boolean checking if two Users are friends
    """
    def get(self, request, uuid, uuid_2):
        user1 = Profile.objects.get(uuid=uuid)
        user2 = Profile.objects.get(uuid=uuid_2)
        if user2 in user1.friends:
            return Response(data={'friends': True}, status=status.HTTP_200_OK)
        else:
            return Response(data={'friends': False}, status=status.HTTP_200_OK)
