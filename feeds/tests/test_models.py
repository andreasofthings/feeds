#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Tests for the "feeds" app.
==========================
"""

from django.test import TestCase, Client

from feeds.models import Feed
from feeds import FEED_OK


class ModelTest(TestCase):
    """
    Test Models and their Managers

    :py:mod:`feeds.tests.ModelTest` aims to test following models:

    - :py:mod:`feeds.models.SiteManager`
    - :py:mod:`feeds.models.WebSite`
    - :py:mod:`feeds.models.TagManager`
    - :py:mod:`feeds.models.Tag`
    - :py:mod:`feeds.models.Feed`
    - :py:mod:`feeds.models.Post`
    - :py:mod:`feeds.models.Enclosure`

    .. codeauthor:: Andreas Neumeier <andreas@neumeier.org>
    """
    fixtures = [
        "Feed_all.yaml",
        "Site.yaml",
        "Tags.yaml",
        "Categories.yaml",
    ]

    def setUp(self):
        """
        Set up enivironment to test models
        """
        self.client = Client()

    def test_site(self):
        """
        Create a :py:mod:`feeds.models.WebSite` Object and verify
        it functions properly.
        """

        from feeds.models import WebSite
        s = WebSite(url="https://angry-planet.com/")
        s.save()
        # self.assertContains( s.get_absolute_url(), s.pk)
        """
        .. todo:: self.assertContains won't work
        for what is being tested here.
        """
        self.assertEqual(str(s), "https://angry-planet.com/")
        """Assert the __str__ representation equals the site-name."""

    def test_tag(self):
        """
        Test a Tag
        """
        from feeds.models import Tag
        """Import the :py:mod:`feeds.models.Tag`-model."""
        t = Tag(name="tag")
        """Instanciate the model."""
        tagid = t.save()
        """Save the model and retrieve the pk/id."""
        self.assertNotEqual(tagid, 0)
        """Assert the pk/id is not 0."""
        self.assertEqual(str(t), "tag")
        """Assert the __str__ representation equals the tag-name."""
        # self.assertContains( t.get_absolute_url(), t.pk)
        """
        Assert the tag URL contains the tag.pk.

        .. todo:: self.assertContains won't work for what is being tested here.
        """

    def test_feed(self):
        """
        Test a :py:mod:`feeds:models.Feed`
        """
        feed = Feed.objects.filter(is_active=True)
        self.assertEquals(feed[0].refresh(), FEED_OK)

    def tearDown(self):
        """
        Clean up environment after model tests
        """
        pass
