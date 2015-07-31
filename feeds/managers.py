#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Managers
========
"""

from django.db import models


class WebSiteManager(models.Manager):
    """
    :py:mod:`WebSiteManager` provide extra functions.
    """
    def __init__(self, *args, **kwargs):
        return super(WebSiteManager, self).__init__(*args, **kwargs)

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class TagManager(models.Manager):
    """
    Manager for `Tag` objects.
    """

    def get_by_natural_key(self, name):
        """
        get Tag by natural key, to allow serialization by key rather than `ìd`
        """
        return self.get(name=name)


class CategoryManager(models.Manager):
    """
    Manager for Category
    """
    def get_by_natural_key(self, name):
        """
        Get Category by natural kea to allow serialization
        """
        return self.get(name=name)


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
        clicklist = self.objects.filter(post__feed__id=feed_id)
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


class OptionsManager(models.Manager):
    def get_options(self):
        options = self.objects.all()
        if options:
            options = options[0]
        else:
            options = self.objects.create()
            """Create with default value."""
        return options
