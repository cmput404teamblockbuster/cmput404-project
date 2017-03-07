# User routers http://www.django-rest-framework.org/api-guide/routers/
from django.conf.urls import url, include
from users.api.routers import author_router

urlpatterns = (
    url(r'', include(author_router.urls)),
)