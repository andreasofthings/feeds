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
import feedparser

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from ..managers import FeedManager
from .site import Site
from .category import Category

logger = logging.getLogger(__name__)


class Feed(models.Model):
    """
    Model that contains information about any feed, including
    - metadata for processing
    - results from social updates
    - calculated values
    """
    site = models.ForeignKey(
        Site,
        blank=True,
        null=True
    )
    feed_url = models.URLField(
        _('feed url'),
        unique=True
    )
    name = models.CharField(
        _('name'),
        max_length=100,
        null=True,
        blank=True
    )
    short_name = models.CharField(
        _('short_name'),
        max_length=50,
        null=True,
        blank=True
    )
    slug = models.SlugField(
        max_length=255,
        db_index=True,
        unique=True,
        null=True,
        blank=True,
        help_text='Short descriptive unique name for use in urls.',
    )
    is_active = models.BooleanField(
        _('is active'),
        default=True,
        help_text=_('If disabled, this feed will not be further updated.')
    )
    category = models.ManyToManyField(
        Category,
        related_name="category_feeds",
        blank=True,
    )
    has_no_guid = models.BooleanField(
        _('has no guid'),
        default=False,
        help_text=_("""
                    This feed doesn't have a proper guid.
                    Use something else instead.
                    """
                    )
    )

    # <rss><channel>
    # mandatory fields
    title = models.CharField(
        _('title'),
        max_length=200,
        blank=True
    )
    link = models.URLField(
        _('link'),
        blank=True
    )
    tagline = models.TextField(
        _('description'),
        blank=True,
        help_text=_('Phrase or sentence describing the channel.'),
    )

    # <rss><channel>
    # optional fields
    language = models.CharField(
        _('language'),
        blank=True,
        max_length=8,
    )
    copyright = models.CharField(
        _('copyright'),
        blank=True,
        max_length=64,
    )

    author = models.CharField(
        _('managingEditor'),
        blank=True,
        max_length=64,
    )

    webmaster = models.CharField(
        _('webmaster'),
        blank=True,
        max_length=64,
    )

    pubDate = models.DateTimeField(_('pubDate'), null=True, blank=True)
    last_modified = models.DateTimeField(
        _('lastBuildDate'),
        null=True,
        blank=True
    )

    # Category
    category = models.ManyToManyField(
        Category,
        related_name="category_feeds",
        blank=True,
    )
    # generator
    # docs
    # cloud

    ttl = models.IntegerField(
        _("""
          TTL stands for time to live.
          It's a number of minutes that indicates how long a
          channel can be cached before refreshing from the source.
          """
          ),
        default=60
    )

    image_title = models.CharField(
        _('image_title'),
        max_length=200,
        blank=True
    )

    image_link = models.URLField(
        _('image_link'),
        blank=True
    )

    image_url = models.URLField(
        _('image_url'),
        blank=True
    )

    # rating
    # textInput
    # skipHours
    # skipDay

    # http://feedparser.org/docs/http-etag.html
    etag = models.CharField(
        _('etag'),
        max_length=50,
        blank=True
    )

    last_checked = models.DateTimeField(
        _('last checked'),
        null=True,
        blank=True,
        auto_now=True
    )

    check_interval = models.IntegerField(
        _('Interval in Minutes between checks.'),
        default=5
    )

    ignore_ca = models.BooleanField(
        _('Indicates whether CA for this certificate should be ignored'),
        default=True
    )
    """Do (not) verify certificate authenticity."""

    announce_posts = models.BooleanField(default=False)
    """Whether to socially announce new articles posts"""

    objects = FeedManager()

    def save(self, *args, **kwargs):
        """
        Need to update items before saving?

        .. todo: This is for sure flaky.
        """
        f = feedparser.parse(self.feed_url)
        if not self.name and 'title' in f.feed:
            self.name = f.feed.title
        if not self.short_name and 'title' in f.feed:
            self.short_name = f.feed.title[:50]
        if not self.link and hasattr(f.feed, 'link'):
            self.link = f.feed.link
        if hasattr(f.feed, 'language'):
            self.language = f.feed.language[:8]
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Feed, self).save(*args, **kwargs)

    class Meta:
        """
        Metadata for Feed Model.
        Permissions contain:
        :fields:
           can_refresh_feed: User with this credential
           is allowed to refresh a feed.
        """
        verbose_name = _('feed')
        verbose_name_plural = _('feeds')
        ordering = ('name', 'feed_url',)
        permissions = (
            ("can_refresh_feed", "Can refresh feed"),
        )

    def __unicode__(self):
        return u'%s' % (self.name)

    def natural_key(self):
        """
        Return a natural_key for this Feed.
        """
        return (self.name, ) + self.category.natural_key()
    natural_key.dependency = ['feeds.Category', ]

    @models.permalink
    def get_absolute_url(self):
        return ('planet:feed-view', [str(self.id)])

    def post_count(self):
        """
        Return the number of posts in this feed.
        """
        return self.posts.count()

    def subscriber_count(self):
        """
        Return the number of subscribers for this feed.
        """
        return self.feed_subscription.count()
