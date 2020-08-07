#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Test subscriptions.

Subscriptions are realized in :py:mod:`feeds.models.Subscriptions`
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class TestSubscriptions(TestCase):
    """

    .. codeauthor:: Andreas Neumeier <andreas@neumeier.org>
    """

    fixtures = [
        'WebSite.yaml',
        'Feed_all.yaml',
        'Users.yaml',
        'Options.yaml',
        'Subscriptions.yaml',
    ]

    def setUp(self):
        """
        Set up enivironment to test models.
        """
        pass

    def test_getSubscription(self):
        """
        Verify the subscriptions function for individual users.

        """
        from feeds.models.subscription import Subscription
        from feeds.models.options import Options
        options = Options(user=User.objects.get(pk=1))
        self.assertFalse(Subscription.objects.feeds(options).exists())

    def tearDown(self):
        pass
