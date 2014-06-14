#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

from django.conf.urls import url, patterns

from feeds.views import HomeView
from feeds.views import OptionsView
from feeds.views import OPMLView
from feeds.views import SiteListView
from feeds.views import SiteCreateView
from feeds.views import SiteDetailView
from feeds.views import SiteUpdateView
from feeds.views import SiteDeleteView

from feeds.views import FeedCreateView
from feeds.views import FeedListView
from feeds.views import FeedDetailView
from feeds.views import FeedUpdateView
from feeds.views import FeedDeleteView
from feeds.views import FeedRefreshView


from feeds.views import PostListView, PostDetailView, PostTrackableView
from feeds.views import CategoryListView, CategoryCreateView
from feeds.views import CategoryDetailView, CategoryUpdateView
from feeds.views import TagListView, TagDetailView
from feeds.views import TagCreateView, TagUpdateView

from feeds.views import SiteSubmitWizardView, SiteSubmitForms

from feeds.rss import RssFeed

urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^options$', OptionsView.as_view(), name="options"),
    url(r'^opml$', OPMLView.as_view(), name="opml"),
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
        r'^(?P<pk>\d+)/$',
        PostDetailView.as_view(),
        name="post-view"
    ),
    url(
        r'^p/$',
        PostListView.as_view(),
        name="post-home"
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
        r'^category/(?P<slug>\w+)/$',
        CategoryDetailView.as_view(),
        name="category-view"
    ),
    url(
        r'^category/(?P<slug>\w+)/update$',
        CategoryUpdateView.as_view(),
        name="category-update"
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
# RSS
#

from django.views.generic import TemplateView

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
# API
#

from api_views import UserSubscriptions

urlpatterns += patterns(
    '',
    url(
        r'/api/v1/subscriptions$',
        UserSubscriptions.as_view(),
        name="subscription-api"
    ),
)
