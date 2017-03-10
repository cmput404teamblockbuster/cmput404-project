from django.conf.urls import url
from posts.api.viewsets import PostViewSet
from users.api.viewsets import ProfileViewSet
from comments.api.viewsets import CommentViewSet

"""
contents from this file are from http://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/#binding-viewsets-to-urls-explicitly
"""

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

post_detail_comments = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

urlpatterns = [
    url(r'^posts/$', post_list, name='post-list'),
    url(r'^posts/(?P<uuid>[^/]+)/$', post_detail, name='post-detail'),
    url(r'^posts/(?P<uuid>[^/]+)/comments/$', post_detail_comments, name='post-detail-comments'),
    url(r'^author/$', profile_list, name='profile-list'),
    url(r'^author/posts/$', 'posts.views.profile_post_list', name='profile-post-list'),
    url(r'^author/(?P<uuid>[^/]+)/$', profile_detail, name='profile-detail'),
    url(r'^author/(?P<uuid>[^/]+)/posts/$', 'posts.views.profile_post_detail', name='profile-post-detail')
]