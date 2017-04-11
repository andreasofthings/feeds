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
from .views import UserSubscriptionsViewSet


router = routers.DefaultRouter()
# register job endpoint in the router
router.register(r'options', OptionsViewSet)
router.register(r'websites', WebSiteViewSet)
router.register(r'feeds', FeedViewSet)
router.register(r'posts', PostViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subscriptions', UserSubscriptionsViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]
