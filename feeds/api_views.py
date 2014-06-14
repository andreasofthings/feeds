from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from feeds.models import Subscription, Feed


class SubscriptionThrottle(UserRateThrottle):
    rate = '1/second'


class UserSubscriptions(APIView):
    def get(self, request, format=None):
        """
        Return a list of all user subscriptions, all Feeds if anonymous.
        """
        if request.user.is_authenticated():
            result = Subscription.objects.filter(user=request.user).feed_set.all()
        else:
            result = Feed.objects.all()
        return Response(result)
