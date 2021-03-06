from django.conf.urls import url
from posts.api.viewsets import PostViewSet
from comments.api.viewsets import CommentViewSet
from posts.api.views import ProfilePostsListView, ProfilePostDetailView
from users.api.views import RegisterUserView, AuthenticatedUserProfileView, UserRelationshipCheckView, AuthenticatedUserRelationshipView, AuthenticatedUserFollowingListView, AuthenticatedUserFollowersListView
from users.api.viewsets import ProfileViewSet, UserRelationshipViewSet,UserRelationshipFriendRequestViewSet, MyFriendsProfilesViewSet
from posts.api.views import AllPublicPostsView

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
my_friends_list = MyFriendsProfilesViewSet.as_view({
    'get': 'list'
})
profile_list = ProfileViewSet.as_view({
    'get': 'list'
})
profile_list_local = ProfileViewSet.as_view({
    'get': 'list_local'
})
profile_detail = ProfileViewSet.as_view({
    'get': 'retrieve',
    'put': 'update'
})
post_detail_comments = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
author_friends_list = UserRelationshipViewSet.as_view({
    'get': 'list',
    'post' : 'query',
})
author_friend_requests_list = UserRelationshipFriendRequestViewSet.as_view({
    'get': 'list',
    'post': 'create_or_update',
    'delete': 'destroy'
})
author_friend_requests_detail = UserRelationshipFriendRequestViewSet.as_view({
    'delete': 'destroy',
})

urlpatterns = [
    # These are the APIs for our own frontend
    url(r'^register/$', RegisterUserView.as_view(), name='register_user'),
    url(r'^friendrequest/(?P<pk>[0-9]+)/$', author_friend_requests_detail, name='friend-request'),
    url(r'^posts/all/$', AllPublicPostsView.as_view(), name='all-public-post-list'),
    url(r'^author/all/$', profile_list, name='all_users'),
    url(r'^author/me/$', AuthenticatedUserProfileView.as_view(), name='auth_profile_detail'),
    url(r'^author/me/relationship/(?P<uuid>[^/]+)/$', AuthenticatedUserRelationshipView.as_view(), name='authenticated-user-relationship-detail'),
    url(r'^author/me/followers/$', AuthenticatedUserFollowersListView.as_view(), name='authenticated-user-followers-list'),
    url(r'^author/me/following/$', AuthenticatedUserFollowingListView.as_view(), name='authenticated-user-following-list'),
    url(r'^author/local/$', profile_list_local, name='all_users_local'),

    # These are the publicly accessible apis
    url(r'^friendrequest/$', author_friend_requests_list, name='friend-request'), # TODO DOCUMENT
    url(r'^posts/$', post_list, name='post-list'), # TODO DOCUMENT
    url(r'^posts/(?P<uuid>[^/]+)/$', post_detail, name='post-detail'), # TODO DOCUMENT
    url(r'^posts/(?P<uuid_input>[^/]+)/comments/$', post_detail_comments, name='post-detail-comments'), # TODO DOCUMENT
    url(r'^author/$', my_friends_list, name='my-friends-list'), # TODO DOCUMENT
    url(r'^author/posts/$', ProfilePostsListView.as_view(), name='profile-post-list'), # TODO DOCUMENT
    url(r'^author/(?P<uuid>[^/]+)/$', profile_detail, name='profile-detail'), # TODO DOCUMENT
    url(r'^author/(?P<uuid>[^/]+)/posts/$', ProfilePostDetailView.as_view(), name='profile-post-detail'), # TODO DOCUMENT
    url(r'^author/(?P<uuid>[^/]+)/friends/$', author_friends_list, name='author-friends-list'), # TODO DOCUMENT
    url(r'^author/(?P<uuid>[^/]+)/friends/(?P<uuid_2>[^/]+)/$', UserRelationshipCheckView.as_view(), name='check_author_relationship'), # TODO DOCUMENT
]
