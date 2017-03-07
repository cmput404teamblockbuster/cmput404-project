from rest_framework import viewsets
from posts.api.serializers import PostSerializer
from posts.models import Post


class AuthorBasedPostsViewSet(viewsets.ModelViewSet):
    """
    refer to http://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()