from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'blockbuster.views.home', name='home'),
    url(r'^login/', 'blockbuster.views.login_view', name='login'),
    url(r'^api/', include('api.urls')),
    url(r'^obtain-auth-token/$', obtain_auth_token),
    url(r'^docs/', include('rest_framework_docs.urls')),

]
