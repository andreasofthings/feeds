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
from django.conf import settings


logger = logging.getLogger(__name__)


class SiteManager(models.Manager):
    """
    :py:mod:`SiteManager` provide extra functions.
    """
    def __init__(self, *args, **kwargs):
        return super(SiteManager, self).__init__(*args, **kwargs)

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Site(models.Model):
    url = models.URLField(unique=True)
    """URL of the `Site`."""

    slug = models.SlugField(null=True)
    """Human readble URL component"""

    objects = SiteManager()
    """
    Overwrite the inherited manager
    with the custom :mod:`feeds.models.SiteManager`
    """

    def save(self, *args, **kwargs):
        """
        Since 'slug' is not a required field for userinput,
        set it before saving.
        """
        if not self.slug:
            self.slug = slugify(self.url)
        return super(Site, self).save(*args, **kwargs)

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


class TagManager(models.Manager):
    """
    Manager for `Tag` objects.
    """

    def get_by_natural_key(self, name):
        """
        get Tag by natural key, to allow serialization by key rather than `ìd`
        """
        return self.get(name=name)


class Tag(models.Model):
    """
    A tag.
    """

    objects = TagManager()
    """
    Overwrite the inherited manager
    with the custom :mod:`feeds.models.TagManager`
    """

    name = models.CharField(
        _('name'),
        max_length=50,
        unique=True,
        db_index=True
    )
    """The name of the Tag."""

    relevant = models.BooleanField(default=False)
    """
    Indicates whether this Tag is relevant for further processing.
    It should be used to allow administrative intervention.
    """

    touched = models.DateTimeField(auto_now=True)
    """Keep track of when this Tag was last used."""

    @property
    def slug(self):
        return slugify(self.name)

    class Meta:
        """
        Django Meta.
        """
        ordering = ('name',)
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def posts(self):
        """
        return all feeds in this category
        """
        return self.tag_posts.all()

    def __unicode__(self):
        """
        Human readable representation of the object.
        """
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('planet:tag-view', [str(self.pk)])

    def natural_key(self):
        return (self.name,)


class CategoryManager(models.Manager):
    """
    Manager for Category
    """
    def get_by_natural_key(self, name):
        """
        Get Category by natural kea to allow serialization
        """
        return self.get(name=name)


class Category(models.Model):
    """
    Category
    ========

    Category model to be used for categorization of content. Categories are
    high level constructs to be used for grouping and organizing content,
    thus creating a site's table of contents.
    """

    objects = CategoryManager()
    """
    References the default ModelManager,
    here :py:mod:`feeds.models.CategoryManager`.
    """

    name = models.CharField(
        max_length=200,
        help_text='Short descriptive name for this category.',
        unique=True,
    )

    @property
    def slug(self):
        return slugify(self.name)

    def __unicode__(self):
        return self.name

    class Meta:
        """
        Django Meta.
        """
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    @property
    def tags(self):
        """
        Return all :py:mod:`feeds.models.Tag`s for this Category.
        """
        return Tag.objects.filter(categories__in=[self]).order_by('name')

    @property
    def feeds(self):
        """
        Return all :py:mod:`feeds.models.Feed`s in this Category.
        """
        return self.category_feeds.all()

    def natural_key(self):
        return (self.name, )

    @models.permalink
    def get_absolute_url(self):
        return ('planet:category-view', [str(self.pk)])


class FeedManager(models.Manager):
    """
    Manager object for :py:mod:`feeds.models.Feed`
    """
    def get_by_natural_key(self, name):
        """
        Get Feed by natural key, to allow
        serialization by key rather than `id`.
        """
        return self.get(name=name)


