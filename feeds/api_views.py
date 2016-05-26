from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework import mixins, viewsets

from .models import Options, Feed, Post
from .serializers import SubscriptionSerializer
from .serializers import CategorySerializer
from .serializers import FeedDetailSerializer, FeedListSerializer
from .serializers import PostSerializer

from category.models import Category


class FeedThrottle(UserRateThrottle):
    rate = "1/second"


class PostThrottle(UserRateThrottle):
    rate = "4/second"


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


class FeedViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    API endpoint that allows feeds to be listed.
    """
    throttle_class = (FeedThrottle,)
    
    def list(self, request):
        queryset = Feed.objects.all()
        data = FeedListSerializer(queryset, many=True)
        return Response(data.data)
        
    def retrieve(self, request, pk=None):
        queryset = Feed.objects.all()
        feed = get_object_or_404(queryset, pk=pk)
        data = FeedDetailSerializer(feed)
        return Response(data.data)



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
