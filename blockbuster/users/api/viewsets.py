from rest_framework import viewsets
from users.api.serializers import AuthorSerializer
from rest_framework.response import Response
from users.models import UserProfile
from rest_framework.decorators import list_route, detail_route
from posts.models import Post
from posts.api.serializers import PostSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """
    refer to http://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
    """
    serializer_class = AuthorSerializer
    queryset = UserProfile.objects.all()


    # http://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing
    @list_route()
    def posts(self, request):
        user_profile = UserProfile.objects.get(user=self.request.user)
        users_posts = Post.objects.filter(author=user_profile).order_by('-created') # get all posts by logged in user
        # page = self.paginate_queryset(posts)
        # if page is not None:
        # serializer = PostSerializer(users_posts, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(users_posts, many=True)
        return Response(serializer.data)

    @detail_route()
    def posts(self, request, pk=None):
        # TODO check if user exists based off pk to return error
        author = pk
        if author is None:
            print 'got here'
            author = UserProfile.objects.get(user=self.request.user).id
        users_posts = Post.objects.filter(author=author).order_by('-created')  # get all posts by logged in user
        # page = self.paginate_queryset(posts)
        # if page is not None:
        # serializer = PostSerializer(users_posts, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(users_posts, many=True)
        return Response(serializer.data)