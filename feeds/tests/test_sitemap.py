#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from django.test import TransactionTestCase, Client
from feeds.models import Feed


class SitemapTest(TransactionTestCase):
    """
    Test sitemaps.
    """

    fixtures = [
        'Feed_basic.yaml',
        'Posts.yaml'
    ]

    def setUp(self):
        self.client = Client()
        for feed in Feed.objects.all():
            feed.refresh()

    def test_sitemap(self):
        result = self.client.get('/feeds/sitemap.xml')
        self.assertEqual(result.status_code, 200)
        result = self.client.get('/feeds/sitemap-feeds.xml')
        self.assertEqual(result.status_code, 200)
        result = self.client.get('/feeds/sitemap-posts.xml')
        self.assertEqual(result.status_code, 200)
