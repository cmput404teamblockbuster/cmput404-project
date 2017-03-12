from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from users.api.serializers import UserSerializer


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
