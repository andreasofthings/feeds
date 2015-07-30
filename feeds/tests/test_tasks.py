#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

import logging

from datetime import datetime
import feedparser

from django.test import TestCase

from feeds import ENTRY_NEW, ENTRY_UPDATED
from feeds import FEED_OK
from feeds import CRON_OK
from feeds.models import Feed, Post


logger = logging.getLogger(__name__)


class TaskTest(TestCase):
    """
    Test Tasks

    .. codeauthor:: Andreas Neumeier <andreas@neumeier.org>
    """

    fixtures = [
        'Site.yaml',
        'Feed_basic.yaml',
        'Posts.yaml',
    ]

    def setUp(self):
        """
        Set up enivironment to test models.
        """

    def test_task_time(self):
        """
        This is a test whether start-time is seen.
        """
        from feeds.tasks import dummy
        dummy.delay(invocation_time=datetime.now())
        dummy(10)

    def test_aggregate(self):
        """
        Test for the `cronjob` function in :py:mod:`feeds.tasks`

        This will go through all of the feeds in the fixture.
        """
        from feeds.tasks import cronjob
        test_result = cronjob.delay()
        self.assertEqual(test_result.get(), CRON_OK)

    def test_count_tweets(self):
        """
        """
        from feeds.tasks import post_update_twitter
        post = Post.objects.all()[0]
        result = post_update_twitter.delay(post.pk)
        self.assertEqual(result.get(), 0)

    def test_count_share_like(self):
        from feeds.tasks import entry_update_facebook
        posts = Post.objects.all()
        result = entry_update_facebook.delay(posts[0].pk)
        self.assertEqual(result.get(), True)

    def test_feed_refresh(self):
        from feeds.tasks import feed_refresh
        feed = Feed.objects.all()[0]
        result = feed_refresh(feed.id)
        self.assertEqual(type(FEED_OK), type(result))

    def test_entry_process(self):
        feeds = Feed.objects.all()
        parsed = feedparser.parse(feeds[0].feed_url)
        self.assertGreater(len(parsed.entries), 0)
        for entry in parsed.entries:
            result = feeds[0].from_feedparser(entry, None)
            self.assertEqual(result, ENTRY_NEW)
        for entry in parsed.entries:
            result = feeds[0].from_feedparser(entry, None)
            self.assertEqual(result, ENTRY_UPDATED)

    def tearDown(self):
        pass
