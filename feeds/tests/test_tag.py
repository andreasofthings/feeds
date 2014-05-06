#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

from django.test import TestCase


class TagTest(TestCase):
    def test_tag(self):
        """
        Test a Tag
        """
        from feeds.models import Tag
        """Import the :py:mod:`feeds.models.Tag`-model."""
        t = Tag(name="tag")
        """Instanciate the model."""
        tagid = t.save()
        """Save the model and retrieve the pk/id."""
        self.assertNotEqual(tagid, 0)
        """Assert the pk/id is not 0."""
        self.assertEqual(str(t), "tag")
        """Assert the __str__ representation equals the tag-name."""
        # self.assertContains( t.get_absolute_url(), t.pk)
        """
        Assert the tag URL contains the tag.pk.

        .. todo:: self.assertContains won't work for what is being tested here.
        """
