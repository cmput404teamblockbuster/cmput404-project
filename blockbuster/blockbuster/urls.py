from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'blockbuster.views.myStream', name='myStream'),
    url(r'^login/', 'blockbuster.views.login', name='login'),
    url(r'^myFriends/$', 'blockbuster.views.myFriends', name='myFriends'),
    url(r'^profile/', 'blockbuster.views.profile', name='profile'),
    url(r'^api/', include('api.urls')),
    url(r'^obtain-auth-token/$', obtain_auth_token),
    url(r'^docs/', include('rest_framework_docs.urls')),

]
