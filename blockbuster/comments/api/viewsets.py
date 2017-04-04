import requests
import uuid
from comments.models import Comment
from rest_framework import viewsets, status
from comments.api.serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from posts.models import Post
from users.models import Profile
from nodes.models import Node
from rest_framwork.pagination import PageNumberPagination

class custom(PageNumberPagination):
    page_size_query_param = 'size'
    page_query_param = 'page'
    def get_paginated_response(self,data):
        return Response(OrderedDict([('count', self.page.paginator.count),
                                     ('current', page),
                                     ('next', self.get_next_link()),
                                     ('previous', self.get_previous_link()),
                                     ('size', page_num),
                                     ('posts', data)])
                        )
        

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
    authentication_classes = (BasicAuthentication, TokenAuthentication)
    pagination_class = custom

    def create(self, request, uuid_input):
        data = request.data
        our_data = request.data.get('comment')
        serializer = CommentSerializer(data=our_data)
        host = data.get('host')
        if host in ['http://blockbuster.canadacentral.cloudapp.azure.com']:
            # host += "api/"
            data = our_data

        if serializer.is_valid():
            try:
                post = Post.objects.get(uuid=uuid_input)  # Get the post the comment is for
            except Post.DoesNotExist:
                node = Node.objects.filter(host=host, is_allowed=True)
                if node:
                    node = node[0]
                    api_url = host + node.api_endpoint + 'posts/' + uuid_input + '/comments/'
                    print(data)
                    response = requests.post(api_url, json=data, auth=(node.username_for_node, node.password_for_node))
                    if 199 < response.status_code < 300:
                        comment = response.json()
                        return Response(status=status.HTTP_200_OK, data=comment)

                    return Response(status=status.HTTP_400_BAD_REQUEST, data=response)
                else:
                    msg = {
                        "query": "addComment",
                        "success": False,
                        "message": "Comment not allowed"
                    }
                    return Response(status=status.HTTP_403_FORBIDDEN, data=msg)

            try:
                identifier = data.get('author').get('id').split('/')[-1]
                profile = Profile.objects.get(uuid=identifier)
            except Profile.DoesNotExist:
                author = data.get('author')
                profile = Profile.objects.create(uuid=uuid.UUID(identifier).hex, username=author.get('displayName'),
                                                 host=author.get('host'))

            Comment.objects.create(
                author=profile,
                body=serializer.data['comment'],
                post=post,
            )
            status_code = status.HTTP_201_CREATED
            response_msg = dict(
                query='addComent',
                success=True,
                message='Comment Added'
            )

            return Response(status=status_code, data=response_msg)

        else:  # If there is a validation error then return it
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
