#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Feeds API views.
"""


from rest_framework.response import Response
from rest_framework import mixins, viewsets, permissions

from ..models import WebSite, Feed, Post, Options

from .serializers import OptionsSerializer
from .serializers import WebSiteSerializer
from .serializers import FeedSerializer
from .serializers import PostSerializer
from .serializers import CategorySerializer
from .serializers import SubscriptionSerializer
from .permission import IsSubscriptionOwner

from category.models import Category

from .throttle import OptionsThrottle
from .throttle import WebSiteThrottle
from .throttle import FeedThrottle
from .throttle import PostThrottle
from .throttle import SubscriptionThrottle

import logging

log = logging.getLogger(__name__)


class OptionsViewSet(viewsets.GenericViewSet):
    throttle_class = (OptionsThrottle, )
    serializer_class = OptionsSerializer
    queryset = Options.objects.all()
    permissions = (permissions.IsAuthenticated, )

    def list(self, request, format=None):
        """
        Return Users Options.
        """
        queryset = Options.objects.all()
        result = OptionsSerializer(queryset, many=True)
        return Response(result.data)


class WebSiteViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    API endpoint that allows WebSites to be listed.
    """

    throttle_class = (WebSiteThrottle,)
    serializer_class = WebSiteSerializer
    queryset = WebSite.objects.all()


class FeedViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    API endpoint that allows feeds to be listed.
    """

    throttle_class = (FeedThrottle,)
    serializer_class = FeedSerializer
    queryset = Feed.objects.all()


class PostViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    API endpoint that allows feeds to be listed.
    """
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000
    throttle_class = (PostThrottle,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """
    API endpoint that allows categories to be listed.
    """
    throttle_class = (FeedThrottle,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UserSubscriptions(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    throttle_class = (SubscriptionThrottle,)

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsSubscriptionOwner(),)

    def get(self, request, format=None):
        """
        Return a list of all user subscriptions, all Feeds if anonymous.
        """
        if request.user.is_authenticated():
            subscriptions = Options.objects.filter(user=request.user)
            result = subscriptions.feed_subscription.all()
        else:
            result = Feed.objects.all()
        return Response(SubscriptionSerializer(result, many=True).data)
