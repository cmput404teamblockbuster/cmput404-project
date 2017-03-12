from rest_framework import viewsets, status
from posts.api.serializers import PostSerializer
from posts.models import Post
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from posts.constants import PRIVACY_PUBLIC


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
    lookup_field = 'uuid'
    lookup_value_regex = '[^/]+'
    # lookup_value_regex = '[0-9a-f]{32}'
    serializer_class = PostSerializer
    model = Post

    def create(self, *args, **kwargs):
        # data = JSONParser().parse(self.request)
        data = self.request.data
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def get_queryset(self):
        """
        if no specific post object is specified in the url params, then all public posts will be returned
        """
        return Post.objects.filter(privacy=PRIVACY_PUBLIC)

