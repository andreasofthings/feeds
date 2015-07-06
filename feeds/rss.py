#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
feeds/feeds.py

output feeds collected elsewhere

..codeauthor: Andreas Neumeier

"""

from django.contrib.syndication.views import Feed as NewsFeed
from django.shortcuts import get_object_or_404

from django.utils.feedgenerator import Rss201rev2Feed

from feeds.models import Feed, Post


class ITunesFeed(Rss201rev2Feed):
    """
    This shall reproduce an iTunes Feed
    """
    def root_attributes(self):
        attrs = super(ITunesFeed, self).root_attributes()
        attrs['xmlns:itunes'] = 'http://www.itunes.com/dtds/podcast-1.0.dtd'
        return attrs

    def add_root_elements(self, handler):
        super(ITunesFeed, self).add_root_elements(handler)
        handler.addQuickElement('itunes:explicit', 'clean')


class RssFeed(NewsFeed):
    """
    Re-Produce a RSS Feed from stored items
    """

    def get_object(self, request, feed_id):
        """
        Get the feed for which the items should be processed
        """
        return get_object_or_404(Feed, pk=feed_id)

    def items(self, obj):
        """
        get the actual feed-entries for `obj`
        """
        result = Post.objects.filter(feed=obj).order_by('-updated')
        return result

    def title(self, obj):
        """
        Return the title for this feed.
        The feed is in `obj`, provided by `get_object`
        """
        return u"%s" % obj.title

    def author(self, obj):
        """
        Return the author for this feed.
        The feed is in `obj`, provided by `get_object`
        """
        return u"%s" % obj.author

    def link(self, obj):
        """
        Return the link for this feed.
        The feed is in `obj`, provided by `get_object`
        """
        return obj.link

    def feed_url(self, obj):
        """
        Return the feed_url/link for this feed.
        The feed is in `obj`, provided by `get_object`
        """
        return obj.link

    def item_link(self, item):
        """
        Return a trackable link for every item part of this feed.
        """
        return item.get_trackable_url()
