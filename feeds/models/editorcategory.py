# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
EditorCategory.

Maintain categories for websites.
"""

from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

import logging

from ..managers import EditorCategoryManager

from django.db.models.signals import pre_save
from django.dispatch import receiver


logger = logging.getLogger(__name__)


class EditorCategory(models.Model):
    """
    EditorCategory Class.

    Category model to be used for categorization of `WebSite`.
    Categories are high level constructs to be used for grouping
    and organizing content, thus creating a site's table of contents.
    """

    objects = EditorCategoryManager()

    name = models.CharField(
        max_length=200,
        unique=True,
        help_text=_('Short descriptive name for this category.'),
    )

    slug = models.SlugField(
        max_length=255,
        db_index=True,
        unique=True,
        help_text=_('Short descriptive unique name for use in urls.'),
    )

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        """Meta config for `EditorCategory`."""

        app_label = "feeds"
        ordering = ('name',)
        unique_together = ('name', 'slug', )
        verbose_name = 'editor_category'
        verbose_name_plural = 'editor_categories'

    @property
    def children(self):
        """Return all children for node."""
        return self.category_set.all().order_by('name')

    @classmethod
    def create(cls, name, slug=None):
        """Override create method."""
        cat = cls(name=name)
        if not slug or slug == "":
            cat.slug = slugify(cat.name)
        cat.save()
        logger.debug(
            "Category name, slug: %s, %s" % (cat.name, cat.slug)
        )
        return cat

    def save(self, *args, **kwargs):
        """Override `save` to automate slug-creation."""
        if not self.slug or self.slug == "":
            self.slug = slugify(self.name)
        super(EditorCategory, self).save(*args, **kwargs)

    def __str__(self):
        """Human readable representation of the object."""
        return u''.join(self.name)

    def natural_key(self):
        """Natural Key for serialization."""
        return u''.join(self.slug)

    def get_absolute_url(self):
        """Get absolute url for views."""
        return reverse(
            'planet:editorcategory-detail',
            args=[str(self.slug)]
        )


@receiver(pre_save, sender=EditorCategory)
def make_slug(sender, instance, *args, **kwargs):
    """Create `slug` on signal."""
    if not instance.slug:
        instance.slug = slugify(instance.name)
