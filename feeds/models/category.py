#! /usr/bin/env python3.6
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

import logging

from ..managers import CategoryManager 

logger = logging.getLogger(__name__)


class TagManager(models.Manager):
    """
    Manager for `Tag` objects.
    """

    def get_by_natural_key(self, slug):
        """
        get Tag by natural key, to allow serialization by key rather than `pk`
        """
        return self.get(slug=slug)


@python_2_unicode_compatible
class Tag(models.Model):
    """
    A tag.
    """

    objects = TagManager()
    """
    Overwrite the inherited manager with the
    custom :mod:`feeds.models.TagManager`
    """

    name = models.CharField(
        _('name'),
        max_length=50,
        unique=True,
        db_index=True
    )
    """The name of the Tag."""

    slug = models.SlugField(
        max_length=255,
        db_index=True,
        unique=True,
        help_text='Short descriptive unique name for use in urls.',
    )
    """
    The slug of the Tag.
    It can be used in any URL referencing this particular Tag.
    """

    relevant = models.BooleanField(default=False)
    """
    Indicates whether this Tag is relevant for further processing.
    It should be used to allow administrative intervention.
    """

    touched = models.DateTimeField(auto_now=True)
    """Keep track of when this Tag was last used."""

    content_type = models.ForeignKey(
        ContentType,
        null=True,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        """
        Django Meta.
        """
        app_label = "feeds"
        ordering = ('name',)
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    @classmethod
    def create(cls, name, slug=None):
        tag = cls(name=name)
        if not slug or slug == "":
            tag.slug = slugify(tag.name)
        tag.save()
        logger.debug("Tag name, slug: %s, %s" % (tag.name, tag.slug))
        return tag

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == "":
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        """
        Human readable representation of the object.
        """
        return u''.join(self.name)

    def natural_key(self):
        return u''.join(self.slug)

    def get_absolute_url(self):
        return ('planet:tag-view', [str(self.slug)])


@python_2_unicode_compatible
class Category(models.Model):
    """
    Category model to be used for categorization of content. Categories are
    high level constructs to be used for grouping and organizing content,
    thus creating a site's table of contents.
    """
    objects = CategoryManager()

    name = models.CharField(
        max_length=200,
        unique=True,
        help_text='Short descriptive name for this category.',
    )

    slug = models.SlugField(
        max_length=255,
        db_index=True,
        unique=True,
        help_text='Short descriptive unique name for use in urls.',
    )

    parent = models.ForeignKey('self', null=True, blank=True,
    on_delete=models.DO_NOTHING,)

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
