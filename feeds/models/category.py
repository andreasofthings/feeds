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

from ..managers import CategoryManager

logger = logging.getLogger(__name__)


class Category(models.Model):
    """
    Category
    ========

    Category model to be used for categorization of content. Categories are
    high level constructs to be used for grouping and organizing content,
    thus creating a site's table of contents.
    """

    objects = CategoryManager()
    """
    References the default ModelManager,
    here :py:mod:`feeds.models.CategoryManager`.
    """

    name = models.CharField(
        max_length=200,
        help_text=_('Short descriptive name for this category.'),
        unique=True,
    )

    @property
    def slug(self):
        return slugify(self.name)

    def __unicode__(self):
        return self.name

    class Meta:
        """
        Django Meta.
        """
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    @property
    def feeds(self):
        """
        Return all :py:mod:`feeds.models.Feed`s in this Category.
        """
        return self.category_feeds.all()

    @property
    def posts(self):
        """
        ToDo:
        Return all :py:mod:`feeds.models.Post`s for
        :py:mod:`feeds.models.Feed`s in this category.
        """
        result = self.category_feeds.posts()
        return result

    def natural_key(self):
        return (self.name, )

    @models.permalink
    def get_absolute_url(self):
        return ('planet:category-view', [str(self.pk)])
