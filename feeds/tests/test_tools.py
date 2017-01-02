#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Test all tools
"""

from django.test import TestCase


class TestTools(TestCase):
    """

    .. codeauthor:: Andreas Neumeier <andreas@neumeier.org>
    """

    def setUp(self):
        """
        Set up enivironment to test models.
        """
        pass

    def test_getFeedFromSite(self):
        from feeds.tools import getFeedsFromSite
        result = getFeedsFromSite("https://nomorecubes.net")
        self.assertEqual(type(result), type([]))

    def tearDown(self):
        pass
