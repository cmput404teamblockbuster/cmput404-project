from django.http import JsonResponse
from rest_framework.exceptions import MethodNotAllowed
from posts.api.serializers import PostSerializer
from posts.models import Post

from users.models import Profile


def profile_post_list(request):
    """
    List all posts available to currently authed user
    from http://www.django-rest-framework.org/tutorial/1-serialization/#writing-regular-django-views-using-our-serializer
    """
    user = request.user

    if request.method == 'GET':
        stream = user.profile.get_stream()
        serializer = PostSerializer(stream, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        raise MethodNotAllowed('POST')


def profile_post_detail(request, uuid):
    """
    display posts by the specified author that are visible to the logged in user

    """
    print type(uuid)
    result = []
    from pprint import pprint
    # pprint(vars(request))
    author = Profile.objects.get(uuid=uuid)
    users_posts = Post.objects.filter(author=author).order_by('-created')  # get all posts by the specified user
    print users_posts
    for post in users_posts:
        if post.is_public or request.user.id in post.viewable_to:  # check if the post is visible to logged in user
            result.append(post)

    # TODO implement pagination here

    serializer = PostSerializer(result,
                                many=True)  # TODO maybe a different serilizer for validating that permissions are met
    # return Response(serializer.data)
    return JsonResponse(serializer.data, safe=False)