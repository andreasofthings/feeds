#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Feed-Aggregator models.
=======================

Stores as much as possible coming out of the feed.

.. moduleauthor:: Andreas Neumeier <andreas@neumeier.org>
"""

from __future__ import unicode_literals

import time
import logging
import datetime
import sys
import traceback

from collections import Counter

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone

import feedparser

from .website import WebSite
from .category import Category

from .. import USER_AGENT
from .. import FEED_OK, FEED_SAME, FEED_ERRPARSE, FEED_ERRHTTP, FEED_ERREXC
from .. import ENTRY_NEW, ENTRY_UPDATED, ENTRY_SAME
from ..managers import FeedManager
from ..exceptions import FeedsBaseException, FeedsHTTPError
from ..exceptions import FeedsParseError, FeedsSameError

logger = logging.getLogger(__name__)


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
        related_name="feeds",
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
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
        blank=True,
        max_length=512
    )

    # rating
    # textInput
    # skipHours
    # skipDay

    # http://feedparser.org/docs/http-etag.html
    etag = models.CharField(
        _('etag'),
        max_length=256,
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
        Save.

        Override default save method to enforce failure count update.
        """
        if self.errors > getattr(settings, 'FEEDS_ERROR_THRESHOLD', 3):
            self.is_active = False
        return super().save(*args, **kwargs)

    class Meta:
        """
        Metadata for Feed Model.

        Permissions contain:
        :fields:
           can_refresh_feed: User with this credential
           is allowed to refresh a feed.
        """

        app_label = "feeds"
        verbose_name = _('feed')
        verbose_name_plural = _('feeds')
        ordering = ('name', 'feed_url',)
        permissions = (
            ("can_refresh_feed", _("Can refresh feed")),
            ("can_subscribe_feed", _("Can subscribe to feed")),
            ("can_backup_feed", _("Can backup feeds")),
        )

    def __str__(self):
        """
        Representation.

        Give a readable representation for this `Feed`.
        """
        return u'%s' % (self.name)

    def post_count(self):
        """
        Count Posts.

        Return the number of posts in this feed.
        """
        return self.posts.count()

    def subscriber_count(self):
        """
        Count Subscribers.

        Return the number of subscribers for this feed.
        """
        return self.feed_subscription.count()

    def get_absolute_url(self):
        """
        Absolute URL for this object.

        .. todo:: should use 'slug' instead of 'id'
        """
        return reverse('planet:feed-detail', args=[str(self.id)])

    def _entry_guid(self, entry):
        """
        Get GUID.

        Try to find a valid GUID in an `entry`.

        Args:
            entry (Feedparser.EntryDict): A Feedparser representation
              of a Feed Entry.

        Returns:
            str: An GUID.

        """
        guid = ""

        guidislink = entry.get('guidislink', False)

        if entry.link and guidislink:
            return entry.link
        elif entry.title:
            guid = entry.title

        return entry.get('id', guid)

    def _guids(self, entries):
        """
        List GUIDs.

        Build a list of `guids` from a list of `entry`.

        Args:
          entries (list): A list of `entries`, as coming from `feedparser`.

        """

        guids = []
        for entry in entries:
            guids.append(self._entry_guid(entry))
        return guids

    def _postdict(self, uids):
        """
        List `uids`.

        Fetch posts that we have on file already and return a dictionary
        with all uids/posts as key/value pairs.

        Args:
            uids (list): List of UIDs


        Returns:
            dict: all queried posts with their UID as a key.

        Raises:
            Exception: description

        """

        return dict(
            [(post.guid, post) for post in self.posts.filter(
                guid__in=uids
            )]
        )

    def fromFeedparser(self, entry, postdict):
        """
        Create Posts from `feedparser`.

        Args:

            entry (dict):
            postdict (dict):


        entry can have these keys:
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

        if self._entry_guid(entry) in postdict.keys():
            logger.debug("update: %s", entry.title)
            post = self.posts.get(guid__exact=self._entry_guid(entry))
        else:
            logger.debug("insert: %s", entry.title)
            post, created = self.posts.fromFeedparser(
                feed=self,
                entry=entry,
                guid=self._entry_guid(entry),
                # published=published_parsed,
                )
            if created:
                result = ENTRY_NEW
                logger.debug(
                    "'%s' is a new entry for feed %s (%s)",
                    entry.title,
                    self.id,
                    post.id
                )

        if 'enclosures' in entry and entry.enclosures:
            for enclosure in entry.enclosures:
                encl, created = post.enclosure.get_or_create(
                    href=enclosure.get('href', '#'),
                    length=enclosure.get('length', 0),
                    enclosure_type=enclosure.get('type', ''),
                )

        logger.debug(
            """Saved '%s', new entry for feed '%s' (FeedID: %s, PostID %s)""",
            post.title,
            self.title,
            self.id,
            post.id
        )

        logger.debug("stop: entry")
        return result

    def update(self, parsed):
        """
        Feed.update.

        Update `feed` with values retrieved from `feedparser` through `parsed`.
        """
        if not self.name:
            self.name = parsed.feed.get('title', self.name)
        if not self.short_name:
            self.short_name = parsed.feed.get('title', self.name)[:50]
        if not self.slug:
            logger.error("Feed %s has no slug yet.", self.name)
            self.slug = slugify(self.name)
        if hasattr(parsed.feed, 'image'):
            if hasattr(parsed.feed.image, 'url'):
                self.image_url = parsed.feed.image.url

        updated = parsed.feed.get("updated_parsed", None)
        if updated:
            timestamp = time.mktime(tuple(map(int, updated)))
            converted = datetime.datetime.fromtimestamp(
                timestamp,
                tz=timezone.utc
            )
            updated = converted
        else:
            updated = timezone.now()
        self.last_modified = updated

        self.pubdate = parsed.feed.get('pubDate', '')
        self.link = parsed.feed.get('link', self.link)
        self.language = parsed.feed.get('language', self.language)
        self.title = parsed.feed.get('title', '')[:200]
        self.tagline = parsed.feed.get('subtitle', '')[:64]
        self.copyright = parsed.feed.get('copyright', '')[:64]
        self.author = parsed.feed.get('author', '')[:64]
        self.logo = parsed.feed.get('logo', None)
        self.webmaster = parsed.feed.get('webmaster', '')[:64]

    def parse(self):
        """
        Wrap `feedparser.parse`.

        Wrap `feedparser.parse` to handle all exceptions.
        """
        try:
            parsed = feedparser.parse(
                self.feed_url,
                agent=USER_AGENT,
                etag=self.etag
            )
        except Exception as error:
            self.errors = self.errors+1
            self.save()  # touch timestamp
            raise FeedsBaseException(
                "Feedparser Error: {} cannot be parsed.".format(self.feed_url),
                error
            )

        if 'status' not in parsed:
            self.errors = self.errors+1
            self.save()  # touch timestamp
            raise FeedsParseError(
                "Parsed Feed {} didn't provide `status`".format(self.name)
            )

        if parsed.status >= 400:
            self.errors = self.errors+1
            self.save()  # touch timestamp
            raise FeedsHTTPError(
                "Feed {} responded HTTP Client Error (4xx)".format(self.name)
            )

        if 'bozo' in parsed and parsed.bozo == 1:
            self.errors = self.errors+1
            self.save()  # touch timestamp
            if type(parsed.bozo_exception) is \
                    feedparser.CharacterEncodingOverride:
                logger.error("CharacterEncodingOverride, trying to continue")
            else:
                raise FeedsParseError(
                    "[{} !BOZO! Feed '{}' is not well formed: {}".format(
                        self.id,
                        self.name,
                        parsed.bozo_exception
                    )
                )

        if parsed.status == 304:
            raise FeedsSameError(
                "[{}] Feed did not change: {}".format(self.id, self.name)
            )

        self.etag = parsed.get('etag', self.etag)
        self.save()
        logger.debug("-- end --")
        return parsed

    def refresh(self, force=False):
        """
        Refresh `Feed`.

        Fetch posts for this feed, considering all we know about that source.
        We Ratelimit refreshing feeds.

        Args:
            force (boolean): Overrule rate limits.

        Returns:
            enum: The resulting status of refreshing this feed.

        """
        logger.debug("-- start --")
        fiveminutesago = timezone.now() - datetime.timedelta(seconds=300)

        if self.last_checked is not None and force is False:
            if self.last_checked > fiveminutesago:
                logger.debug(
                    "tried feed %s too quick. aborting. (%s, %s, %s)",
                    self.feed_url,
                    self.last_checked,
                    self.last_checked + datetime.timedelta(seconds=300),
                    timezone.now()
                )
                return FEED_SAME

        try:
            parsed = self.parse()
        except FeedsHTTPError:
            return FEED_ERRHTTP
        except FeedsParseError:
            return FEED_ERRPARSE
        except FeedsSameError:
            return FEED_SAME

        try:
            self.update(parsed)
        finally:
            """
            Make sure timestamp is touched

            .. todo::
                make sure this is necessary.
            """
            self.save()

        guid_list = self._guids(parsed.entries)
        postdict = self._postdict(guid_list)
        try:
            result = Counter(
                (
                    self.fromFeedparser(entry, postdict)
                    for
                    entry
                    in
                    parsed.entries
                )
            )
        except Exception as error:
            logger.debug("-- end (ERR) %s --", error)
            traceback.print_exc(file=sys.stdout)
            return FEED_ERREXC

        logger.debug("Feed '%s' returned %s", self.title, result)
        logger.debug("-- end --")
        self.errors = 0
        self.save()
        from django.contrib.sitemaps import ping_google
        ping_google(reverse("planet:sitemap"))
        return FEED_OK
