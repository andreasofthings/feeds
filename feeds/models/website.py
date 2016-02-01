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

from ..managers import WebSiteManager

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class WebSite(models.Model):
    url = models.URLField(
        unique=True,
        help_text=_("URL of the Website.")
    )
    """URL of the `Site`."""

    slug = models.SlugField(null=True)
    """Human readble URL component"""

    objects = WebSiteManager()
    """
    Overwrite the inherited manager
    with the custom :mod:`feeds.models.WebSiteManager`
    """

    def save(self, *args, **kwargs):
        """
        Since 'slug' is not a required field for userinput,
        set it before saving.
        """
        if not self.slug:
            self.slug = slugify(self.url)
        return super(WebSite, self).save(*args, **kwargs)

    def __str__(self):
        """
        String representation of :Site:
        """
        return u"%s" % (self.url)

    @models.permalink
    def get_absolute_url(self):
        """
        Absolute URL for this object.

        ToDo: should use 'slug' instead of 'id'
        """
        return ('planet:site-view', [str(self.id)])

    def feeds(self):
        """
        return all feeds for this :Site:.
        """
        return self.feed_set.all()

    def natural_key(self):
        return (self.slug,)
