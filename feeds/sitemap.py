#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
      possible values for changefreq:
        'always'
        'hourly'
        'daily'
        'weekly'
        'monthly'
        'yearly'
        'never'
"""

from datetime import timedelta

from django.utils import timezone
from django.contrib.sitemaps import Sitemap
from django.db.models import Max

from .models import Feed, Post


class FeedSitemap(Sitemap):
    """
    SiteMap for Feeds
    """

    def changefreq(self, obj):
        posts = obj.posts.order_by('-published')
        if posts.count() > 0:
            last_post = posts[0]
            if last_post.published > timezone.now()-timedelta(hours=1):
                return "hourly"
            if last_post.published > timezone.now()-timedelta(days=1):
                return "daily"
            if last_post.published > timezone.now()-timedelta(days=7):
                return "weekly"
        return "monthly"

    def priority(self, obj):
        return 1.0

    def items(self):
        return Feed.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.last_modified


class PostSitemap(Sitemap):
    """
    SiteMap for Posts
      possible values for changefreq:
        'always'
        'hourly'
        'daily'
        'weekly'
        'monthly'
        'yearly'
        'never'
    """

    def changefreq(self, obj):
        if obj.published > timezone.now()-timedelta(hours=1):
            return "hourly"
        if obj.published > timezone.now()-timedelta(days=1):
            return "daily"
        if obj.published > timezone.now()-timedelta(days=7):
            return "weekly"
        if obj.published > timezone.now()-timedelta(days=31):
            return "monthly"
        return "yearly"

    def priority(self, obj):
        """
        Datamodel changed

        .. todo::
        Fix to use ratings.score
        """
        posts = Post.objects.all()
        maximum = 100 # float(posts.aggregate(Max('rating__score'))['score__max'])
        if maximum > 0:
            priority = float(50)/float(maximum)
            # priority = float(obj.rating)/float(maximum)
        else:
            priority = 0

        if priority <= 0.1:
            priority = 0

        return priority

    def items(self):
        return Post.objects.order_by('-published')

    def lastmod(self, obj):
        return obj.published

    limit = 1000
