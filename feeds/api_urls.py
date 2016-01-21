from django.conf.urls import url, include

#
# API
#
from .api_views import FeedViewSet
from .api_views import PostViewSet
from .api_views import CategoryViewSet
from rest_framework import routers

router = routers.DefaultRouter()
# register job endpoint in the router
router.register(r'categories', CategoryViewSet)
router.register(r'feeds', FeedViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(
        r'^api-auth/',
        include(
            'rest_framework.urls',
            namespace='rest_framework')
    ),
]
