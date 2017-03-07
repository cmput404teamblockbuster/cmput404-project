from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'blockbuster.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'blockbuster.views.home', name='home'),
    url(r'^login/', 'users.accounts.views.login', name='login'),
    url(r'^api/author', include('users.api.urls')),
]
