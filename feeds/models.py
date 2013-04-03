#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Feed-Aggregator models
"""

import os
import re
                
import feedparser
import urllib2
from django.db import models, IntegrityError
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _ 
from django.template.defaultfilters import slugify

class TagManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

class Tag(models.Model):
    """
    A tag.
    """
    objects = TagManager()
    name = models.CharField(_('name'), max_length=50, unique=True, db_index=True)
    slug = models.SlugField(
        max_length=255,
        db_index=True,
        unique=True,
        help_text='Short descriptive unique name for use in urls.',
    )

    relevant = models.BooleanField(default = False)
    touched = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    @property
    def posts(self):
        """
        return all feeds in this category
        """
        return ()# self.tag_posts.all()
    
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('planet:tag-view', [str(self.slug)])

class CategoryManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

class Category(models.Model):
    """
    Category model to be used for categorization of content. Categories are
    high level constructs to be used for grouping and organizing content,
    thus creating a site's table of contents.
    """
    objects = CategoryManager()
    
    title = models.CharField(
        max_length=200,
        help_text='Short descriptive name for this category.',
    )
    
    slug = models.SlugField(
        max_length=255,
        db_index=True,
        unique=True,
        help_text='Short descriptive unique name for use in urls.',
    )
    
    parent = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        # ToDo: prohibit circular references
        if not self.slug:
            self.slug = slugify(self.title)  # Where self.name is the field used for 'pre-populate from'
        super(Category, self).save(*args, **kwargs)

    @property
    def children(self):
        return self.category_set.all().order_by('title')

    @property
    def tags(self):
        return Tag.objects.filter(categories__in=[self]).order_by('title')

    @property
    def feeds(self):
        """
        return all feeds in this category
        """
        return self.category_feeds.all()

    @models.permalink
    def get_absolute_url(self):
        return ('planet:category-view', [str(self.slug)])

class Feed(models.Model):
    """
    Model that contains information about any feed, including
    - metadata for processing 
    - results from social updates
    - calculated values 
    """
    name = models.CharField(_('name'), max_length=100)
    shortname = models.CharField(_('shortname'), max_length=50)
    slug = models.SlugField(
        max_length=255,
        db_index=True,
        unique=True,
        null=True,
        help_text='Short descriptive unique name for use in urls.',
    )

    feed_url = models.URLField(_('feed url'), unique=True)
    is_active = models.BooleanField(
            _('is active'), 
            default=True,
            help_text=_('If disabled, this feed will not be further updated.') 
        )
    beta = models.BooleanField(
        _('is beta'), 
        default=False,
        help_text=_('If beta, this feed will be processed through the celery pipeline.') 
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
    last_modified = models.DateTimeField(_('lastBuildDate'), null=True, blank=True)

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
        _("""ttl stands for time to live. It's a number of minutes that indicates how long a channel can be cached before refreshing from the source."""),
        default=60
    )

    image_title = models.CharField(_('image_title'), max_length=200, blank=True)
    image_link = models.URLField(_('image_link'), blank=True)
    image_url = models.URLField(_('image_url'), blank=True)

    # ratin
    # textInput
    # skipHours
    # skipDay

    # http://feedparser.org/docs/http-etag.html
    etag = models.CharField(_('etag'), max_length=50, blank=True)
    last_checked = models.DateTimeField(_('last checked'), null=True, blank=True)


    def save(self, *args, **kwargs):
        """
        Need to update items before saving?
        """
        if not self.slug:
            self.slug = slugify(self.shortname) 
        super(Feed, self).save(args, kwargs)

    class Meta:
        """
        Metadata for Feed Model
        """
        verbose_name = _('feed')
        verbose_name_plural = _('feeds')
        ordering = ('name', 'feed_url',)
        permissions = (
            ("can_refresh_feed", "Can refresh feed"),
        )

    def __unicode__(self):
        return u'%s' % (self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('planet:feed-view', [str(self.id)])
    
class Post(models.Model):
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
    guid = models.CharField(_('guid'), max_length=200, db_index=True, unique=True)
    created = models.DateTimeField(_('pubDate'), auto_now_add=True)

    published = models.BooleanField(default=False)
        
    last_modified = models.DateTimeField(null=True, blank=True) # ToDo: this is unused, remove?
    date_modified = models.DateTimeField(_('date modified'), null=True, blank=True)
            

    tags = models.ManyToManyField(Tag, related_name="tag_posts", through='TaggedPost')

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
        return ('planet:post-trackable-view', [str(self.id)])

    def __unicode__(self):
        return u'%s'%(self.title)

    def save(self, *args, **kwargs):
        try:
            super(Post, self).save(*args, **kwargs)
        except IntegrityError, e:
            if e == 1062:
                pass
                # logger.debug("entry %s does already exist"%(self.guid))

class Enclosure(models.Model):
    """
    potential enclosure of a post
    """
    post = models.ForeignKey(Post, related_name="enclosure")
    url = models.URLField()
    length = models.BigIntegerField()
    enclosure_type = models.CharField(max_length=32)

class FeedPostCount(models.Model):
    feed = models.ForeignKey(Feed, verbose_name=_('feed'), null=False, blank=False)
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
        super(FeedPostCount, self).save(*args, **kwargs) # Call the "real" save() method.

class PostReadCount(models.Model):
    """
    This is not a real counter, more a log.

    Need to count and cleanup elsewhere.
    """
    post = models.ForeignKey(Post)
    created = models.DateTimeField(auto_now=True)

class TaggedPost(models.Model):
    """
    Holds the relationship between a tag and the item being tagged.
    """
    
    tag  = models.ForeignKey(Tag, verbose_name=_('tag'), related_name='post_tags')
    post = models.ForeignKey(Post, verbose_name=_('post'))

    class Meta:
        # Enforce unique tag association per object
        unique_together = (('tag', 'post', ),)
        verbose_name = _('tagged item')
        verbose_name_plural = _('tagged node')

    def __unicode__(self):
        return u'%s [%s]' % (self.post, self.tag)

# vim: ts=4 et sw=4 sts=4

