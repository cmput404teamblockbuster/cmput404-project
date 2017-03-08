from rest_framework import viewsets
from posts.api.serializers import PostSerializer
from posts.models import Post
from comments.models import Comment
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from comments.api.serializers import CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    refer to http://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        """
        if no specific post object is specified in the url params, then all public posts will be returned
        """
        return Post.objects.filter(is_public=True)

    @detail_route() # TODO add post functionality here based off http://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing
    def comments(self, request, pk=None):
        post_comments = Comment.objects.filter(post=pk).order_by('-created')  # get all comments for a specific post
        # page = self.paginate_queryset(posts)
        # if page is not None:
        # serializer = PostSerializer(users_posts, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = CommentSerializer(post_comments, many=True)
        return Response(serializer.data)



class AuthenticatedAuthorPostViewSet(viewsets.ModelViewSet):
    """
    viewset for the currently logged in users posts. Accessed via api/author/posts
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
