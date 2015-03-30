#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Test the recursive opml import.
"""

from feeds.views import opml_import
from django.test import TestCase


class TaskOPML(TestCase):
    """
    Test OPML Import

    .. codeauthor:: Andreas Neumeier <andreas@neumeier.org>
    """

    def setUp(self):
        """
        Set up enivironment to test models.
        """
        pass

    def test_opml_import(self):
        from xml.etree import ElementTree
        tree = ElementTree.parse(open('feeds/tests/data/feedlyshort.opml'))
        result = opml_import(tree)
        self.assertEqual(result, True)

    def tearDown(self):
        pass
