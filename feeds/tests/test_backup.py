#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class BackupTest(TestCase):
    """
    Test whether all :py:mod:`feeds.views` are working.

    .. moduleauthor:: Andreas Neumeier <andreas@neumeier.org>
    """

    fixtures = [
        'Feed_all.yaml',
        'Categories.yaml',
    ]

    def setUp(self):
        """
        Set up environment.
        """

        self.client = Client()
        """Test Client."""

    def test_backup(self):
        """
        """
        result = self.client.get(reverse('planet:backup'))
        self.assertEqual(result.status_code, 200)
