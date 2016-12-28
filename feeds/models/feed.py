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

import sys
import time
import logging
import datetime
import traceback

from collections import Counter

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.utils import timezone

import feedparser
from feedparser import CharacterEncodingOverride

from .website import WebSite
from category.models import Category

from .. import USER_AGENT
from .. import FEED_OK, FEED_SAME, FEED_ERRPARSE, FEED_ERRHTTP, FEED_ERREXC
from .. import ENTRY_NEW, ENTRY_UPDATED, ENTRY_SAME
from ..managers import FeedManager
from ..feedexceptions import FeedErrorHTTP, FeedErrorParse, FeedSame

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Feed(models.Model):
    """
Model that contains information about any feed, including:

    - metadata for processing
    - results from social updates
    - calculated values

Coming from `feedparser`:

    - bozo
    - bozo_exception
    - encoding
    - etag
    - feed.author
    - feed.author_detail
    - feed.cloud
    - feed.contributors
    - feed.docs
    - feed.errorreportsto
    - feed.generator
    - feed.generator_detail
    - feed.icon
    - feed.id
    - feed.image
    - feed.info
    - feed.info_detail
    - feed.language
    - feed.license
    - feed.link
    - feed.links
    - feed.logo
    - feed.published
    - feed.published_parsed
    - feed.publisher
    - feed.publisher_detail
    - feed.rights
    - feed.rights_detail
    - feed.subtitle
    - feed.subtitle_detail
    - feed.tags
    - feed.textinput
    - feed.title
    - feed.title_detail
    - feed.ttl
    - feed.updated
    - feed.updated_parsed
    - headers
    - href
    - modified
    - namespaces
    - status
    - version
    """
    website = models.ForeignKey(
        WebSite,
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
    errors = models.IntegerField(
        _('Has errors'),
        default=0,
        help_text=_("""
                    Remember errors for a feed, and don't try again if a
                    threshold is met
                    """)
    )
    category = models.ManyToManyField(
        Category,
        related_name="category_feeds",
        blank=True,
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
    logo = models.URLField(
        _('logo'),
        blank=True,
        null=True,
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
        """
        if self.errors > getattr(settings, 'FEEDS_ERROR_THRESHOLD', 3):
            self.is_active = False
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
            ("can_refresh_feed", _("Can refresh feed")),
            ("can_subscribe_feed", _("Can subscribe to feed")),
            ("can_backup_feed", _("Can backup feeds")),
        )

    def __str__(self):
        return u'%s' % (self.name)

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
        return dict(
            [(post.guid, post) for post in self.posts.filter(
                guid__in=uids
            )]
        )

    def from_feedparser(self, entry, postdict):
        """
        Receive Entry, postdict
        ..arguments:
            entry: actual Entry
            postdict: ?
        entry has these keys:
        - 'summary_detail'
        - 'published'
        - 'published_parsed'
        - 'links'
        - 'title'
        - 'tags'
        - 'summary'
        - 'content'
        - 'guidislink'
        - 'title_detail'
        - 'link'
        - 'id'

        returnvalue::
            Either ENTRY_NEW, ENTRY_UPDATE
        """
        result = ENTRY_SAME

        now = timezone.now()
        created_parsed = entry.get('created_parsed', now)
        published_parsed = entry.get('published_parsed', created_parsed)

        if isinstance(published_parsed, time.struct_time):
            published_parsed = \
                datetime.datetime.fromtimestamp(
                    time.mktime(published_parsed)
                )

        if timezone.is_naive(published_parsed):
            published_parsed = \
                timezone.make_aware(published_parsed)

        if timezone.is_naive(published_parsed):
            logger.error("WHAT THE FUCK, DJANGO.TOOLS")

        p, created = self.posts.from_feedparser(
            feed=self,
            title=entry.title,
            guid=self._entry_guid(entry),
            published=published_parsed,
        )
        if created:
            result = ENTRY_NEW
            p.save()
            logger.debug(
                "'%s' is a new entry for feed %s (%s)",
                entry.title,
                self.id,
                p.id
            )
        p.content = entry.get('content', '')
        """.. todo:: get other content instead."""
        p.author = entry.get('author', '')
        p.author_email = entry.get('author_email', '')
        p.summary = entry.get('summary', '')

        if 'category' in entry and len(entry.category) > 0:
            for category in entry.category:
                cat, created = p.categories.get_or_create(
                    name=category
                )

        if 'enclosures' in entry and len(entry.enclosures) > 0:
            for enclosure in entry.enclosures:
                e, created = p.enclosure.get_or_create(
                    href=enclosure['href'],
                    length=enclosure['length'],
                    enclosure_type=enclosure['type'],
                )
                if created:
                    e.save()

        p.save()
        logger.debug(
            """Saved '%s', new entry for feed '%s' (FeedID: %s, PostID %s)""",
            p.title,
            self.title,
            self.id,
            p.id
        )

        if hasattr(entry, 'link'):
            if p.link is not entry.link:
                p.link = entry.link
                if not created:
                    result = ENTRY_UPDATED

        logger.debug("stop: entry")
        p.save()
        return result

    def update(self, parsed):
        """
        Update `feed` with values from `parsed`
        """
        if not self.name and 'title' in parsed.feed:
            self.name = parsed.feed.title[:100]
        if not self.short_name and 'title' in parsed.feed:
            self.short_name = parsed.feed.title[:50]
        if not self.link and hasattr(parsed.feed, 'link'):
            self.link = parsed.feed.link
        if hasattr(parsed.feed, 'language'):
            self.language = parsed.feed.language[:7]
        if hasattr(parsed.feed, 'image'):
            if hasattr(parsed.feed.image, 'url'):
                self.image_url = parsed.feed.image.url
        if not self.slug:
            self.slug = slugify(self.name)

        self.etag = parsed.get('etag', '')
        self.pubdate = parsed.feed.get('pubDate', '')

        """
        .. todo:: Same as above. A trainwreck.
        """
        try:
            updated = parsed.feed.get('updated', timezone.now())
            updated_parsed = parsed.feed.get('updated_parsed', updated)

            if isinstance(updated_parsed, time.struct_time):
                updated_parsed = \
                    datetime.datetime.fromtimestamp(
                        time.mktime(updated_parsed)
                    )

            if timezone.is_naive(updated_parsed):
                updated_parsed = \
                    timezone.make_aware(updated_parsed)

            self.last_modified = updated_parsed

        except ValueError as e:
            """
            .. todo:: Proper Exceptionhandling
            """
            logger.error(e)
            logger.error(parsed.feed.updated)

        self.title = parsed.feed.get('title', '')[0:200]
        self.tagline = parsed.feed.get('subtitle', '')[:64]
        self.copyright = parsed.feed.get('copyright', '')[:64]
        self.author = parsed.feed.get('author', '')[:64]
        self.logo = parsed.feed.get('logo', None)
        self.webmaster = parsed.feed.get('webmaster', '')[:64]

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
                "[%d] !BOZO! Feed '%s' is not well formed: %s",
                self.id,
                self.name,
                fpf.bozo_exception
            )
            if type(fpf.bozo_exception) is CharacterEncodingOverride:
                logger.error("CharacterEncodingOverride, trying to continue")
                pass
            else:
                raise FeedErrorParse(fpf.bozo_exception)

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
        Refresh feed.
        """
        logger.debug("-- start --")
        now = timezone.now()
        fiveminutesago = now - datetime.timedelta(seconds=300)

        if self.last_checked is not None:
            if self.last_checked > fiveminutesago:
                logger.error(
                    "tried feed %s too quick. aborting. (%s, %s, %s)",
                    self.feed_url,
                    self.last_checked,
                    self.last_checked + datetime.timedelta(seconds=300),
                    now
                )
                return FEED_SAME

        try:
            parsed = self.parse()
        except FeedErrorHTTP as e:
            self.errors = self.errors+1
            self.save()  # touch timestamp
            return FEED_ERRHTTP
        except FeedErrorParse as e:
            logger.error("Feed %s raised FeedErrorParse: %s", self.name, e)
            self.errors = self.errors+1
            self.save()  # touch timestamp
            return FEED_ERRPARSE
        except FeedSame:
            self.save()  # touch timestamp
            return FEED_SAME

        try:
            self.update(parsed)
        finally:
            """
            Make sure timestamp is touched
            """
            self.save()

        guid_list = self._guids(parsed.entries)
        postdict = self._postdict(guid_list)
        try:
            result = Counter(
                (
                    self.from_feedparser(entry, postdict)
                    for
                    entry
                    in
                    parsed.entries
                )
            )
        except Exception as e:
            logger.debug("-- end (ERR) --")
            traceback.print_exc(file=sys.stdout)
            return FEED_ERREXC

        logger.debug("Feed '%s' returned %s", self.title, result)
        logger.debug("-- end --")
        self.errors = 0
        self.save()
        from django.contrib.sitemaps import ping_google
        ping_google(reverse("planet:sitemap"))
        return FEED_OK
