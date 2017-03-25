from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from users.api.serializers import UserSerializer, UserRelationshipSerializer
from users.models import Profile, UserRelationship
from users.api.serializers import ProfileSerializer
from users.constants import RELATIONSHIP_STATUS_TYPES, RELATIONSHIP_STATUS_PENDING, RELATIONSHIP_STATUS_FRIENDS, RELATIONSHIP_STATUS_FOLLOWING
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict

class custom(PageNumberPagination):
    page_size_query_param = 'size'
    page_query_param = 'page'

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
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthenticatedUserRelationshipView(APIView):
    """
    returns the UserRelationship object with the current user and a specified user
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, uuid):
        auth_user = request.user.profile
        if str(auth_user.uuid) == uuid:
            return Response(data='The profile with the given UUID is your own.', status=status.HTTP_200_OK)
        other_user = Profile.objects.get(uuid=uuid)
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

class UserFriendsListView(APIView):
    """
    returns a list of users that are friends with a specified user
    """
    #http://stackoverflow.com/questions/14190140/merge-querysets-in-django
    def get(self, request,uuid):
        friend_uuids = []
        for r in UserRelationship.objects.select_related('initiator__uuid').filter(receiver__uuid=uuid,
                                                                                 status=RELATIONSHIP_STATUS_FRIENDS):
            friend_uuids.append(r.initiator.uuid)
        for r in UserRelationship.objects.select_related('receiver__uuid').filter(initiator__uuid=uuid,
                                                                                status=RELATIONSHIP_STATUS_FRIENDS):
            friend_uuids.append(r.receiver.uuid)
        
        allmyfriends = Profile.objects.filter(uuid__in=friend_uuids)
        serializer = ProfileSerializer(allmyfriends,many=True)
        
     


        
        mypaginator = custom()
        results = mypaginator.paginate_queryset(allmyfriends, request)


        page = self.request.GET.get('page', 1)
        page_num = self.request.GET.get('size', 1000)


        serializer = ProfileSerializer(results, many=True)  # TODO maybe a different serilizer for validating that permissions are met

        return Response(OrderedDict([('count', mypaginator.page.paginator.count),
                                     ('current', page),
                                     ('next', mypaginator.get_next_link()),
                                     ('previous', mypaginator.get_previous_link()),
                                     ('size', page_num),
                                     ('posts', serializer.data)]), status=status.HTTP_200_OK)

            #return JsonResponse(serializer.data)

    

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
