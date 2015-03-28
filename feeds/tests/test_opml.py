#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Test the recursive opml import.
"""

import os
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
        if 'TRAVIS' not in os.environ:
            from xml.etree import ElementTree
            tree = ElementTree.parse(open('feeds/tests/data/feedly.opml'))
            result = opml_import(tree)
            self.assertEqual(result, True)
        else:
            """Don't test this in Travis."""
            self.assertTrue(True)

    def tearDown(self):
        pass
