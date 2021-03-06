import requests
from posts.api.serializers import PostSerializer
from posts.models import Post
from users.models import Profile
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from nodes.models import Node
from posts.constants import PRIVACY_TYPES, PRIVATE_TO_ALL_FRIENDS, PRIVACY_PRIVATE, PRIVACY_PRIVATE, PRIVACY_PUBLIC, \
    PRIVATE_TO_FOAF, PRIVACY_UNLISTED,PRIVACY_SERVER_ONLY,contentchoices,text_markdown,text_plain,binary,png,jpeg
from django.contrib.sites.models import Site
from posts.utils import foreign_post_viewable_for_author, get_foreign_posts_by_author, sort_posts
from dateutil import parser

site_name = Site.objects.get_current().domain

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
        try:
            foreign_request = False
            host = request.user.node.host
            for node in Node.objects.filter(is_allowed=True):
                if host in node.host:
                    foreign_request = True
            if not foreign_request:
                return Response(status=status.HTTP_401_UNAUTHORIZED, data='Request is from an unaccepted server.')
        except Node.DoesNotExist:
            foreign_request = False

        all_posts = []
        if foreign_request:
            posts = Post.objects.all().exclude(privacy=PRIVACY_SERVER_ONLY)
            serializer = PostSerializer(posts, many=True, context={'request': request})

        else: # local user making request
            user = request.user
            local_stream, foreign_friend_list = user.profile.get_local_stream_and_foreign_friend_list()
            if foreign_friend_list:
                for friend in foreign_friend_list:
                    node = Node.objects.filter(host=friend.host, is_allowed=True)
                    if node:
                        node = node[0]
                        api_url = '%s%sauthor/%s/posts/' % (friend.host, node.api_endpoint, friend.uuid)
                        try:
                            response = requests.get(api_url, auth=(node.username_for_node, node.password_for_node))
                        except requests.ConnectionError:
                            response = None
                        result = response.json() if response and 199 < response.status_code < 300 else None
                        if not result:
                            continue

                        # Filter on our own end
                        for post in result.get('posts'):
                            if foreign_post_viewable_for_author(post, request.user.profile):
                                all_posts.append(post)
                    else:
                        continue

            serializer = PostSerializer(local_stream, many=True, context={'request': request} )
        all_posts.extend(serializer.data)

        mypaginator = custom()
        results = mypaginator.paginate_queryset(all_posts, request)
        page = self.request.GET.get('page', 1)
        page_num = self.request.GET.get('size', 1000)

        #sort the posts/comments
        if len(all_posts) > 1:
            sort_posts(all_posts)

        return Response(OrderedDict([('query', 'posts'),
                                     ('count', mypaginator.page.paginator.count),
                                     ('current', page),
                                     ('next', mypaginator.get_next_link()),
                                     ('previous', mypaginator.get_previous_link()),
                                     ('size', page_num),
                                     ('posts', all_posts)]), status=status.HTTP_200_OK
                        )


class ProfilePostDetailView(APIView):
    """
    Lists posts by the specified author that are visible to the requesting user.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication, TokenAuthentication)

    def get(self, request, uuid):
        result = []
        foreign_request = False
        request_host = request.get_host() #TODO: note this get_host() is giving back our own host, not the requesting user's host???
        # see: https://docs.python.org/3.3/library/urllib.request.html
        for node in Node.objects.filter(is_allowed=True):
            if request_host in node.host:  # check if a server is making the request, could be bypassed if we do not hold a record of the server
                foreign_request = True

        # this will also make sure that team8's host is filtered out
        if Node.objects.filter(user=request.user, is_allowed=True): # temp side check for if node. might need to be more secure?
            print "get to /author/id/posts by node:", request.user
            foreign_request = True
        elif Node.objects.filter(user=request.user, is_allowed=False):
            return Response(data="You are not allowed on our server.", status=status.HTTP_401_UNAUTHORIZED)

        foreign_profile = False
        try:
            author = Profile.objects.get(uuid=uuid)
            if site_name != author.host:
                foreign_profile = True # Then the uuid given is for a remote author
        except Profile.DoesNotExist:
            if foreign_request:
                return Response(status=status.HTTP_404_NOT_FOUND,
                                data="No profile with the given UUID is found on this server.")
            foreign_profile = True # Then the uuid given is for a remote author

        if foreign_request:
            if Node.objects.filter(user=request.user, share_image=False):
                result = Post.objects.filter(author=author).exclude(privacy=PRIVACY_SERVER_ONLY).exclude(contentType=png).exclude(contentType=jpeg)
            else:
                result = Post.objects.filter(author=author).exclude(privacy=PRIVACY_SERVER_ONLY) # send them all posts that are NOT server only

        elif foreign_profile:
            response = get_foreign_posts_by_author(uuid)
            if not response:
                return Response(data="Could not find a host with such a UUID profile", status=status.HTTP_404_NOT_FOUND)
            for post in response:
                if foreign_post_viewable_for_author(post, self.request.user.profile) or post.get('visibility') in ['PUBLIC']:
                    result.append(post)

            return Response(data=dict(posts=result), status=status.HTTP_200_OK)

        else: # a local user is requesting posts from a local author
            users_posts = Post.objects.filter(author=author).order_by('-created')  # get all posts by the specified user
            for post in users_posts:
                if post.privacy == PRIVACY_PUBLIC or post.viewable_for_author(request.user.profile):  # check if the post is visible to logged in user
                    result.append(post)

        mypaginator = custom()
        results = mypaginator.paginate_queryset(result, request)
        page = self.request.GET.get('page', 1)
        page_num = self.request.GET.get('size', 1000)
        serializer = PostSerializer(results,
                                    many=True, context={'request': request} )

        #sort the posts/comments
        sort_posts(serializer.data)

        return Response(OrderedDict([('query', 'posts'),
                                     ('count', mypaginator.page.paginator.count),
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
                    # assume everyone is following example-article.json
                    continue
            else:
                print response.status_code,"can not get public posts from node:", host, "with url:", url,response.text

        # get all local public posts
        data = Post.objects.filter(privacy=PRIVACY_PUBLIC)
        serializer = PostSerializer(data, many=True, context={'request': request})
        result.extend(serializer.data)

        #sort the posts/comments
        sort_posts(result)

        return Response(status=status.HTTP_200_OK, data=result)
