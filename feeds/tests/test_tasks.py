#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from datetime import datetime
import feedparser

from django.test import TestCase
from django.core.urlresolvers import reverse

from feeds.models import Feed, Post


class TaskTest(TestCase):
    """
    Test Tasks

    .. codeauthor:: Andreas Neumeier <andreas@neumeier.org>
    """

    fixtures = ['Feed.yaml', ]

    def setUp(self):
        """
        Set up enivironment to test models.
        """

        self.feed1 = Feed(
            feed_url=reverse('planet:rss1'),
            name="rss1",
            short_name="rss1"
        )
        self.feed1.save()

        self.feed2 = Feed(
            feed_url=reverse('planet:rss2'),
            name="rss2",
            short_name="rss2"
        )
        self.feed2.save()

        self.post1 = Post(
            feed=self.feed1,
            link="http://localhost/post1"
        )
        self.post1.save()

        self.post2 = Post(
            feed=self.feed2,
            link="http://localhost/post2"
        )
        self.post2.save()

    def test_task_time(self):
        """
        .. todo:: Needs amqp.
        """
        from feeds.tasks import dummy
        dummy.delay(invocation_time=datetime.now())
        dummy(10)

    def test_aggregate(self):
        from feeds.tasks import aggregate
        result = aggregate()
        self.assertEqual(result, True)

    def test_count_tweets(self):
        from feeds.tasks import entry_update_twitter
        result = entry_update_twitter(Post.objects.all()[0].id)
        self.assertEqual(result, 0)

    def test_count_share_like(self):
        from feeds.tasks import entry_update_facebook
        result = entry_update_facebook(Post.objects.all()[0].id)
        self.assertEqual(result, True)

    def test_feed_refresh(self):
        from feeds.tasks import feed_refresh
        from feeds import ENTRY_NEW, ENTRY_UPDATED, ENTRY_SAME, ENTRY_ERR
        feed = Feed.objects.all()[0]
        result = feed_refresh(feed.id)
        self.assertGreaterEqual(result[ENTRY_NEW], 0)
        self.assertGreaterEqual(result[ENTRY_UPDATED], 0)
        self.assertGreaterEqual(result[ENTRY_SAME], 0)
        self.assertGreaterEqual(result[ENTRY_ERR], 0)

    def test_entry_process(self):
        from feeds.tasks import entry_process
        f = Feed.objects.all()[0]
        feed = feedparser.parse(f.feed_url)
        for entry in feed.entries:
            result = entry_process(entry, f.id, None, None)
            self.assertEqual(result, True)

    def tearDown(self):
        pass
