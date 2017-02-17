from django.conf.urls import url, include

#
# API
#
from rest_framework import routers

from .views import FeedViewSet
from .views import PostViewSet
from .views import CategoryViewSet

router = routers.DefaultRouter()
# register job endpoint in the router
router.register(r'categories', CategoryViewSet)
router.register(r'feeds', FeedViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
