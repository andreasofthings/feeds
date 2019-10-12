#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Feeds API urls.
API for :mod:`feeds`
"""
from django.urls import path, include

from rest_framework import routers
from rest_framework.schemas import get_schema_view

from .views import CronView
from .views import CronFeedView
from .views import OptionsView
from .views import WebSiteViewSet
from .views import FeedViewSet
from .views import PostViewSet
from .views import CategoryViewSet
from .views import TagViewSet
from .views import SubscriptionsViewSet


router = routers.DefaultRouter()
# register job endpoint in the router
router.register(
    prefix=r'websites',
    viewset=WebSiteViewSet,
    basename='website-api'
)
router.register(
    prefix=r'feeds',
    viewset=FeedViewSet,
    basename='feed-api'
)
router.register(
    prefix=r'posts',
    viewset=PostViewSet,
    basename='post-api'
)
router.register(
    prefix=r'categories',
    viewset=CategoryViewSet,
    basename='category-api',
)
router.register(
    prefix=r'tags',
    viewset=TagViewSet,
    basename="tag-api",
)
router.register(r'subscriptions', SubscriptionsViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('schema', get_schema_view(
        title="Feeds API",
        description="API for feeds.",
        url='https://www.pramari.de/feeds/api/'),
        name='openapi-schema'),
    path('cron', CronView.as_view()),
    path('cron/feed', CronFeedView.as_view()),
    path('options/', OptionsView.as_view()),
    path('options/<slug:username>/', OptionsView.as_view())
]
