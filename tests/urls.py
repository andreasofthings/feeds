#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
urly.py to allow tests in travis-ci
"""

from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from django.contrib import admin
from feeds.sitemap import PostSitemap, FeedSitemap

sitemaps = {
    'feed': FeedSitemap,
    'post': PostSitemap,
}

urlpatterns = patterns('',
                       url(r'^feeds/',
                           include(
                               'feeds.urls',
                               namespace="planet",
                               app_name="planet"
                           )
                           ),
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
                       )

from django.contrib.sitemaps import views as sitemaps_views
from django.views.decorators.cache import cache_page

urlpatterns += patterns(
    '',
    url(r'^sitemap\.xml$',
        cache_page(86400)(sitemaps_views.index),
        {
            'sitemaps': sitemaps,
            'sitemap_url_name': 'sitemaps'
        }
        ),
    url(r'^sitemap-(?P<section>.+)\.xml$',
        cache_page(86400)(sitemaps_views.sitemap),
        {
            'sitemaps': sitemaps
        },
        name='sitemaps'),
    )

urlpatterns += patterns(
    url(r'^admin/', include(admin.site.urls)),
)
