from rest_framework import routers

from users.api.viewsets import AuthorBasedPostsViewSet

author_router = routers.SimpleRouter()

# posts module
author_router.register(r'posts', AuthorBasedPostsViewSet)


