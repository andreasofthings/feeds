#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Managers
========
"""

from django.db import models
from django.core.cache import cache

import feedparser
import requests


class FeedManager(models.Manager):
    """
    Manager object for :py:mod:`feeds.models.Feed`
    """

    @classmethod
    def create(cls, website, url):
        """
        Create a :py:mod:`feeds.model.Feed` object
        """
        feed = cls(website=website, feed_url=url)
        feedcontent = cache.get_or_set(url, requests.get(url), 10600)
        parsed = feedparser.parse(feedcontent)
        feed.title = parsed.feed.get('title', '')[0:200]
        feed.tagline = parsed.feed.get('subtitle', '')[:64]
        feed.copyright = parsed.feed.get('copyright', '')[:64]
        feed.author = parsed.feed.get('author', '')[:64]
        feed.logo = parsed.feed.get('logo', None)
        feed.webmaster = parsed.feed.get('webmaster', '')[:64]
        return feed

    def get_by_natural_key(self, name):
        """
        Get Feed by natural key, to allow
        serialization by key rather than `id`.
        """
        return self.get(name=name)
