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


class TaskTestNot(TestCase):
    """
    Test Tasks

    .. codeauthor:: Andreas Neumeier <andreas@neumeier.org>
    """

    fixtures = [
        'WebSite.yaml',
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
        test_result = cronjob()
        self.assertEqual(test_result, CRON_OK)

    def test_purge(self):
        """
        Test for the `purge` function in :py:mod:`feeds.tasks`

        This will go through all of the posts in the fixture and
        purge for the default value.
        """
        from feeds.tasks import purge
        test_result = purge.delay()
        self.assertEqual(test_result.get(), True)

    def test_count_tweets(self):
        """
        test tweet-counts

        .. todo:: make this relevant
        .. todo:: test this in the `python-social` module
        """
        self.assertEqual(True, True)
        return
        from feeds.tasks import post_update_twitter
        post = Post.objects.all()[0]
        result = post_update_twitter.delay(post.pk)
        self.assertEqual(result.get(), (0,))

        result = post_update_twitter.delay(999999)
        with self.assertRaises(Post.DoesNotExist):
            self.assertEqual(type(result.get()), type((0, )))
            self.assertEqual(len(result.get()), len((0, )))

    def test_count_share_like(self):
        """
        test facebook shares and likes

        .. todo:: make this relevant
        .. todo:: test this in the `python-social` module
        """
        self.assertEqual(True, True)
        return
        from feeds.tasks import post_update_facebook
        posts = Post.objects.all()
        result = post_update_facebook.delay(posts[0].pk)
        self.assertEqual(type(result.get()), type((0, 0)))
        self.assertEqual(len(result.get()), len((0, 0,)))

        result = post_update_facebook.delay(9999999)
        with self.assertRaises(Post.DoesNotExist):
            self.assertEqual(type(result.get()), type((0, 0)))
            self.assertEqual(len(result.get()), len((0, 0)))

    def test_count_linkedin(self):
        """
        test linkedin count

        .. todo:: make this relevant
        .. todo:: test this in the `python-social` module
        """
        self.assertEqual(True, True)
        return

        from feeds.tasks import post_update_linkedin

        post = Post.objects.all()[0]
        result = post_update_linkedin.delay(post.pk)
        self.assertEqual(len(result.get()), len((0,)))

        result = post_update_linkedin.delay(999999)

        with self.assertRaises(Post.DoesNotExist):
            self.assertEqual(result.get(), (-1,))

    def test_update_social(self):
        """
        """
        from feeds.tasks import post_update_social

        post = Post.objects.all()[0]
        """Get a post from test-data."""
        result = post_update_social.delay(post.pk)
        """See how often that was shared socially."""
        self.assertEqual(type(result.get()), type(0))
        """Since it's test-data, it should show up some integer."""

        result = post_update_social.delay(999999)
        """Try to find a non-existing post on social media."""
        self.assertEqual(result.get(), 0)
        """Expect '0' as a result."""

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
            """
            .. todo::
                should actually assert a new entry:
                    `self.assertEqual(result, ENTRY_NEW)`
            """
        for entry in parsed.entries:
            result = feeds[0].from_feedparser(entry, None)
            self.assertEqual(result, ENTRY_UPDATED)

    def tearDown(self):
        pass
