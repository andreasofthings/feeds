#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Tests the posts manager.
=======================
"""

from django.test import TestCase
from datetime import timedelta

from feeds.models import Post

import logging

logger = logging.getLogger(__name__)


class ManagerTest(TestCase):
    """
    Test PostManager

    :py:mod:`feeds.tests.ModelTest` aims to test following models:
    """
    fixtures = [
        "Feed_basic.yaml",
        "Posts.yaml",
    ]

    def setUp(self):
        """
        Set up enivironment to test models
        """
        logger.debug("setUp Tests for `Post`-Manager.")

    def test_post_manager_older_than(self):
        """
        Posts.yaml has one entry from 2000-01-01.

        This should be older than 1 day, but not older than 100 years.
        Hence, count should be 1, respectively 0.
        """
        p = Post.objects.older_than(timedelta(days=100*365))
        self.assertEqual(len(p), 0)
        p = Post.objects.older_than(timedelta(days=1))
        self.assertEqual(len(p), 4)

    def test_post_category(self):
        p = Post.objects.get(pk=1)
        cat, created = p.categories.get_or_create(
            name="category"
        )

    def tearDown(self):
        """
        Clean up environment after model tests
        """
        pass
