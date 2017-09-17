#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
urly.py to allow tests in travis-ci
"""

from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.contrib import admin
from feeds.sitemap import PostSitemap, FeedSitemap
from django.contrib.sitemaps import views as sitemaps_views
from django.views.decorators.cache import cache_page


sitemaps = {
    'feed': FeedSitemap,
    'post': PostSitemap,
}

urlpatterns = [
    url(r'^feeds/',
        include(
            'feeds.urls',
            namespace="planet",
            app_name="planet"
        )
        ),
    url(r'^feedapi/', include('feeds.api.urls')),
    url(
        r'^testfeed1',
        TemplateView.as_view(
            template_name="test/feed1.html"
        )
    ),
    url(
        r'^accounts/login/',
        TemplateView.as_view(
            template_name="feeds/index.html"
        )
    ),
    url(r'^sitemap\.xml$',
        cache_page(86400)(sitemaps_views.index),
        {
            'sitemaps': sitemaps,
            'sitemap_url_name': 'sitemaps'
        },
        name='sitemap'
        ),
    url(r'^sitemap-(?P<section>.+)\.xml$',
        cache_page(86400)(sitemaps_views.sitemap),
        {
            'sitemaps': sitemaps
        },
        name='sitemaps'
        ),
    url(r'^admin/', include(admin.site.urls)),
]
