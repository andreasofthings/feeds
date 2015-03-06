from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework import mixins, viewsets

from .models import Options, Feed, Job
from .serializers import SubscriptionSerializer
from .serializers import FeedSerializer
from .serializers import JobSerializer


class JobViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """
    API endpoint that allows jobs to be viewed or created.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class FeedThrottle(UserRateThrottle):
    rate = "1/second"


class FeedViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    API endpoint that allows feeds to be listed.
    """
    throttle_class = (FeedThrottle,)
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer


class SubscriptionThrottle(UserRateThrottle):
    rate = '1/second'


class UserSubscriptions(APIView):
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
