from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework import mixins, viewsets, permissions

from ..models import Options, Feed, Post

from .serializers import SubscriptionSerializer
from .serializers import CategorySerializer
from .serializers import FeedDetailSerializer, FeedListSerializer
from .serializers import PostSerializer
from .permission import IsSubscriptionOwner

from category.models import Category


class FeedThrottle(UserRateThrottle):
    rate = "1/second"


class PostThrottle(UserRateThrottle):
    rate = "4/second"


class SubscriptionThrottle(UserRateThrottle):
    rate = '1/second'

    
class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """
    API endpoint that allows categories to be listed.
    """
    throttle_class = (FeedThrottle,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    API endpoint that allows feeds to be listed.
    """
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000
    throttle_class = (PostThrottle,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class FeedViewSet(viewsets.ViewSet):
    """
    API endpoint that allows feeds to be listed.
    """
    
    throttle_class = (FeedThrottle,)
    
    def list(self, request):
        queryset = Feed.objects.all()
        serializer = FeedListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Feed.objects.all()
        feed = get_object_or_404(queryset, pk=pk)
        serializer = FeedDetailSerializer(feed)
        return Response(serializer.data)




class UserSubscriptions(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer

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
