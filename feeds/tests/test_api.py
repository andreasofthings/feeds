#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from rest_framework import status
from rest_framework.test import APITestCase

import logging

log = logging.getLogger(__name__)


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
        "Users.yaml",
        "Options.yaml",
        "Site.yaml",
        "Feed_all.yaml",
        "Posts.yaml",
    ]

    def setUp(self):
        """
        Set up environment to test the API
        """
        # self.client = Client()
        pass

    def test_options_anonymous(self):
        """
        Return options list.

        .. todo:: Should actually not work and require authentication.
        .. input: None.
        .. expect:: 404 Not Found
        """
        log.debug("test_options_anonymous")
        response = self.client.get('/feeds/api/options/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_options_authenticated(self):
        """
        Request options for an authenticated user.
        """
        # Make an authenticated request to the view...
        self.client.login(username="andreas", password="password")
        response = self.client.get('/feeds/api/options/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_website_anonymous(self):
        """
        request subscription, expect a list of all feeds in json

        .. todo:: This ain't done yet.
        """
        response = self.client.get('/feeds/api/websites/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_feeds_anonymous(self):
        """
        1. request /feeds/api/feeds, expect a list of all feeds in json.
        2. request /feeds/api/feeds/1, expect details for feed 1 in json.

        .. todo:: This ain't done yet.
        """
        response = self.client.get('/feeds/api/feeds/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/feeds/api/feeds/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_posts_anonymous(self):
        """
        1. request /feeds/api/posts, expect a list of all posts in json.
        2. request /feeds/api/posts/1, expect details for post 1 in json.

        .. todo:: This ain't done yet.
        """
        response = self.client.get('/feeds/api/posts/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/feeds/api/posts/2/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subscription_anonymous(self):
        """
        request subscription, expect a list of all feeds in json

        .. todo:: Should require authentication.
        """
        response = self.client.get('/feeds/api/subscriptions/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        """
        Clean up environment after model tests
        """
        pass
