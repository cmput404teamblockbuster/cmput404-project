from django.conf.urls import url

from posts.api.viewsets import PostViewSet

from users.api.viewsets import ProfileViewSet

post_list = PostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
post_detail = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})
profile_list = ProfileViewSet.as_view({
    'get': 'list'
})
profile_detail = ProfileViewSet.as_view({
    'get': 'retrieve'
})

# user_detail_post = UserPostViewSet({
#     # 'get' : 'retrieve'
# })
# post_detail_comments = CommentViewSet({
#     'get': 'list',
#     'post': 'create'
# })
# user_list_post = UserPostViewSet.as_view({
#     'get': 'list'
# })
# Notice how we're creating multiple views from each ViewSet class, by binding the http methods to the required action for each view.
#
# Now that we've bound our resources into concrete views, we can register the views with the URL conf as usual.

urlpatterns = [
    url(r'^posts/$', post_list, name='post-list'),
    url(r'^posts/(?P<uuid>[^/]+)/$', post_detail, name='post-detail'),
    # url(r'^posts/(?P<uuid>[^/]+)/comments/$', post_detail_comments, name='post-detail-comments'),
    url(r'^author/$', profile_list, name='profile-list'),
    url(r'^author/posts/$', 'posts.views.profile_post_list', name='profile-post-list'),
    url(r'^author/(?P<uuid>[^/]+)/$', profile_detail, name='profile-detail'),
    url(r'^author/(?P<uuid>[^/]+)/posts/$', 'posts.views.profile_post_detail', name='profile-post-detail')
]