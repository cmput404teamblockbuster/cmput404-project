from django.conf.urls import url, include
from posts.api.routers import post_router

urlpatterns = (
    url(r'', include(post_router.urls)),
)