#! /usr/bin/env python2.7
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
from django.template.defaultfilters import slugify

from ..managers import TagManager

logger = logging.getLogger(__name__)


class Tag(models.Model):
    """
    A tag.
    """

    objects = TagManager()
    """
    Overwrite the inherited manager
    with the custom :mod:`feeds.models.TagManager`
    """

    name = models.CharField(
        _('name'),
        max_length=50,
        unique=True,
        db_index=True
    )
    """The name of the Tag."""

    relevant = models.BooleanField(default=False)
    """
    Indicates whether this Tag is relevant for further processing.
    It should be used to allow administrative intervention.
    """

    touched = models.DateTimeField(auto_now=True)
    """Keep track of when this Tag was last used."""

    @property
    def slug(self):
        return slugify(self.name)

    class Meta:
        """
        Django Meta.
        """
        ordering = ('name',)
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def posts(self):
        """
        return all feeds in this category
        """
        return self.tag_posts.all()

    def __unicode__(self):
        """
        Human readable representation of the object.
        """
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('planet:tag-view', [str(self.pk)])

    def natural_key(self):
        return (self.name,)
