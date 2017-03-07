
from rest_framework.response import Response
from rest_framework import mixins, viewsets, permissions

from ..models import WebSite, Feed, Post, Options

from .serializers import WebSiteSerializer
from .serializers import FeedSerializer
from .serializers import PostSerializer
from .serializers import CategorySerializer
from .serializers import SubscriptionSerializer
from .permission import IsSubscriptionOwner

from category.models import Category


from .throttle import WebSiteThrottle, FeedThrottle, PostThrottle, SubscriptionThrottle


class WebSiteViewSet(viewsets.ViewSet):
    """
    API endpoint that allows feeds to be listed.
    """

    throttle_class = (WebSiteThrottle,)
    serializer = WebSiteSerializer
    queryset = WebSite.objects.all()


class FeedViewSet(viewsets.ViewSet):
    """
    API endpoint that allows feeds to be listed.
    """

    throttle_class = (FeedThrottle,)
    serializer = FeedSerializer
    queryset = Feed.objects.all()


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
