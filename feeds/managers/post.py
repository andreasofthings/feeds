#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
PostManager
===========
"""

from django.db import models


class PostManager(models.Manager):
    """
    """
    def subscribed(self, user):
        """
        Get only Posts for subscribed feeds.
        .. todo: This returns a queryset of all Posts, ordered by their
        published date. It should be limited by the requesting users feed-
        subscriptions. At the time, the queryset below likely breaks.
        """
        return self.filter(feeds_subscriptions__user=user)

    def from_feedparser(self, *args, **kwargs):
        """
        Actual logic to create a new post from feedparser goes here.
        """
        return self.get_or_create(*args, **kwargs)

    def older_than(self, ttl):
        """
        Get all Posts older than `ttl`.

        .. ToDo: work with timezones.
        """
        from datetime import datetime
        edge = datetime.now() - ttl
        return self.filter(published__lte=edge)