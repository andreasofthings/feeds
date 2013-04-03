#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
feeds/feeds.py

output feeds collected elsewhere

..codeauthor: Andreas Neumeier

"""

from django.contrib.syndication.views import Feed as NewsFeed
from django.utils import feedgenerator
from django.contrib.syndication.views import FeedDoesNotExist
from django.shortcuts import get_object_or_404

from django.utils.feedgenerator import Rss201rev2Feed

from feeds.models import Feed, Post

class AngryPlanetFeed(Rss201rev2Feed):
    def root_attributes(self):
        attrs = super(iTunesFeed, self).root_attributes()
        attrs['xmlns:itunes'] = 'http://www.itunes.com/dtds/podcast-1.0.dtd'
        return attrs

    def add_root_elements(self, handler):
        super(iTunesFeed, self).add_root_elements(handler)
        handler.addQuickElement('itunes:explicit', 'clean')

class RssFeed(NewsFeed):
    def get_object(self, request, pk):
        return get_object_or_404(Feed, pk=pk)

    def items(self, obj):
        return Post.objects.filter(feed=obj).order_by('-created')

    def title(self, obj):
        return u"%s" % obj.title

    def author(self, obj):
        return u"%s" % obj.author

    def link(self, obj):
        return obj.link

    def feed_url(self, obj):
        return obj.link

    def item_link(self, item):
        return item.get_trackable_url()

# vim: ts=4 et sw=4 sts=4

