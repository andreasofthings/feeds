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

from ..managers import PostReadCountManager
from .feed import Feed
from .post import Post

logger = logging.getLogger(__name__)


class FeedPostCount(models.Model):
    feed = models.ForeignKey(
        Feed,
        verbose_name=_('feed'),
        null=False,
        blank=False,
        on_delete=models.DO_NOTHING,
    )
    entry_new = models.IntegerField(default=0)
    entry_updated = models.IntegerField(default=0)
    entry_same = models.IntegerField(default=0)
    entry_err = models.IntegerField(default=0)
    created = models.IntegerField()

    class Meta:
        """
        Django Meta
        """
        app_label = "feeds"

    @models.permalink
    def get_absolute_url(self):
        return ('planet:feed-post-count-view', [str(self.id)])

    def __unicode__(self):
        return u'%s [%s]' % (self.feed, self.entry_new)

    def save(self, *args, **kwargs):
        """
        # Now (Epoch time), rounded to full seconds (hence the cast)
        # subtract the modulo of 3600, result is the floor hour
        """
        import time
        this_hour = int(time.time()) - int(time.time()) % 3600
        self.created = int(this_hour)
        super(FeedPostCount, self).save(*args, **kwargs)


class FeedEntryStats(models.Model):
    """
    These are stats for one particulat :py:mod:`feeds.models.Feed` in the list.
    """
    feed = models.ForeignKey(Feed, on_delete=models.DO_NOTHING,)
    collected = models.DateTimeField(auto_now_add=True)
    entry_new = models.IntegerField(default=0)
    entry_same = models.IntegerField(default=0)
    entry_updated = models.IntegerField(default=0)
    entry_err = models.IntegerField(default=0)

    class Meta:
        """
        Django Meta
        """
        app_label = "feeds"


class FeedStats(models.Model):
    """
    These are stats for all :py:mod:`feeds.models.Feed` in the list.
    """
    collected = models.DateTimeField(auto_now_add=True)
    feed_ok = models.IntegerField(default=0)
    feed_same = models.IntegerField(default=0)
    feed_errparse = models.IntegerField(default=0)
    feed_errhttp = models.IntegerField(default=0)
    feed_errexc = models.IntegerField(default=0)

    class Meta:
        """
        Django Meta
        """
        app_label = "feeds"


class PostReadCount(models.Model):
    """
    This is not a real counter, more a log.

    Need to count and cleanup elsewhere.
    """
    objects = PostReadCountManager()
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING,)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Django Meta
        """
        app_label = "feeds"
