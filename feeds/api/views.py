#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Feeds API.

All views related to Feeds API exist here.
"""

import datetime
from rest_framework import renderers, views
from rest_framework import status, mixins, viewsets, permissions, response
from rest_framework.generics import RetrieveAPIView

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.conf import settings

import feedparser
from ..models import WebSite, Feed, Post, Options, Subscription, Category

from .serializers import OptionsSerializer
from .serializers import WebSiteSerializer
from .serializers import FeedSerializer, FeedPKSerializer
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

LOG = logging.getLogger(__name__)


class CronView(views.APIView):
    """
    A view to handle GCP cron invocation.

    A view that will handle all invocations issued by `GCP cron`.
    """

    # queryset = get_user_model().objects.all()
    permission_classes = (permissions.AllowAny,)
    delay = 10

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        """
        Avoid CSRF Protection for Cloud-Tasks.

        Avoid CSRF Protection for Cloud-Tasks by decorating
        the `dispatch` method.
        """
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        """Cronview POST method."""
        return self.post(request)

    def post(self, request):
        """
        GET `/postfeed/cron`.

        Run Cronjobs when triggered by external GET.
        """
        if request:
            for feed in Feed.objects.all():
                # actually, rather serialize the real object than some mock.
                f = FeedPKSerializer(
                    feed,
                    context={'request': request}
                )
                LOG.debug("sending task feed: %s", feed)
                if settings.GOOGLE_APP_ENGINE:
                    from google.protobuf import timestamp_pb2
                    from google.cloud import tasks as tasks

                    client = tasks.CloudTasksClient()
                    project = "pramari-de"
                    queue = "default"
                    location = "europe-west3"
                    parent = client.queue_path(project, location, queue)
                    task = {
                        # "http_request": {  # Specify the type of request.
                        "app_engine_http_request": {  # Specify the requesttype
                            "http_method": "POST",
                            "relative_uri": "/feeds/api/cron/feed",
                            "body": renderers.JSONRenderer().render(f.data),
                            "headers": {"content-type": "application/json"},
                        },
                        "schedule_time":
                        timestamp_pb2.Timestamp().FromDatetime(
                            datetime.datetime.utcnow() + \
                            datetime.timedelta(seconds=self.delay)
                        ),
                    }
                    # task["app_engine_http_request"]["content-type"] = \
                    # "application/json"
                    LOG.debug("emitted task `%s` for obj", task)
                    self.delay += 10
                    task = client.create_task(parent, task)
                else:
                    return response.Response(
                        "No change!",
                        status=status.HTTP_200_OK
                    )
        return response.Response("OK!", status=status.HTTP_200_OK)


class CronFeedView(views.APIView):
    """
    CronFeedView.

    View Class relating to `Feed` operations.

    Tests:

    """

    # queryset = get_user_model().objects.all()
    # parser_classes = (FeedTaskParser,)

    permission_classes = (permissions.AllowAny,)
    serializer_class = FeedSerializer

    def get(self, request):
        """
        HTTP GET /postfeed/feed/.

        Return OK on case of HTTP GET
        """
        if request:
            return response.Response("GET OK!", status=status.HTTP_200_OK)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        """
        Avoid CSRF Protection for Cloud-Tasks.

        ToDo::
            Actually verify headers for GCP initiated requests.
            See:
            https://cloud.google.com/tasks/docs/creating-appengine-handlers
        """
        return super().dispatch(*args, **kwargs)

    def post(self, request, format=None):
        """
        POST /postfeed/feed.

        Receive serialized `FeedURL`, process all parsable `Entry`s.
        """
        serialized = FeedPKSerializer(
            data=request.data,
            context={'request': request}
        )
        if serialized.is_valid():
            pk = serialized.data.get("pk", None)
            if not pk:
                return response.Response(
                    "NO CONTENT", status=status.HTTP_204_NO_CONTENT
                )
            feed = Feed.objects.get(pk=pk)
            feed.refresh()
            return response.Response(
                "POST OK!",
                status=status.HTTP_201_CREATED
            )
        else:
            LOG.error("invalid de-serialized: %s", serialized.data)
            LOG.error("de-serialized errors: %s", serialized.errors)
            return response.Response("POST OK!", status=status.HTTP_200_OK)


class OptionsView(RetrieveAPIView):
    """
    APIView Options.

    Provide an API to retrieve User Options.

    """

    throttle_class = (OptionsThrottle, )
    serializer_class = OptionsSerializer
    queryset = Options.objects.all()
    permissions = (permissions.IsAuthenticated, )

    def retrieve(self, request, username=None, *args, **kwargs):
        """
        Get.

        Return Users Options.
        """
        queryset = Options.objects.filter(user=request.user)
        result = OptionsSerializer(queryset, many=True)
        return response.Response(result.data)


class WebSiteViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    WebSiteViewSet.

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
    View Feeds.

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
    PostViewSet.

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
    CategoryViewSet.

    API endpoint that allows categories to be listed.
    """

    throttle_class = (FeedThrottle,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UserSubscriptionsViewSet(viewsets.GenericViewSet):
    """
    UserSubscriptionsViewSet.

    API Endpoint to list User Subscriptions.
    """

    serializer_class = SubscriptionSerializer
    throttle_class = (SubscriptionThrottle,)
    queryset = Subscription.objects.all()
    permissions = (IsOwner, )
