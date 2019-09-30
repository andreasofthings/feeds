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
from ..managers import PostManager

from .category import Tag, Category


logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Post(models.Model):
    """
    Model to hold an actual feed entry

    .. required::
      - feed
      - title
      - link
      - published
    """
    feed = models.ForeignKey(
        Feed,
        verbose_name=_('feed'),
        related_name="posts",
        null=False,
        blank=False,
        on_delete=models.DO_NOTHING,
    )
    title = models.CharField(max_length=512)
    link = models.URLField(_('link'), )
    summary = models.TextField(_('description'), blank=True)
    author = models.CharField(_('author'), max_length=50, blank=True)
    author_email = models.EmailField(_('author email'), blank=True)
    comments = models.URLField(_('comments'), blank=True)
    # enclosure , see there
    guid = models.CharField(
        _('guid'),
        max_length=255,
        db_index=True,
        unique=True
    )
    guidislink = models.BooleanField(default=False)
    published = models.DateTimeField(_('pubDate'))
    updated = models.DateTimeField(_('last_updated'), auto_now=True)

    tags = models.ManyToManyField(
        Tag,
        related_name="tag_posts",
        through='TaggedPost'
    )

    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name="categories"
    )

    # management
    has_errors = models.BooleanField(default=False)

    # republishing
    was_announced = models.BooleanField(default=False)
    was_recommended = models.BooleanField(default=False)

    objects = PostManager()

    class Meta:
        """
        Django Meta
        """

        app_label = "feeds"
        ordering = ['-published', ]

    @property
    def score(self):
        """
        .. todo::
            implement this depending on `:py:feeds.models.rating`
        """
        return self.ratings.order_by('-updated')[0]

    def get_absolute_url(self):
        """return the absolute url for this `Post`."""
        from django.urls import reverse
        return reverse('planet:post-detail', args=[str(self.id)])

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
        related_name='post_tags',
        on_delete=models.DO_NOTHING,
    )
    post = models.ForeignKey(
        Post,
        verbose_name=_('post'),
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        """
        Meta Information TaggedPost.

        Enforce unique tag association per object
        """
        app_label = "feeds"
        unique_together = (('tag', 'post', ),)
        verbose_name = _('tagged item')
        verbose_name_plural = _('tagged node')

    def __unicode__(self):
        return u'%s [%s]' % (self.post, self.tag)
