from django.conf.urls import include, url
from django.contrib import admin
# from api.routers import api_router

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'blockbuster.views.home', name='home'),
    url(r'^api/', include('api.urls')),

]
