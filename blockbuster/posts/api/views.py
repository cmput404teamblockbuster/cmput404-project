import requests
from posts.api.serializers import PostSerializer
from posts.models import Post
from users.models import Profile
from posts.constants import PRIVACY_PUBLIC, PRIVACY_UNLISTED, PRIVATE_TO_FOF
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from nodes.models import Node
from blockbuster import settings


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
                node = Node.objects.filter(host=friend.host, is_allowed=True)
                if node:
                    node = node[0]
                    api_url = '%s%sauthor/%s/posts/' % (friend.host, node.api_endpoint, friend.uuid)
                    # We send a post request to the other server with the requesting users uuid so they know who is wanting info
                    data = dict(
                        requesting_user_uuid=str(self.request.user.profile.uuid)
                    )
                    try:
                        response = requests.post(api_url, json=data, auth=(
                        node.username_for_node, node.password_for_node))  # TODO change this back to request.get
                    except requests.ConnectionError:
                        response = None
                    result = response.json() if response and 199 < response.status_code < 300 else None
                    if not result:
                        continue
                    all_posts.extend(result.get('posts'))
                else:
                    continue

        serializer = PostSerializer(local_stream, many=True)
        all_posts.extend(serializer.data)

        mypaginator = custom()
        results = mypaginator.paginate_queryset(local_stream, request)
        page = self.request.GET.get('page', 1)
        page_num = self.request.GET.get('size', 1000)

        #sort the posts
        if len(all_posts) > 1:
            all_posts.sort(key=lambda k: k['published'], reverse=True)
        #sort the comments
        for post in all_posts:
            if len(post['comments']) > 1:
                post['comments'].sort(key=lambda k: k['published'], reverse=True)

        return Response(OrderedDict([('count', mypaginator.page.paginator.count),
                                     ('current', page),
                                     ('next', mypaginator.get_next_link()),
                                     ('previous', mypaginator.get_previous_link()),
                                     ('size', page_num),
                                     ('posts', all_posts)]), status=status.HTTP_200_OK
                        )


class ProfilePostDetailView(APIView):
    """
    Lists posts by the specified author that are visible to the requesting user.
    TODO i think here we want ot return all posts by the specified author, except for server_only posts, if the request is foreign (check SITE_URL)
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
            elif post.privacy == PRIVATE_TO_FOF:
                if post.viewable_to_FOF(author):
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

    # TODO likely remove this post
    def post(self, request, uuid):
        """
        exact same as the get request except we return posts visible to the given uuid in the post body
        """
        result = []
        try:
            author = Profile.objects.get(uuid=uuid)
            if author.host != settings.SITE_URL: # if this is a foreign user
                raise Profile.DoesNotExist
        except Profile.DoesNotExist:
            for node in Node.objects.all():
                api_url = '%sauthor/%s/posts/' % (node.host, uuid)
                try:
                    data = dict(requesting_user_uuid=request.data.get('requesting_user_uuid')) # TODO change from post to get
                    response = requests.post(api_url, json=data, auth=(node.username_for_node, node.password_for_node))
                except requests.ConnectionError:
                    continue
                if 199 < response.status_code < 300:
                    return Response(data=response.json())
                print response.text
                continue
        users_posts = Post.objects.filter(author=author).order_by('-created').exclude(privacy=PRIVACY_UNLISTED)  # get all posts by the specified user
        for post in users_posts:
            if post.privacy == PRIVACY_PUBLIC or request.data.get('requesting_user_uuid') in post.viewable_to:  # check if the post is visible to logged in user
                result.append(post)

            elif post.privacy == PRIVATE_TO_FOF:
                if post.viewable_to_FOF(author):
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
    authentication_classes = (BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        result = []
        # get posts from all nodes
        for node in Node.objects.filter(is_allowed=True):
            host = node.host
            url = host + node.api_endpoint + 'posts/'
            try:
                response = requests.get(url, auth=(node.username_for_node, node.password_for_node))
            except requests.ConnectionError:
                continue

            # Check for successful response
            if 199 < response.status_code < 300:
                try:
                    result.extend(response.json().get('posts'))
                except AttributeError:
                    result.extend(response.json())
            else:
                print response.status_code,"can not get public posts from node:", host, "with url:", url

        # get all local public posts
        data = Post.objects.filter(privacy=PRIVACY_PUBLIC)
        serializer = PostSerializer(data, many=True)
        result.extend(serializer.data)

        #sort the posts
        if len(result) > 1:
            result.sort(key=lambda k: k['published'], reverse=True)
        #sort the comments
        for post in result:
            if len(post['comments']) > 1:
                post['comments'].sort(key=lambda k: k['published'], reverse=True)

        return Response(status=status.HTTP_200_OK, data=result)