#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from django.test import TestCase
from feeds.models import Tag


class TestPostModel(TestCase):
    """
    Tests for Tag model.

    Derived from pythons unittest.TestCase:
    https://docs.python.org/3/library/unittest.html#unittest.TestCase
    """

    fixtures = [
        'Tag.yaml',
    ]

    def setUp(self):
        pass

    def test_tag_instance(self):
        """
        Test tag instance.

        Test whether a Post can be instanciated.
        """
        t = Tag.objects.get(pk=1)
        self.assertIsInstance(t, Tag)

    def test_tag_create(self):
        """
        Test tag instance.

        Test whether a Post can be instanciated.
        """
        t1 = Tag(name="1")
        t1.save()
        t2, c = Tag.objects.get_or_create(name="1")
        self.assertFalse(c)
        t3, c = Tag.objects.get_or_create(name="2")
        self.assertTrue(c)
        self.assertIsInstance(t1, Tag)
        self.assertIsInstance(t2, Tag)
        self.assertIsInstance(t3, Tag)

    def tearDown(self):
        pass
