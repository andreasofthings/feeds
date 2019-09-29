#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
PostManager
===========
"""

from django.db import models
import time
import datetime


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

    def fromFeedparser(self, *args, **kwargs):
        """
        Create a `Post` object from a Feedparser Entry.

        Actual logic to create a new post from feedparser goes here.
        """
        feed = kwargs['feed']
        entry = kwargs['entry']
        print(feed)
        print(entry)

        published = entry.get("published_parsed", None)
        if published:
            timestamp = time.mktime(tuple(map(int, published)))
            converted = datetime.datetime.fromtimestamp(timestamp)
            published = converted
        else:
            published = datetime.datetime.now()
        post, created = self.get_or_create(
            feed=feed,
            guidislink=entry.get("guidislink", False),
            guid=entry.get("id", None),
            link=entry.get("link", None),
            title=entry.get("title", None),
            summary=entry.get("summary", None),
            published=published,
            #  language=entry.get("language", "en"),
            author=entry.get("author", ""),
            author_email=entry.get("author_email", ""),
            # tags=entry.get("tags", []),
        )
        # for tag in entry.get("tags", []):
        #    t, created = post.objects.
        return post, created


    def older_than(self, ttl):
        """
        Get all Posts older than `ttl`.

        `ttl`is in the form of `datetime.timedelta(days=31)``

        .. ToDo: work with timezones.
        """
        from django.utils import timezone
        now = timezone.now()
        edge = now - ttl
        return self.filter(published__lte=edge)

    def latest(self):
        """
        Filter Posts.

        Get all Posts orderd by `published`.
        """
        return self.order_by('-published')
