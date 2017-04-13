#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Feeds API urls.
API for :mod:`feeds`
"""
from django.conf.urls import url, include

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
