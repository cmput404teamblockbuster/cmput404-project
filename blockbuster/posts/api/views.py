import requests
from posts.api.serializers import PostSerializer
from posts.models import Post
from users.models import Profile
from posts.constants import PRIVACY_PUBLIC
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from nodes.models import Node


class custom(PageNumberPagination):
    page_size_query_param = 'size'
    page_query_param = 'page'


class ProfilePostsListView(APIView):
    """
    List all posts available to currently authenticated user. This is their "stream".
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, TokenAuthentication)

    def get(self, request):
        # http://www.django-rest-framework.org/tutorial/3-class-based-views/#rewriting-our-api-using-class-based-views
        user = request.user

        local_stream, foreign_friend_list = user.profile.get_local_stream_and_foreign_friend_list()
        all_posts = []
        if foreign_friend_list:
            for friend in foreign_friend_list:
                node = Node.objects.filter(host=friend.host)
                if node and node[0].is_allowed:
                    node = node[0]
                    api_url = '%sapi/author/%s/posts/' % (friend.host, friend.uuid) # TODO change this endpoint eventually to handle group api's
                    # We send a post request to the other server with the requesting users uuid so they know who is wanting info
                    data = dict(
                        requesting_user_uuid = str(self.request.user.profile.uuid)
                    )
                    response = requests.post(api_url, json=data, auth=(node.username_for_node, node.password_for_node))
                    result = response.json() if 199<response.status_code<300 else None
                    if not result:
                        return Response('%d Error: Could not communicate with server %s. (%s)' % (response.status_code, node.host, response.text), status=status.HTTP_400_BAD_REQUEST)
                    all_posts.extend(result.get('posts'))
                else:
                    return Response(status=status.HTTP_401_UNAUTHORIZED,
                                    data='You are not an accepted server on our system.')

        serializer = PostSerializer(local_stream, many=True)
        all_posts.extend(serializer.data)
        return Response(all_posts, status=status.HTTP_200_OK)


class ProfilePostDetailView(APIView):
    """
    Lists posts by the specified author that are visible to the requesting user.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, TokenAuthentication)

    def get(self, request, uuid):
        result = []
        author = Profile.objects.get(uuid=uuid)
        users_posts = Post.objects.filter(author=author).order_by('-created')  # get all posts by the specified user
        for post in users_posts:
            if post.privacy == PRIVACY_PUBLIC or request.user.id in post.viewable_to:  # check if the post is visible to logged in user
                result.append(post)

        mypaginator = custom()
        results = mypaginator.paginate_queryset(result, request)
        page = self.request.GET.get('page', 1)
        page_num = self.request.GET.get('size', 1000)
        serializer = PostSerializer(results,
                                    many=True)
        return Response(OrderedDict([('count', mypaginator.page.paginator.count),
                                     ('current', page),
                                     ('next', mypaginator.get_next_link()),
                                     ('previous', mypaginator.get_previous_link()),
                                     ('size', page_num),
                                     ('posts', serializer.data)])
                        )

    def post(self, request, uuid):
        """
        exact same as the get request except we return posts visible to the given uuid in the post body
        """
        result = []
        author = Profile.objects.get(uuid=uuid)
        users_posts = Post.objects.filter(author=author).order_by('-created')  # get all posts by the specified user
        for post in users_posts:
            if post.privacy == PRIVACY_PUBLIC or request.data.get('uuid') in post.viewable_to:  # check if the post is visible to logged in user
                result.append(post)

        mypaginator = custom()
        results = mypaginator.paginate_queryset(result, request)
        page = self.request.GET.get('page', 1)
        page_num = self.request.GET.get('size', 1000)
        serializer = PostSerializer(results,
                                    many=True)
        return Response(OrderedDict([('count', mypaginator.page.paginator.count),
                                     ('current', page),
                                     ('next', mypaginator.get_next_link()),
                                     ('previous', mypaginator.get_previous_link()),
                                     ('size', page_num),
                                     ('posts', serializer.data)])
                        )


class AllPublicPostsView(APIView):
    """
    This will get all public posts from all servers in our accepted nodes
    """
    def get(self, request):
        result = []
        # get posts from all nodes
        for node in Node.objects.all():
            if node.is_allowed:
                host = node.host
                url = host + 'api/posts/'
                try:
                    response = requests.get(url, auth=(node.username_for_node, node.password_for_node))
                except requests.ConnectionError:
                    continue

                if 199 < response.status_code < 300:
                    result.extend(response.json())
                else:
                    print "can not get public posts from node:", host

        # get all local public posts
        data = Post.objects.filter(privacy=PRIVACY_PUBLIC)
        serializer = PostSerializer(data, many=True)
        result.extend(serializer.data)

        return Response(status=status.HTTP_200_OK, data=result)