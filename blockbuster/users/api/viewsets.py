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
from django.contrib.sites.models import Site
from users.utils import determine_if_request_from_foundbook

site_name = Site.objects.get_current().domain

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
            for node in Node.objects.filter(is_allowed=True):
                response = self.request_foreign_profile_data(node, uuid)
                if response and response.status_code == 200:
                    profile = response.json()
                    return Response(status=status.HTTP_200_OK, data=profile)
            return Response(status=status.HTTP_404_NOT_FOUND, data='There are no profiles matching the given UUID')

        host = profile.host
        local = (host == site_name)
        if not local:
            # if host in ['http://warm-hollows-14698.herokuapp.com/', 'http://radiant-beyond-17792.herokuapp.com/']:
            #     host += 'api/'
            node = Node.objects.filter(host=host)
            if node and node[0].is_allowed:
                node = node[0]
                response = self.request_foreign_profile_data(node, uuid)

                if response and response.status_code == 200:
                    profile = response.json()
                    return Response(status=status.HTTP_200_OK, data=profile)
                return Response(status=status.HTTP_400_BAD_REQUEST, data='Could not contact server. Received response:%s'
                                                                         %(vars(response)))
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED, data='User is from an unaccepted server.')

        serializer = FullProfileSerializer(profile)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def list_local(self, *args, **kwargs):
        listofauthors = []
        local = Profile.objects.all()
        node = Node.objects.all()
        localserializer = FullProfileSerializer(local, many=True)
        listofauthors.extend(localserializer.data)
        return Response(status=status.HTTP_200_OK, data=listofauthors)

    def list(self, *args, **kwargs):
        listofauthors = []
        local = Profile.objects.all()
        localserializer = FullProfileSerializer(local, many=True)
        listofauthors.extend(localserializer.data)

        return Response(status=status.HTTP_200_OK, data=listofauthors)

    def request_foreign_profile_data(self, node, uuid):
        endpoint = 'author/'
        api_url = node.host + node.api_endpoint + endpoint + str(uuid) + '/'
        try:
            response = requests.get(api_url, auth=(node.username_for_node, node.password_for_node))
        except requests.ConnectionError:
            response = None

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
        try:
            requested_profile = Profile.objects.get(uuid=uuid)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data="No profile with the given UUID is found on this server.")

        friends = requested_profile.friends
        data = dict(
            query='friends',
            authors=list((friend.url for friend in friends))
        )
        return Response(data=data, status=status.HTTP_200_OK)

    def query(self, request, uuid):
        """
        this will check to see if any author uris in the given list is a friend with the requested author
        """
        try:
            requested_profile = Profile.objects.get(uuid=uuid)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data="No profile with the given UUID is found on this server.")

        authors_list = request.data.get('authors', None)
        result_friends_list = []
        if authors_list:
            for friend in requested_profile.friends:
                if friend.api_id in authors_list:
                    result_friends_list.append(friend.api_id)
            response_msg = dict(
                query='friends',
                author=requested_profile.api_id,
                authors=result_friends_list
            )
            return Response(status=status.HTTP_200_OK, data=response_msg)

        return Response(status=status.HTTP_400_BAD_REQUEST, data='no authors list given.')


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
        data = self.request.data
        foreign_user = None
        role = None
        must_create_profile = True
        local_initiator = False
        local_receiver = False
        from_foundbook = determine_if_request_from_foundbook(data)

        if from_foundbook: # set displayName for them!
            try:
                our_profile = Profile.objects.get(uuid=data.get('friend').get('id'))
                displayName = our_profile.username
                data.get('friend')['displayName'] = displayName
            except Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND, data="Profile with given UUID does not exist.")

        try:
            if from_foundbook:
                local_author = Profile.objects.get(uuid=data.get('author').get('id'))
            else:
                local_author = Profile.objects.get(username=data.get('author').get('displayName'))
            if local_author.host == site_name:
                local_initiator = True
            else:
                must_create_profile = False
                foreign_user = data.get('author')
        except Profile.DoesNotExist:
            foreign_user = data.get('author')
            role = 'author'

        try:
            if from_foundbook:
                local_friend = Profile.objects.get(uuid=data.get('friend').get('id'))
            else:
                local_friend = Profile.objects.get(username=data.get('friend').get('displayName'))
            if local_friend.host == site_name:
                local_receiver = True
            else:
                must_create_profile = False
                foreign_user = data.get('friend')
        except Profile.DoesNotExist:
            foreign_user = data.get('friend')
            role = 'friend'

        if not local_initiator or not local_receiver: # one of the users is from another server
            url_contents = urlparse(foreign_user.get('id')) # TODO this might not always be a url
            host = foreign_user.get('host', foreign_user.get('id')[:foreign_user.get('id').find(url_contents.path) + 1] if not from_foundbook else None)
            node = Node.objects.filter(host=host, is_allowed=True)
            if node:  # then we trust their server
                identifier = url_contents.path.split('/')[-1]
                if identifier == "":
                    identifier = url_contents.path.split('/')[-2]
                requesting_node = Node.objects.filter(user=self.request.user) # we want to know if node is requesting for an update
                if not requesting_node: # then a local user is requesting a friendship for a user on another server
                    node = node[0]
                    friend_request_url = '%s%sfriendrequest/' % (node.host, node.api_endpoint)
                    headers = {'Content-type': 'application/json'}
                    response = requests.post(friend_request_url, json=data, headers=headers, auth=(node.username_for_node, node.password_for_node))
                    print 'request sent to other server'
                    if response.status_code>=300:
                        return Response(status=response.status_code,
                                        data='Your request is rejected by %s' % host)

                if must_create_profile:
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