class Feed(models.Model):
    """
    Model that contains information about any feed, including
    - metadata for processing
    - results from social updates
    - calculated values
    """
    site = models.ForeignKey(Site, null=True)
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
    beta = models.BooleanField(
        _('is beta'),
        default=False,
        help_text=_('If beta, celery pipeline.')
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
        if not self.short_name:
            self.short_name = f.feed.title
        if not self.link and hasattr(f.feed, 'link'):
            self.link = f.feed.link
        if hasattr(f.feed, 'language'):
            self.language = f.feed.language
        if not self.slug:
            self.slug = slugify(self.name)
        super(Feed, self).save(args, kwargs)

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


class Post(models.Model):
    """
    Model to hold an actual feed entry
    """
    feed = models.ForeignKey(
        Feed,
        verbose_name=_('feed'),
        related_name="posts",
        null=False,
        blank=False,
    )
    title = models.CharField(max_length=512)
    link = models.URLField(_('link'), )
    content = models.TextField(_('description'), blank=True)
    author = models.CharField(_('author'), max_length=50, blank=True)
    author_email = models.EmailField(_('author email'), blank=True)
    category = models.ManyToManyField(
        Category,
        related_name="category_posts",
        blank=True,
    )
    comments = models.URLField(_('comments'), blank=True)
    # enclosure, see there
    guid = models.CharField(
        _('guid'),
        max_length=255,
        db_index=True,
        unique=True
    )
    created = models.DateTimeField(_('pubDate'), auto_now_add=True)

    published = models.BooleanField(default=False)

    last_modified = models.DateTimeField(null=True, blank=True)
    """.. todo::  this is unused, remove? """

    date_modified = models.DateTimeField(
        _('date modified'),
        null=True,
        blank=True
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="tag_posts",
        through='TaggedPost'
    )

    # Social
    tweets = models.IntegerField(default=0)
    blogs = models.IntegerField(default=0)
    plus1 = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    pageviews = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    updated_social = models.BooleanField(default=False)

    # republishing
    was_announced = models.BooleanField(default=False)
    was_recommended = models.BooleanField(default=False)

    # management
    has_errors = models.BooleanField(default=True)

    @models.permalink
    def get_absolute_url(self):
        return ('post-view', [str(self.id)])

    @models.permalink
    def get_trackable_url(self):
        """
        Get an URL for this particular object,
        that will be tracked in a separate view.

        The related view is :mod:`feeds.views.PostTrackableView`

        The view redirects to `feeds.models.Post.link`, storing
        information about the requesting client in `feeds.models.PostReadCount`
        """
        return ('planet:post-trackable-view', [str(self.id)])

    def save(self, *args, **kwargs):
        """
        sanity check the post before saving.
        """
        if not self.guid:
            self.guid = self.link
        super(Post, self).save(*args, **kwargs)
        """Call the "real" save() method."""

    def __unicode__(self):
        return u'%s' % (self.title)


class Enclosure(models.Model):
    """
    potential enclosure of a :mod:`feeds.models.Post`
    """

    post = models.ForeignKey(Post, related_name="enclosure")
    """reference to the post the enclosure belongs to."""

    url = models.URLField()
    """the url of the enclosed media file."""

    length = models.BigIntegerField()
    """length of the enclosed media file in byte."""

    enclosure_type = models.CharField(max_length=32)
    """type of the enclosed file, for example 'image/jpeg'."""

    def __unicode__(self):
        """
        return type of object and containing post
        """
        return u'%s [for %s]' % (self.enclosure_type, self.post)


class FeedPostCount(models.Model):
    feed = models.ForeignKey(
        Feed,
        verbose_name=_('feed'),
        null=False,
        blank=False
    )
    entry_new = models.IntegerField(default=0)
    entry_updated = models.IntegerField(default=0)
    entry_same = models.IntegerField(default=0)
    entry_err = models.IntegerField(default=0)
    created = models.IntegerField()

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
    feed = models.ForeignKey(Feed)
    collected = models.DateTimeField(auto_now_add=True)
    entry_new = models.IntegerField(default=0)
    entry_same = models.IntegerField(default=0)
    entry_updated = models.IntegerField(default=0)
    entry_err = models.IntegerField(default=0)


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


class PostReadCountManager(models.Manager):
    """
    Manager for Tag objects
    """

    def get_feed_count_in_timeframe(self, feed_id, start, delta, steps):
        """
        feed_id:which feed
        start:  start at which time
        delta:  how long shall one step be
        steps:  how many steps
        """
        clickdata = ()
        clicklist = PostReadCount.objects.filter(post__feed__id=feed_id)
        lower_offset = start
        for i in range(steps):
            upper_offset = lower_offset
            lower_offset = upper_offset - delta
            if clicklist:
                clickdata.append(
                    clicklist.filter(
                        created__gte=lower_offset
                    ).filter(created__lte=upper_offset).count())
        return clickdata


class PostReadCount(models.Model):
    """
    This is not a real counter, more a log.

    Need to count and cleanup elsewhere.
    """
    objects = PostReadCountManager()
    post = models.ForeignKey(Post)
    created = models.DateTimeField(auto_now=True)


class TaggedPost(models.Model):
    """
    Holds the relationship between a tag and the item being tagged.
    """

    tag = models.ForeignKey(
        Tag,
        verbose_name=_('tag'),
        related_name='post_tags'
    )
    post = models.ForeignKey(
        Post,
        verbose_name=_('post')
    )

    class Meta:
        # Enforce unique tag association per object
        unique_together = (('tag', 'post', ),)
        verbose_name = _('tagged item')
        verbose_name_plural = _('tagged node')

    def __unicode__(self):
        return u'%s [%s]' % (self.post, self.tag)


class OptionsManager(models.Manager):
    def get_options(self):
        options = Options.objects.all()
        if options:
            options = options[0]
        else:
            options = Options.objects.create()
            """Create with default value."""
        return options


class Options(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    number_initially_displayed = models.IntegerField(default=10)
    number_additionally_displayed = models.IntegerField(default=5)
    max_entries_saved = models.IntegerField(default=100)

    objects = OptionsManager()
    subscriptions = models.ManyToManyField(Feed, through='Subscription')

    class Meta:
        verbose_name_plural = "options"

    def __unicode__(self):
        return u'Options'


class Subscription(models.Model):
    """
    User Feed Subscription
    """
    user = models.ForeignKey(
        Options,
        verbose_name=_('User Subscription'),
        related_name='user_subscription'
    )
    feed = models.ForeignKey(
        Feed,
        verbose_name=_('Feed Subscription'),
        related_name='feed_subscription'
    )

    def __unicode__(self):
        return u'%s subscribed [%s]' % (self.user, self.feed)
