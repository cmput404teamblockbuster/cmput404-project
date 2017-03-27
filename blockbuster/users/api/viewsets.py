import json
import requests
import uuid
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from users.models import Profile, UserRelationship
from users.api.serializers import FullProfileSerializer, UserRelationshipSerializer, CondensedProfileSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.constants import RELATIONSHIP_STATUS_PENDING, RELATIONSHIP_STATUS_FRIENDS, RELATIONSHIP_STATUS_FOLLOWING
from urlparse import urlparse
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from nodes.models import Node

from blockbuster import settings


class ProfileViewSet(viewsets.ModelViewSet):
    """
    refer to http://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
    """
    lookup_field = 'uuid'
    lookup_value_regex = '[^/]+'
    serializer_class = FullProfileSerializer
    queryset = Profile.objects.all()
    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def retrieve(self, *args, **kwargs):
        uuid =  kwargs.get('uuid')
        profile = None
        try:
            profile = Profile.objects.get(uuid=uuid)
        except Profile.DoesNotExist:

            for node in Node.objects.all():
                if node.is_allowed:
                    print("dhjkshdkjsahkhkfa line 38")
                    response = self.request_foreign_profile_data(node, uuid)
                    if response.status_code == 200:
                        profile = response.json()
                        return Response(status=status.HTTP_200_OK, data=profile)
            return Response(status=status.HTTP_404_NOT_FOUND, data='Profile with this uuid does not exist.')

        host = profile.host
        local = (host == settings.SITE_URL)
        if not local:

            node = Node.objects.filter(host=host)
            if node and node[0].is_allowed:
                node = node[0]
                response = self.request_foreign_profile_data(node, uuid)
                if response.status_code == 200:
                    profile = response.json()
                    return Response(status=status.HTTP_200_OK, data=profile)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED, data='User is from an unaccepted server.')

        serializer = ProfileSerializer(profile)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def list(self, *args, **kwargs):
        listofauthors = []
        local = Profile.objects.all()
        node = Node.objects.all()
        localserializer = ProfileSerializer(local, many=True)
        listofauthors.extend(localserializer.data)
        for singlenode in node:
            if singlenode.is_allowed == True:
                endpoint = 'api/author/all/'
                api_url = singlenode.host + endpoint
                try:
                    response = requests.get(api_url, auth=(singlenode.username_for_node, singlenode.password_for_node))
                except requests.ConnectionError:
                    continue
                if response.status_code == 200:
                    payload = response.json()
                    if len(payload) > 0:
                        listofauthors.extend(payload)


        return Response(status=status.HTTP_200_OK, data=listofauthors)

    def request_foreign_profile_data(self, node, uuid):
        endpoint = 'api/author/'
        api_url = node.host + endpoint + str(uuid) + '/'
        response = requests.get(api_url, auth=(node.username_for_node, node.password_for_node))
        return response


class MyFriendsProfilesViewSet(viewsets.ModelViewSet):
    """
    returns the authenticated users friends list
    """
    serializer_class = CondensedProfileSerializer
    authentication_classes = (BasicAuthentication, TokenAuthentication)
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
    authentication_classes = (BasicAuthentication, TokenAuthentication)
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
    authentication_classes = (BasicAuthentication, TokenAuthentication)
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
        """
        TODO implement node friending as follows
        if requester is from another site then we parse the requestors host and see if they exist in our db
            if they do we create a profile of the requestor and set their uuid to ours
            if they dont then we raise a authentication error
        if requester is local and person friending is foregin:
            confirm the foreign person is in our accepted node host
            make an api call to their friendrequest api
        if local we do this as normal.
        """
        data = self.request.data
        foreign_user = None
        role = None
        try:
            local_author = Profile.objects.get(username=data.get('author').get('displayName'))
            local_initiator = True
        except Profile.DoesNotExist:
            local_initiator = False
            foreign_user = data.get('author')
            role = 'author'

        try:
            local_receiver = Profile.objects.get(username=data.get('friend').get('displayName'))
            local_receiver = True
        except Profile.DoesNotExist:
            local_receiver = False
            foreign_user = data.get('friend')
            role = 'friend'

        if not local_initiator or not local_receiver: # one of the users is from another server
            url_contents = urlparse(foreign_user.get('id'))
            host = foreign_user.get('host', foreign_user.get('id')[:foreign_user.get('id').find(url_contents.path) + 1])
            node = Node.objects.filter(host=host)
            if node:  # then we trust their server
                identifier = url_contents.path.split('/')[-1]
                if not local_receiver: # then a local user is requesting a friendship for a user on another server
                    node = node[0]
                    friend_request_url = '%sapi/friendrequest/' % node.host
                    headers = {'Content-type': 'application/json'}
                    response = requests.post(friend_request_url, json=data, headers=headers, auth=(node.username_for_node, node.password_for_node))
                    print 'request sent to other server'

                new_profile = Profile.objects.create(uuid=uuid.UUID(identifier).hex, username=foreign_user.get('displayName'),
                                                     host=host)  # WARNING we will get errors because url will be our api endpoints
                data[role] = CondensedProfileSerializer(new_profile).data
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED,
                                data='You are not an accepted server on our system.')

        if not data.get('status', None):
            data['status'] = RELATIONSHIP_STATUS_PENDING
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
        else:  # otherwise the user shouldn't have access to this object
            return Response(data='You do not have access to this friendship.', status=status.HTTP_403_FORBIDDEN)

        if instance.status == RELATIONSHIP_STATUS_FRIENDS:
            # If friends then we change to following so other user can still see posts
            instance.initiator = other_user_in_relationship
            instance.receiver = self.request.user.profile
            instance.status = RELATIONSHIP_STATUS_FOLLOWING
            instance.save()

        else:
            instance.delete()

        return Response(data="success", status=status.HTTP_200_OK)
