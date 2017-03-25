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


class custom(PageNumberPagination):
    page_size_query_param = 'size'
    page_query_param = 'page'


class ProfilePostsListView(APIView):
    """
    List all posts available to currently authenticated user. This is their "stream".
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):


        # http://www.django-rest-framework.org/tutorial/3-class-based-views/#rewriting-our-api-using-class-based-views
        user = request.user

        stream = user.profile.get_stream()
        serializer = PostSerializer(stream, many=True)
        #return JsonResponse(serializer.data, safe=False)


        mypaginator = custom()
        results = mypaginator.paginate_queryset(stream,request)
        page = self.request.GET.get('page', 1)
        page_num = self.request.GET.get('size', 1000)
        serializer = PostSerializer(results, many=True)
        return Response(OrderedDict([('count', mypaginator.page.paginator.count),
        ('current', page),
        ('next', mypaginator.get_next_link()),
        ('previous', mypaginator.get_previous_link()),
        ('size', page_num),
        ('posts', serializer.data)]))

      


class ProfilePostDetailView(APIView):
    """
    Lists posts by the specified author that are visible to the requesting user.
    """

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
                                    many=True)  # TODO maybe a different serilizer for validating that permissions are met
        return Response(OrderedDict([('count', mypaginator.page.paginator.count),
                                     ('current', page),
                                     ('next', mypaginator.get_next_link()),
                                     ('previous', mypaginator.get_previous_link()),
                                     ('size', page_num),
                                     ('posts', serializer.data)])
                        )
