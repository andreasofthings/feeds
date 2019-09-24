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
from .views import OptionsView
from .views import WebSiteViewSet
from .views import FeedViewSet
from .views import PostViewSet
from .views import CategoryViewSet
from .views import UserSubscriptionsViewSet


router = routers.DefaultRouter()
# register job endpoint in the router
router.register(r'websites', WebSiteViewSet)
router.register(r'feeds', FeedViewSet)
router.register(r'posts', PostViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subscriptions', UserSubscriptionsViewSet)

schema_view = get_schema_view(title="Feeds API")

urlpatterns = [
    path('', include(router.urls)),
    path('schema', schema_view),
    path('cron', CronView.as_view()),
    path('options/', OptionsView.as_view()),
    path('options/<slug:username>/', OptionsView.as_view())
]
