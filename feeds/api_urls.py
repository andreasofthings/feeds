from django.conf.urls import url, include, patterns

#
# API
#
from .views import JobViewSet
from rest_framework import routers

router = routers.DefaultRouter()
# register job endpoint in the router
router.register(r'jobs', JobViewSet)

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
