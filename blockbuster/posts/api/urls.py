from django.conf.urls import include, url
from django.contrib import admin
from api.routers import api_router

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', PostViewSet, name='home'),
    # url(r'^login/', 'users.views.login', name='login'),
    url(r'^api/', include(api_router.urls)),

]
