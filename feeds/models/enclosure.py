#! /usr/bin/env python3.6
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Feed-Aggregator models.
=======================

Stores as much as possible coming out of the feed.

.. moduleauthor:: Andreas Neumeier <andreas@neumeier.org>
"""

import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from .post import Post

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Enclosure(models.Model):
    """
    potential enclosure of a :mod:`feeds.models.Post`
    """

    post = models.ForeignKey(
        Post,
        related_name="enclosure",
        on_delete=models.DO_NOTHING,
    )
    """reference to the post the enclosure belongs to."""

    href = models.URLField()
    """the url of the enclosed media file."""

    length = models.BigIntegerField()
    """length of the enclosed media file in byte."""

    enclosure_type = models.CharField(max_length=32)
    """type of the enclosed file, for example 'image/jpeg'."""

    class Meta:
        """
        Django Meta
        """
        app_label = "feeds"

    def __str__(self):
        """
        return type of object and containing post
        """
        return u'%s [for %s]' % (self.enclosure_type, self.post)
