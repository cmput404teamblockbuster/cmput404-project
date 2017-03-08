from rest_framework import routers
from posts.api.viewsets import PostViewSet
from users.api.viewsets import AuthorViewSet

api_router = routers.SimpleRouter()


"""
information regarding routers from http://www.django-rest-framework.org/api-guide/routers/#usage
"""
# author module
api_router.register(r'author', AuthorViewSet, base_name='authors')

# posts module
api_router.register(r'posts', PostViewSet, base_name='posts')

