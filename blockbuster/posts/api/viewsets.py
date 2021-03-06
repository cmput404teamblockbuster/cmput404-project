from collections import OrderedDict
from rest_framework import viewsets, status
from posts.api.serializers import PostSerializer
from posts.models import Post
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from posts.constants import PRIVACY_PUBLIC, PRIVACY_UNLISTED, PRIVACY_PRIVATE, PRIVACY_SERVER_ONLY, png, jpeg
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from users.models import Profile
from nodes.models import Node


class custom(PageNumberPagination):
    page_size_query_param = 'size'
    page_query_param = 'page'
    def get_paginated_response(self,data):
        return Response(OrderedDict([('query', 'comments'),
                                     ('count', self.page.paginator.count),
                                     ('current', self.page_query_param),
                                     ('next', self.get_next_link()),
                                     ('previous', self.get_previous_link()),
                                     ('size', self.page_size_query_param),
                                     ('comments', data)])
                        )


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

    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, TokenAuthentication)
    pagination_class = custom
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
            # manually add visibileTo field
            # WARNING - we can only handle one visibility to one person!
            if serializer.data.get('visibility') == PRIVACY_PRIVATE:
                identifier = data.get('visibleTo')[0].split('/')[-1]
                if len(identifier) <= 1:
                    identifier = data.get('visibleTo')[0].split('/')[-2]
                profile = Profile.objects.get(uuid=(identifier))
                post = Post.objects.filter(content=serializer.data.get('content')).order_by('-created')
                post[0].private_to.add(profile)
                post[0].save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def list(self, *args, **kwargs):
        """
        all public posts will be returned for the current server
        """

        if Node.objects.filter(user=self.request.user):
            if Node.objects.filter(user=self.request.user, is_allowed=True):  # remote user and allowed
                data = Post.objects.filter(privacy=PRIVACY_PUBLIC)
                if Node.objects.filter(user=self.request.user, is_allowed=True, share_image=False): # remote user, allowed but no picture.
                    data = data.exclude(contentType=png).exclude(contentType=jpeg)
            else: # remote user, not allowed
                data = Post.objects.none() # return empty data if the node is not allowed
        else: # local user
            data = Post.objects.filter(privacy=PRIVACY_PUBLIC)\

        mypaginator = custom()
        results = mypaginator.paginate_queryset(data, self.request)
        serializer = PostSerializer(results, many=True)

        page = self.request.GET.get('page', 1)
        page_num = self.request.GET.get('size', 1000)
        print serializer.data, "nere"
        return Response(OrderedDict([('query', 'posts'),
                                     ('count', mypaginator.page.paginator.count),
                                     ('current', page),
                                     ('next', mypaginator.get_next_link()),
                                     ('previous', mypaginator.get_previous_link()),
                                     ('size', page_num),
                                     ('posts', serializer.data)]), status=status.HTTP_200_OK
                        )

    def retrieve(self, *args, **kwargs):
        """
        Given a valid uuid, it will display the post to the user as long as it is viewable to them.
        """
        user = self.request.user
        post = Post.objects.get(uuid=kwargs.get('uuid'))

        # return 403 if a node is requiring
        if Node.objects.filter(user=user, is_allowed=False):
            return Response('You do not have permission to see this post.', status=status.HTTP_403_FORBIDDEN)
        if Node.objects.filter(user=user, is_allowed=True,share_image=False) and post.contentType in [jpeg,png]:
            return Response('You do not have permission to see this post.', status=status.HTTP_403_FORBIDDEN)

        if post.privacy == PRIVACY_PUBLIC or post.privacy == PRIVACY_UNLISTED:
            serializer = PostSerializer(post)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        if not user.is_anonymous():
            serializer = PostSerializer(post)
            try:
                if post.viewable_for_author(user.profile):
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
            except Profile.DoesNotExist: # Then its a node requesting it
                if post.privacy != PRIVACY_SERVER_ONLY:
                    if Node.objects.get(host=user.node.host, is_allowed=True):
                        return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response('You do not have permission to see this post.', status=status.HTTP_403_FORBIDDEN)
