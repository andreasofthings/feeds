#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

from django.conf.urls import url, patterns, include

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
from .views import CategoryListView, CategoryCreateView
from .views import CategoryDetailView
from .views import CategoryUpdateView
from .views import CategoryDeleteView
from .views import TagListView, TagDetailView
from .views import TagCreateView, TagUpdateView

from .views import SiteSubmitWizardView, SiteSubmitForms

from .views import BackupView

from .rss import RssFeed

from .api_views import UserSubscriptions
from .sitemap import PostSitemap

from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'posts': PostSitemap,
}


urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^options$', OptionsView.as_view(), name="options"),
    url(r'^opml$', OPMLView.as_view(), name="opml"),
    url(r'^search/', include('haystack.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap')
)

urlpatterns += patterns(
    '',
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
    )

urlpatterns += patterns(
    '',
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
)

urlpatterns += patterns(
    '',
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
)

urlpatterns += patterns(
    '',
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
)

urlpatterns += patterns(
    '',
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
)

urlpatterns += patterns(
    '',
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
    url(
        r'^category/(?P<pk>\w+)/$',
        CategoryDetailView.as_view(),
        name="category-view"
    ),
    url(
        r'^category/(?P<pk>\w+)/update$',
        CategoryUpdateView.as_view(),
        name="category-update"
    ),
    url(
        r'^category/(?P<pk>\w+)/delete$',
        CategoryDeleteView.as_view(),
        name="category-delete"
    ),
)

urlpatterns += patterns(
    '',
    url(
        r'^tag /$',
        TagListView.as_view(),
        name="tag-home"
    ),
    url(
        r'^tag/page/(?P<page>\w+)/$',
        TagListView.as_view(),
        name="tag-home-paginated"
    ),
    url(
        r'^tag/add/$',
        TagCreateView.as_view(),
        name="tag-add"
    ),
    url(
        r'^tag/(?P<slug>[\w-]+)/$',
        TagDetailView.as_view(),
        name="tag-view"
    ),
    url(
        r'^tag/(?P<id>\d+)/update/$',
        TagUpdateView.as_view(),
        name="tag-update"
    ),
)

#
# Backup
#

urlpatterns += patterns(
    '',
    url(r'^backup/$', BackupView.as_view(), name="backup"),
)

#
# RSS
#


urlpatterns += patterns(
    '',
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
)

#
# Legacy API
#

urlpatterns += patterns(
    '',
    url(
        r'/api/v1/subscriptions$',
        UserSubscriptions.as_view(),
        name="subscription-api"
    ),
)
