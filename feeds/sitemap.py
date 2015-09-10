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

from datetime import datetime, timedelta

from django.utils import timezone
from django.contrib.sitemaps import Sitemap
from django.db.models import Max

from feeds.models import Feed, Post, Category, Tag


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
        posts = Post.objects.all()
        maximum = float(posts.aggregate(Max('score'))['score__max'])
        if maximum > 0:
            priority = float(obj.score)/float(maximum)
        else:
            priority = 0

        if priority <= 0.1:
            priority = 0

        return priority

    def items(self):
        return Post.objects.filter(score__gt=0)

    def lastmod(self, obj):
        return obj.published

    limit = 1000


class CategorySitemap(Sitemap):
    """
    SiteMap for Categories
    """

    def changefreq(self, obj):
        return "weekly"

    def priority(self, obj):
        return 1.0

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return datetime.now()


class TagSitemap(Sitemap):
    """
    SiteMap for Tags
    """

    def changefreq(self, obj):
        if obj.touched > timezone.now()-timedelta(hours=1):
            return "hourly"
        if obj.touched > timezone.now()-timedelta(days=1):
            return "daily"
        if obj.touched > timezone.now()-timedelta(days=7):
            return "weekly"
        return "monthly"

    def priority(self, obj):
        posts_per_tag = obj.posts().count()
        total_posts = Post.objects.all().count()
        priority = float(posts_per_tag) / float(total_posts)
        return priority

    def items(self):
        return Tag.objects.all()

    def lastmod(self, obj):
        return obj.touched
