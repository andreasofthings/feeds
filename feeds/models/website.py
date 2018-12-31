#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Feed-Aggregator models.
=======================

Stores as much as possible coming out of the feed.

.. moduleauthor:: Andreas Neumeier <andreas@neumeier.org>
"""

from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.urls import reverse

from ..managers import WebSiteManager

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class WebSite(models.Model):
    # website_url = models.URLField(
    #    unique=True,
    #    help_text=_("URL of the Website.")
    # )
    @property
    def website_url(self):
        from urllib.parse import urlunparse
        return urlunparse(
            self.scheme,
            self.netloc,
            self.path,
            self.params,
            self.query,
            self.fragment
        )
    """URL of the `Site`."""

    name = models.CharField(max_length=128)
    """Name of the website."""

    SCHEMES = (
        ('http', 'HTTP'),
        ('https', 'HTTPS'),
    )
    scheme = models.CharField(
        max_length=5,
        choices=SCHEMES,
        default='https',
    )
    netloc = models.CharField(max_length=512)
    path = models.CharField(max_length=512, default='/')
    params = models.CharField(max_length=256, blank=True, null=True)
    query = models.CharField(max_length=256, blank=True, null=True)
    fragment = models.CharField(max_length=256, blank=True, null=True)

    slug = models.SlugField(null=True)
    """Human readble URL component"""

    commercial = models.BooleanField(default=True)
    """Indicate, whether this is a commercial site."""

    objects = WebSiteManager()
    """
    Overwrite the inherited manager
    with the custom :mod:`feeds.models.WebSiteManager`
    """

    class Meta:
        """
        Django Meta.
        """
        app_label = "feeds"
        ordering = ('netloc',)
        verbose_name = _('website')
        verbose_name_plural = _('websites')
        unique_together = ('netloc', 'path')

    def save(self, *args, **kwargs):
        """
        Since 'slug' is not a required field for userinput,
        set it before saving.

        .. todo::
            This is a bit of magic, that should rather not happen.
            It strips http:// https:// and www, if present.
        """
        if not self.slug:
            def remove_prefix(s, prefix):
                return s[len(prefix):] if s.startswith(prefix) else s
            slug = remove_prefix(slugify(self.website_url), "https")
            slug = remove_prefix(slugify(self.website_url), "http")
            slug = remove_prefix(slugify(self.website_url), "www")
            self.slug = slug
        if not self.name:
            self.name = self.slug
        return super(WebSite, self).save(*args, **kwargs)

    def __str__(self):
        """
        String representation of :Site:
        """
        return u"%s" % (self.name)

    def get_absolute_url(self):
        """
        Absolute URL for this object.

        .. todo:: should use 'slug' instead of 'id'
        """
        return reverse('planet:website-detail', args=[str(self.id)])

    def feedcount(self):
        """
        return count of all feeds for this :WebSite:.
        """
        return self.feeds.count()

    def natural_key(self):
        return (self.slug,)
