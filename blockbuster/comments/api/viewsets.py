from comments.models import Comment
from rest_framework import viewsets, status
from comments.api.serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from posts.models import Post


class CommentViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    View the comments for the specified post.

    create:
    Add a comment to the specified post.
    """
    # http://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, uuid):
        data = request.data
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            post = Post.objects.get(uuid=uuid)  # Get the post the comment is for
            author = request.user.profile
            if not post.viewable_for_author(author):
                status_code = status.HTTP_403_FORBIDDEN
                response_msg = dict(
                    success=False,
                    message='Comment not allowed'
                )
            else:
                Comment.objects.create(
                    author=author,
                    body=serializer.data['body'],
                    post=post,
                )
                status_code = status.HTTP_201_CREATED
                response_msg = dict(
                    success=True,
                    message='Comment Added'
                )

            return Response(status=status_code, data=response_msg)

        else:  # If there is a validation error then return it
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
