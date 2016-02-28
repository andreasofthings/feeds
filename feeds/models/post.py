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

import logging

from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .feed import Feed
from category.tag import Tag

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
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
    comments = models.URLField(_('comments'), blank=True)
    # enclosure, see there
    guid = models.CharField(
        _('guid'),
        max_length=255,
        db_index=True,
        unique=True
    )
    published = models.DateTimeField(_('pubDate'))
    updated = models.DateTimeField(_('last_updated'), auto_now=True)

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
    linkedin = models.IntegerField(default=0)
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
        return ('planet:post-view', [str(self.id)])

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

    def __str__(self):
        """
        Python 2/3 compatibility through @python_2_unicode_compatible
        """
        return u'%s' % (self.title)


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
