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
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save
from django.dispatch import receiver


# from ..managers import TagManager
import logging
logger = logging.getLogger(__name__)


class TagNameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(TagNameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()

class Tag(models.Model):
    """
    A tag.
    """

    # objects = TagManager()
    """
    Overwrite the inherited manager with the
    custom :mod:`feeds.models.TagManager`
    """

    name = TagNameField(
        _('name'),
        max_length=50,
        unique=True,
        db_index=True
    )
    """The name of the Tag."""

    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
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

    def __str__(self):
        """
        Human readable representation of the object.
        """
        return self.name

    def natural_key(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('planet:tag-detail', args=[str(self.slug),])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Tag, self).save(*args, **kwargs)
