from django.conf.urls import url, include, patterns

#
# API
#
from .api_views import FeedViewSet
from rest_framework import routers

router = routers.DefaultRouter()
# register job endpoint in the router
router.register(r'feeds', FeedViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    url(
        r'^api-auth/',
        include(
            'rest_framework.urls',
            namespace='rest_framework')
    ),
)
