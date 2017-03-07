from django.conf.urls import url, include

"""
# API for :mod:`feeds`

"""

from rest_framework import routers

from .views import SiteViewSet
from .views import FeedViewSet
from .views import PostViewSet
from .views import CategoryViewSet

router = routers.DefaultRouter()
# register job endpoint in the router
router.register(r'sites', SiteViewSet)
router.register(r'feeds', FeedViewSet)
router.register(r'posts', PostViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
