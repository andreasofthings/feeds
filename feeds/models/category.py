#! /usr/bin/env python3.6
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

import logging

# from ..managers import CategoryManager


logger = logging.getLogger(__name__)


class Category(models.Model):
    """
    Category model.

    Model to be used for categorization of content. Categories are
    high level constructs to be used for grouping and organizing content,
    thus creating a site's table of contents.
    """
    # objects = CategoryManager()

    name = models.CharField(
        max_length=200,
        # unique=True,
        help_text=_('Short descriptive name for this category.'),
    )

    slug = models.SlugField(
        max_length=255,
        db_index=True,
#        unique=True,
        help_text='Short descriptive unique name for use in urls.',
    )

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        """
        Django Meta.
        """
        app_label = "feeds"
        ordering = ('name',)
        unique_together = ('name', 'slug', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    @property
    def children(self):
        return self.category_set.all().order_by('name')

    @classmethod
    def create(cls, name, slug=None):
        cat = cls(name=name)
        if not slug or slug == "":
            cat.slug = slugify(cat.name)
        cat.save()
        logger.debug("Category name, slug: %s, %s" % (cat.name, cat.slug))
        return cat

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == "":
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        """
        Human readable representation of the object.
        """
        return u''.join(self.name)

    def natural_key(self):
        return u''.join(self.slug)

    def get_absolute_url(self):
        return reverse('planet:category-detail', args=[str(self.slug)])
