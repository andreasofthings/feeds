#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Test the recursive opml import.
"""

from feeds.views import opmlImport
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

upload_file = 'feeds/tests/data/feedlyshort.opml'


class TaskOPML(TestCase):
    """
    Test OPML Import

    .. codeauthor:: Andreas Neumeier <andreas@neumeier.org>
    """

    username = "john"
    password = "password"

    def setUp(self):
        """
        Set up enivironment to test models
        """
        self.user = User.objects.create_user(
            self.username,
            'lennon@thebeatles.com',
            self.password
        )
        """Test user."""

        self.client = Client()
        """Test Client."""

    def test_opml_import(self):
        from xml.etree import ElementTree
        tree = ElementTree.parse(open(upload_file))
        result = opmlImport(tree)
        self.assertEqual(result, True)

    def test_opml_view(self):
        with open(upload_file) as fp:
            result = self.client.post(
                reverse('planet:opml'),
                {'opml': fp}
            )
            self.assertEqual(result.status_code, 302)

    def tearDown(self):
        pass
