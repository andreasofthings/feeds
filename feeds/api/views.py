#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Feeds API views.
"""


from rest_framework.response import Response
from rest_framework import mixins, viewsets, permissions
from rest_framework.generics import RetrieveAPIView

from ..models import WebSite, Feed, Post, Options, Subscription, Category

from .serializers import OptionsSerializer
from .serializers import WebSiteSerializer
from .serializers import FeedSerializer
from .serializers import PostSerializer
from .serializers import CategorySerializer
from .serializers import SubscriptionSerializer
from .permission import IsOwner


from .throttle import OptionsThrottle
from .throttle import WebSiteThrottle
from .throttle import FeedThrottle
from .throttle import PostThrottle
from .throttle import SubscriptionThrottle

import logging

log = logging.getLogger(__name__)


class OptionsView(RetrieveAPIView):
    throttle_class = (OptionsThrottle, )
    serializer_class = OptionsSerializer
    queryset = Options.objects.all()
    permissions = (permissions.IsAuthenticated, )

    def retrieve(self, request, username=None, *args, **kwargs):
        """
        Return Users Options.
        """
        queryset = Options.objects.filter(user=request.user)
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


class UserSubscriptionsViewSet(viewsets.GenericViewSet):
    serializer_class = SubscriptionSerializer
    throttle_class = (SubscriptionThrottle,)
    queryset = Subscription.objects.all()
    permissions = (IsOwner, )
