from rest_framework import viewsets, status
from posts.api.serializers import PostSerializer
from posts.models import Post
from nodes.models import Node
import requests
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from posts.constants import PRIVACY_PUBLIC, PRIVACY_UNLISTED
from rest_framework.authentication import BasicAuthentication, TokenAuthentication



class PostViewSet(viewsets.ModelViewSet):
    """
    list:
    Lists all public posts

    create:
    Create a post

    retrieve:
    Display a specific post in the system. It must be visible to the authenticated user.

    update:
    Update a specific post that you have created.

    destroy:
    Delete a specific post that you have created.
    """
    #
    # refer to:
    # http://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
    # http://www.django-rest-framework.org/api-guide/routers/#simplerouter
    #
    # Permissions:
    # http://www.django-rest-framework.org/api-guide/permissions/#api-reference

    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (BasicAuthentication, TokenAuthentication)
    lookup_field = 'uuid'
    lookup_value_regex = '[^/]+'
    serializer_class = PostSerializer
    model = Post
    queryset = Post.objects.all()

    def create(self, *args, **kwargs):
        data = self.request.data
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def list(self, *args, **kwargs):
        """
        all public posts will be returned for the current server
        """
        data = Post.objects.filter(privacy=PRIVACY_PUBLIC)
        serializer = PostSerializer(data, many=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def retrieve(self, *args, **kwargs):
        """
        Given a valid uuid, it will display the post to the user as long as it is viewable to them.
        """
        user = self.request.user
        post = Post.objects.get(uuid=kwargs.get('uuid'))
        if post.privacy == PRIVACY_PUBLIC or post.privacy == PRIVACY_UNLISTED:
            serializer = PostSerializer(post)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        if not user.is_anonymous():
            if post.viewable_for_author(user.profile):
                serializer = PostSerializer(post)
                return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response('You do not have permission to see this post.', status=status.HTTP_403_FORBIDDEN)

