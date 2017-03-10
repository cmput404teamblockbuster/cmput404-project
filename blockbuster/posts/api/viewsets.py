from rest_framework import viewsets
from posts.api.serializers import PostSerializer
from posts.models import Post
from comments.models import Comment
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from comments.api.serializers import CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    refer to:
    http://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
    http://www.django-rest-framework.org/api-guide/routers/#simplerouter
    """
    lookup_field = 'uuid'
    lookup_value_regex = '[^/]+'
    # lookup_value_regex = '[0-9a-f]{32}'
    serializer_class = PostSerializer
    model = Post

    # def create(self, *args, **kwargs):
    #     # Use 'invite' instead
    #     print self.request.data
    #     # raise MethodNotAllowed('POST')

    def get_queryset(self):
        """
        if no specific post object is specified in the url params, then all public posts will be returned
        """
        return Post.objects.filter(is_public=True)

    @detail_route() # TODO add POST functionality here based off http://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing
    def comments(self, request, pk=None):
        post = Post.object.get(uuid=pk)
        post_comments = Comment.objects.filter(post=post.id).order_by('-created')  # get all comments for a specific post

        # TODO implement pagination something like below
        # page = self.paginate_queryset(posts)
        # if page is not None:
        # serializer = PostSerializer(users_posts, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = CommentSerializer(post_comments, many=True)
        return Response(serializer.data)

