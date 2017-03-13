from django.conf.urls import url
from posts.api.viewsets import PostViewSet
from users.api.viewsets import ProfileViewSet
from comments.api.viewsets import CommentViewSet
from posts.api.views import ProfilePostsListView, ProfilePostDetailView
from users.api.views import RegisterUserView, AuthenticatedUserProfileView
from users.api.viewsets import UserRelationshipViewSet
from users.api.viewsets import UserRelationshipFriendRequestViewSet

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
author_friends = UserRelationshipViewSet.as_view({
    'get': 'list',
})
author_friend_requests = UserRelationshipFriendRequestViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

urlpatterns = [
    url(r'^register/$', RegisterUserView.as_view(), name='register_user'),
    url(r'^friendrequest/$', author_friend_requests, name='friend-request'),
    url(r'^posts/$', post_list, name='post-list'),
    url(r'^posts/(?P<uuid>[^/]+)/$', post_detail, name='post-detail'),
    url(r'^posts/(?P<uuid>[^/]+)/comments/$', post_detail_comments, name='post-detail-comments'),
    url(r'^author/$', profile_list, name='profile-list'),
    url(r'^author/posts/$', ProfilePostsListView.as_view(), name='profile-post-list'),
    url(r'^author/me/$', AuthenticatedUserProfileView.as_view(), name='auth_profile_detail'),
    url(r'^author/(?P<uuid>[^/]+)/$', profile_detail, name='profile-detail'),
    url(r'^author/(?P<uuid>[^/]+)/posts/$', ProfilePostDetailView.as_view(), name='profile-post-detail'),
    url(r'^author/(?P<uuid>[^/]+)/friends/$', author_friends, name='author-friends-list'),

]