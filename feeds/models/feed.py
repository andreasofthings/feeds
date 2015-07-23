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
import datetime
import calendar
from collections import Counter

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from .. import USER_AGENT
from .. import FEED_OK, FEED_SAME, FEED_ERRPARSE, FEED_ERRHTTP, FEED_ERREXC
from ..managers import FeedManager
from ..feedexceptions import FeedErrorHTTP, FeedErrorParse, FeedSame
from .site import Site
from .category import Category
from .post import Post

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

    def _entry_guid(self, entry):
        """
        Get an individual guid for an entry
        """
        guid = ""

        if entry.link:
            guid = entry.link
        elif entry.title:
            guid = entry.title

        return entry.get('id', guid)

    def _guids(self, entries):
        guids = []
        for entry in entries:
            guids.append(self._entry_guid(entry))
        return guids

    def _postdict(self, uids):
        """
        fetch posts that we have on file already and return a dictionary
        with all uids/posts as key/value pairs.
        """
        all_posts = Post.objects.filter(feed=self)
        postdict = dict(
            [(post.guid, post) for post in all_posts.filter(
                guid__in=uids
            )]
        )
        return postdict

    def update(self, parsed):
        """
        Update `feed` with values from `parsed`
        """
        self.etag = parsed.get('etag', '')
        self.pubdate = parsed.feed.get('pubDate', '')
        self.last_modified = datetime.datetime.utcfromtimestamp(
            calendar.timegm(
                parsed.feed.get('updated_parsed', self.pubdate)
            )
        )
        self.title = parsed.feed.get('title', '')[0:254]
        self.tagline = parsed.feed.get('subtitle', '')
        self.link = parsed.feed.get('link', '')
        self.language = parsed.feed.get('language', '')
        self.copyright = parsed.feed.get('copyright', '')
        self.author = parsed.feed.get('author', '')
        self.webmaster = parsed.feed.get('webmaster', '')

    def parse(self):
        try:
            fpf = feedparser.parse(
                self.feed_url,
                agent=USER_AGENT,
                etag=self.etag
            )
        except Exception as e:
            logger.error(
                'Feedparser Error: (%s) cannot be parsed: %s',
                self.feed_url,
                str(e)
            )
            raise e

        if 'status' not in fpf or fpf.status >= 400:
            raise FeedErrorHTTP

        if 'bozo' in fpf and fpf.bozo == 1:
            logger.error(
                "[%d] !BOZO! Feed is not well formed: %s",
                self.id,
                self.name
            )
            raise FeedErrorParse

        if fpf.status == 304:
            logger.debug(
                "[%d] Feed did not change: %s",
                self.id,
                self.name
            )
            raise FeedSame

        logger.debug("-- end --")
        return fpf

    def refresh(self):
        """
        Refresh feed from `self.link`
        """
        logger.debug("-- start --")
        try:
            parsed = self.parse()
        except FeedErrorHTTP as e:
            return FEED_ERRHTTP
        except FeedErrorParse as e:
            return FEED_ERRPARSE
        except FeedSame:
            return FEED_SAME
        self.update(parsed)
        guid_list = self._guids(parsed.entries)
        postdict = self.__postdict(guid_list)
        try:
            result = Counter(
                (
                    e, created = Entry.objects.from_feedparser(self.id, entry, postdict)
                    for
                    entry
                    in
                    parsed.entries
                )
            )
        except Exception as e:
            logger.debug("-- end (ERR) --")
            raise e
            return FEED_ERREXC

        logger.info("Feed '%s' returned %s", self.title, result)
        logger.debug("-- end --")
        return FEED_OK

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
