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
    # @list_route() TODO this would make api/author/posts return the logged in users posts, but since this endpoint method is the same name as the @detail_route() below, it wont work.
    # def posts(self, request):
    #     user_profile = UserProfile.objects.get(user=self.request.user)
    #     users_posts = Post.objects.filter(author=user_profile).order_by('-created') # get all posts by logged in user
    #     # page = self.paginate_queryset(posts)
    #     # if page is not None:
    #     # serializer = PostSerializer(users_posts, many=True)
    #     #     return self.get_paginated_response(serializer.data)
    #
    #     serializer = PostSerializer(users_posts, many=True)
    #     return Response(serializer.data)

    @detail_route()
    def posts(self, request, pk=None):
        """
        display posts by the specified author that are visible to the logged in user

        """
        result = []
        from pprint import pprint
        pprint(vars(request))
        users_posts = Post.objects.filter(author=pk).order_by('-created')  # get all posts by the specified user
        for post in users_posts:
            if post.is_public or request.user.id in post.viewable_to: # check if the post is visible to logged in user
                result.append(post)

        #  TODO implement pagination here

        serializer = PostSerializer(result, many=True) # TODO maybe a different serilizer for validating that permissions are met
        return Response(serializer.data)
