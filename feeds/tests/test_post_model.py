#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from django.test import TestCase
from feeds.models import Post, Feed


class TestPostModel(TestCase):
    """
    Tests for Post model.

    Derived from pythons unittest.TestCase:
    https://docs.python.org/3/library/unittest.html#unittest.TestCase
    """

    fixtures = [
        'Feed_all.yaml',
        'Posts.yaml',
    ]

    def setUp(self):
        pass

    def test_post_instance(self):
        """
        Test whether a Post can be instanciated.
        """
        from django.utils import timezone
        f = Feed.objects.get(pk=1)
        p = Post.objects.get_or_create(
            feed=f,
            title="Test",
            link="https://neumeier.org"
            published=timezone.now()
            )
        self.assertIsInstance(p, Post)

    def tearDown(self):
        pass
