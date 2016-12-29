#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class ApiTest(TestCase):
    """
    Test Models and their Managers

    :py:mod:`feeds.tests.ModelTest` aims to test following models:

    - :py:mod:`feeds.models.SiteManager`
    - :py:mod:`feeds.models.Site`
    - :py:mod:`feeds.models.TagManager`
    - :py:mod:`feeds.models.Tag`
    - :py:mod:`feeds.models.Feed`
    - :py:mod:`feeds.models.Post`
    - :py:mod:`feeds.models.Enclosure`

    .. codeauthor:: Andreas Neumeier <andreas@neumeier.org>
    """
    fixtures = [
        "Feed_all.yaml",
    ]

    def setUp(self):
        """
        Set up environment to test the API
        """
        self.client = Client()

    def test_subscription_anonymous(self):
        """
        request subscription, expect a list of all feeds in json

        .. todo:: This ain't done yet.
        """
        self.assertEqual(True, True)

    def tearDown(self):
        """
        Clean up environment after model tests
        """
        pass
