#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

from django.urls import include, path
from django.conf.urls import url

from .views import HomeView
from .views import OptionsView
from .views import OPMLView
from .views import WebSiteListView
from .views import WebSiteCreateView
from .views import WebSiteDetailView
from .views import WebSiteUpdateView
from .views import WebSiteDeleteView
from .views import WebSiteSubmitWizardView
from .views import WebSiteSubmitForms

from .views import FeedCreateView
from .views import FeedListView
from .views import FeedDetailView
from .views import FeedUpdateView
from .views import FeedDeleteView
from .views import FeedRefreshView
from .views import FeedSubscribeView
from .views import FeedUnSubscribeView

from .views import FeedSubscriptionsView

from .views import PostListView, PostSubscriptionView
from .views import PostDetailView, PostTrackableView

from .views import CategoryListView
from .views import CategoryCreateView
from .views import CategoryDetailView
from .views import CategoryUpdateView
from .views import TagListView
from .views import TagCreateView
from .views import TagDetailView
from .views import TagUpdateView

from .rss import RssFeed
from .syndication import LatestEntriesFeed


# from feeds.api.views import UserSubscriptions
from .sitemap import PostSitemap, FeedSitemap

from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps.views import index as sitemap_index
from django.views.decorators.cache import cache_page

sitemaps = {
    'feeds': FeedSitemap,
    'posts': PostSitemap,
}

app_name = "feeds"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('options', OptionsView.as_view(), name="options"),
    path('opml', OPMLView.as_view(), name="opml"),
    path('api/', include('feeds.api.urls')),
    path('search', include('haystack.urls')),
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
        r'^website/$',
        WebSiteListView.as_view(),
        name="website-home",
    ),
    url(
        r'^website/submit/$',
        WebSiteSubmitWizardView.as_view(WebSiteSubmitForms),
        name="website-submit"
    ),
    url(
        r'^website/add/$',
        WebSiteCreateView.as_view(),
        name="website-add"
    ),
    url(
        r'^website/(?P<pk>\d+)/$',
        WebSiteDetailView.as_view(),
        name="website-detail"
    ),
    url(
        r'^website/(?P<pk>\d+)/update/$',
        WebSiteUpdateView.as_view(),
        name="website-update"
    ),
    url(
        r'^website/(?P<pk>\d+)/delete/$',
        WebSiteDeleteView.as_view(),
        name="website-delete"
    ),
]

urlpatterns += [
    url(r'^list/$', FeedListView.as_view(), name="feed-home"),
    # url(
    #    r'^page/(?P<page>\w+)/$',
    #    FeedListView.as_view(),
    #    name="feed-home-paginated"
    # ),
    url(
        r'^add/$',
        FeedCreateView.as_view(),
        name="feed-add"
    ),
    url(
        r'^feed/(?P<pk>\d+)/$',
        FeedDetailView.as_view(),
        name="feed-detail"
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
        r'^category/$',
        CategoryListView.as_view(),
        name="category-home"
        ),
    url(
        r'^category/page/(?P<page>\w+)/$',
        CategoryListView.as_view(),
        name="category-home-paginated"
    ),
    url(
        r'^category/add/$',
        CategoryCreateView.as_view(),
        name="category-add"
    ),
    url(r'^category/id/(?P<pk>\d+)/$',
        CategoryDetailView.as_view(), name="category-detail"),
    url(r'^category/name/(?P<slug>[-\w]+)/$',
        CategoryDetailView.as_view(), name="category-detail"),
    url(
        r'^category/(?P<pk>\d+)/update$',
        CategoryUpdateView.as_view(),
        name="category-update"
    ),
    url(
        r'^category/(?P<slug>\w+)/update$',
        CategoryUpdateView.as_view(),
        name="category-update"
    ),
    url(
        r'^tag/$',
        HomeView.as_view(),
        name="tag-home"
    ),
    url(
        r'^tag/(?P<pk>\d+)/$',
        HomeView.as_view(),
        name="tag-view"
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
        r'^post/(?P<pk>\d+)/$',
        PostDetailView.as_view(),
        name="post-detail"
    ),
    url(
        r'^p/$',
        PostListView.as_view(),
        name="post-home"
    ),
    # url(
    #    r'^p/page(?P<page>[0-9]+)/$',
    #    PostListView.as_view(),
    #    name="post-home-paginated"
    # ),
    url(
        r'^s/$',
        PostSubscriptionView.as_view(),
        name="post-subscription-home"
    ),
    url(
        r'^s/page(?P<page>[0-9]+)/$',
        PostSubscriptionView.as_view(),
        name="post-subscription-home-paginated"
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


urlpatterns += [
    url(
        r'^rss/$',
        LatestEntriesFeed(),
        name="rss-feed"
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
    #    url(
    #        r'api/v1/subscriptions$',
    #        UserSubscriptions.as_view(),
    #        name="subscription-api"
    #    ),
]
