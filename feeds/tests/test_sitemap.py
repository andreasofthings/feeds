#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from django.test import TestCase, Client


class ViewsAnonymousTest(TestCase):
    """
    """
    def setUp(self):
        self.client = Client()

    def test_sitemap(self):
        result = self.client.get('/feeds/sitemap.xml')
        self.assertEqual(result.status_code, 200)
