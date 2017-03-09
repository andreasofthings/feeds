#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from django.test import TestCase, Client
from rest_framework.test import APITestCase
from rest_framework import status


class ApiTest(APITestCase):
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
        "Site.yaml",
        "Feed_all.yaml",
    ]

    def setUp(self):
        """
        Set up environment to test the API
        """
        # self.client = Client()
        pass

    def test_website_anonymous(self):
        """
        request subscription, expect a list of all feeds in json

        .. todo:: This ain't done yet.
        """
        response = self.client.get('/feedapi/websites/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_feeds_anonymous(self):
        """
        request subscription, expect a list of all feeds in json

        .. todo:: This ain't done yet.
        """
        response = self.client.get('/feedapi/feeds/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
