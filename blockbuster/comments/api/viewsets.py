from comments.models import Comment
from rest_framework import viewsets
from comments.api.serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    refer to http://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
    """
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()