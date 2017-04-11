from django.conf.urls import url, include

"""
# API for :mod:`feeds`

"""

from rest_framework import routers

from .views import OptionsViewSet
from .views import WebSiteViewSet
from .views import FeedViewSet
from .views import PostViewSet

from .views import CategoryViewSet


router = routers.DefaultRouter()
# register job endpoint in the router
router.register(r'options', OptionsViewSet, base_name="planet")
router.register(r'websites', WebSiteViewSet, base_name="planet")
router.register(r'feeds', FeedViewSet, base_name="planet")
router.register(r'posts', PostViewSet, base_name="planet")
router.register(r'categories', CategoryViewSet, base_name="planet")


urlpatterns = [
    url(r'^', include(router.urls)),
]
