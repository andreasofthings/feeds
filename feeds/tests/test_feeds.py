#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

from django.test import TestCase
from django.core.urlresolvers import reverse


class TestFeedCredentials(TestCase):
    """
    Test those aspects of :py:mod:`feeds.views` related to
    py:mod:`feeds.models.Feed`, that require proper cedentials.
    """

    username = ""
    password = ""

    def test_feed_add_post(self):
        """
        go to feed-add
        add a post.
        """
        result = self.client.post(reverse('planet:feed-add'))
        self.client.login(username=self.username, password=self.password)
        self.assertEqual(result.status_code, 302)
