#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

from django.conf.urls import url, include

from .views import HomeView
from .views import OptionsView
from .views import OPMLView
from .views import SiteListView
from .views import SiteCreateView
from .views import SiteDetailView
from .views import SiteUpdateView
from .views import SiteDeleteView

from .views import FeedCreateView
from .views import FeedListView
from .views import FeedDetailView
from .views import FeedUpdateView
from .views import FeedDeleteView
from .views import FeedRefreshView
from .views import FeedSubscribeView
from .views import FeedUnSubscribeView

from .views import FeedSubscriptionsView

from .views import PostListView, PostDetailView, PostTrackableView

from .views import SiteSubmitWizardView, SiteSubmitForms

from .rss import RssFeed

from .api_views import UserSubscriptions
from .sitemap import PostSitemap, FeedSitemap

from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps.views import index as sitemap_index
from django.views.decorators.cache import cache_page

sitemaps = {
    'feeds': FeedSitemap,
    'posts': PostSitemap,
}


urlpatterns = [
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^options$', OptionsView.as_view(), name="options"),
    url(r'^opml$', OPMLView.as_view(), name="opml"),
    url(r'^search/', include('haystack.urls')),
    url(
        r'^sitemap\.xml$',
        cache_page(86400)(sitemap_index),
        {
            'sitemaps': sitemaps,
            'sitemap_url_name': 'planet:sitemaps'
        },
        name='sitemap'
    ),
    url(
        r'^sitemap-(?P<section>.+)\.xml$',
        cache_page(86400)(sitemap),
        {
            'sitemaps': sitemaps
        },
        name='sitemaps'
    ),

    url(
        r'^site/$',
        SiteListView.as_view(),
        name="site-home"
    ),
    url(
        r'^site/submit/$',
        SiteSubmitWizardView.as_view(SiteSubmitForms),
        name="site-submit"
    ),
    url(
        r'^site/add/$',
        SiteCreateView.as_view(),
        name="site-add"
    ),
    url(
        r'^site/(?P<pk>\d+)/$',
        SiteDetailView.as_view(),
        name="site-view"
    ),
    url(
        r'^site/(?P<pk>\d+)/update/$',
        SiteUpdateView.as_view(),
        name="site-update"
    ),
    url(
        r'^site/(?P<pk>\d+)/delete/$',
        SiteDeleteView.as_view(),
        name="site-delete"
    ),
]

urlpatterns += [
    url(r'^list/$', FeedListView.as_view(), name="feed-home"),
    url(
        r'^page/(?P<page>\w+)/$',
        FeedListView.as_view(),
        name="feed-home-paginated"
    ),
    url(
        r'^add/$',
        FeedCreateView.as_view(),
        name="feed-add"
    ),
    url(
        r'^feed/(?P<pk>\d+)/$',
        FeedDetailView.as_view(),
        name="feed-view"
    ),
    url(
        r'^feed/(?P<pk>\d+)/update/$',
        FeedUpdateView.as_view(),
        name="feed-update"
    ),
    url(
        r'^feed/(?P<pk>\d+)/delete/$',
        FeedDeleteView.as_view(),
        name="feed-delete"
    ),
    url(
        r'^feed/(?P<pk>\d+)/refresh/$',
        FeedRefreshView.as_view(),
        name="feed-refresh"
    ),
]

urlpatterns += [
    url(
        r'^feed/(?P<pk>\d+)/subscribe/$',
        FeedSubscribeView.as_view(),
        name="feed-subscribe"
    ),
    url(
        r'^feed/(?P<pk>\d+)/unsubscribe/$',
        FeedUnSubscribeView.as_view(),
        name="feed-unsubscribe"
    ),
    url(
        r'^feed/subscriptions/$',
        FeedSubscriptionsView.as_view(),
        name="feed-subscriptions"
    ),
    url(
        r'^(?P<pk>\d+)/$',
        PostDetailView.as_view(),
        name="post-view"
    ),
    url(
        r'^p/$',
        PostListView.as_view(),
        name="post-home"
    ),
    url(
        r'^p/page(?P<page>[0-9]+)/$',
        PostListView.as_view(),
        name="post-home-paginated"
    ),
    url(
        r'^f/(?P<feed_id>\d+)/$',
        RssFeed(),
        name="rss"
    ),
    url(
        r'^t/(?P<pk>\d+)/$',
        PostTrackableView.as_view(),
        name="post-trackable-view"
    ),
]

#
# Backup / RSS / Legacy API
#

urlpatterns += [
    url(
        r'test/rss1/$',
        TemplateView.as_view(template_name="feeds/tests/rss1.html"),
        name="rss1"
    ),
    url(
        r'test/rss2/$',
        TemplateView.as_view(template_name="feeds/tests/rss2.html"),
        name="rss2"
    ),
    url(
        r'api/v1/subscriptions$',
        UserSubscriptions.as_view(),
        name="subscription-api"
    ),
]
