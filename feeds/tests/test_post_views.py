#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from feeds.models import Post


class TestPostAnonymous(TestCase):
    """
    Test views for Posts as anonymous.
    """

    fixtures = [
        'Site.yaml',
        'Feed_all.yaml',
        'Posts.yaml',
    ]

    def setUp(self):
        self.client = Client()

    def test_post_view(self):
        """
        Test whether a Post can be viewed anonymous.
        """
        p = Post.objects.all()[0].pk
        result = self.client.get(reverse('planet:post-detail', args=(p,)))
        self.assertEquals(result.status_code, 200)
