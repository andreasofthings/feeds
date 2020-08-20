#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
PostManager
===========
"""

import sys
import logging
from django.db import models
import time
import datetime
from django.utils import timezone

from ..models.category import Category
from ..models.tag import Tag

logger = logging.getLogger(__name__)


class PostManager(models.Manager):
    """
    Manage Post Objects.

    Manager for `Post` Objects.
    """

    def subscribed(self, user):
        """
        Subscribe List.

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
        guid = kwargs['guid']

        published = entry.get("published_parsed", None)
        if published:
            timestamp = time.mktime(tuple(map(int, published)))
            converted = datetime.datetime.fromtimestamp(
                timestamp,
                tz=timezone.utc
            )
            published = converted
        else:
            published = datetime.datetime.now()

        post, created = self.get_or_create(
            feed=feed,
            guid=guid,
            published=published
        )

        if created:
            post.guidislink = entry.get("guidislink", False)
            post.link = entry.get("link", post.link)
            post.title = entry.get("title", None)
            post.summary = entry.get("summary", None)
            post.published = published
            post.language = entry.get("language", "en"),
            post.author = entry.get("author", "")
            post.author_email = entry.get("author_email", "")
            post.save()


        tags = entry.get("tags", [])
        if tags:
            for tag in tags:
                t, c = Tag.objects.get_or_create(name=tag['term'])
                if c:
                    t.save()
                post.tags.add(t)

        category = entry.get("category", "")
        # logger.error(f"Post has the following categories: {categories}")
        # logger.error("Entry has the following keys: {}".format(entry.keys()))
        if category:
            cat, c = Category.objects.get_or_create(name=category)
            if c:
                cat.save()
            post.categories.add(cat)

        return post, created

    def today(self):
        """
        Get all Posts for today.

        .. todo::
            Potential timezone / naive datetime problem.
        """
        return self.filter(published__date=datetime.datetime.today())

    def older_than(self, ttl):
        """
        Get all Posts older than ttl.

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
