from rest_framework import routers

post_router = routers.SimpleRouter()

# posts module
post_router.register(r'comments', PostBasedCommentViewSet)


