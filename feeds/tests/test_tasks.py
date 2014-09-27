#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from datetime import datetime
import feedparser

from django.test import TestCase
from django.core.urlresolvers import reverse

from feeds import FEED_OK, FEED_SAME, FEED_ERRPARSE, FEED_ERRHTTP, FEED_ERREXC
from feeds.models import Feed, Post


class TaskTest(TestCase):
    """
    Test Tasks

    .. codeauthor:: Andreas Neumeier <andreas@neumeier.org>
    """

    fixtures = ['Site.yaml', 'Feed.yaml', ]

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
        This is a test whether start-time is seen.
        """
        from feeds.tasks import dummy
        dummy.delay(invocation_time=datetime.now())
        dummy(10)

    def test_cronjob(self):
        """
        This is a test for the entire chain.
        """
        from feeds.tasks import cronjob
        cronjob()

    def test_aggregate(self):
        """
        Test for the `aggregate` function in :py:mod:`feeds.tasks`
        """
        from feeds.tasks import cronjob
        test_result = cronjob()
        # self.assertTrue(result.successful())
        self.assertEqual(type(test_result), type({}))
        self.assertIn(FEED_OK, test_result)
        self.assertIn(FEED_SAME, test_result)
        self.assertIn(FEED_ERRPARSE, test_result)
        self.assertIn(FEED_ERRHTTP, test_result)
        self.assertIn(FEED_ERREXC, test_result)

    def test_count_tweets(self):
        """
        """
        from feeds.tasks import entry_update_twitter
        post = Post.objects.all()[0]
        result = entry_update_twitter.delay(post.pk)
        self.assertEqual(result.get(), 0)

    def test_count_share_like(self):
        from feeds.tasks import entry_update_facebook
        post = Post.objects.all()[0]
        result = entry_update_facebook.delay(post.pk)
        self.assertEqual(result.get(), True)

    def test_feed_refresh(self):
        from feeds.tasks import feed_refresh
        feed = Feed.objects.all()[0]
        result = feed_refresh(feed.id)
        self.assertEqual(type(FEED_OK), type(result))

    def test_entry_process(self):
        from feeds.tasks import entry_process
        f = Feed.objects.all()[0]
        feed = feedparser.parse(f.feed_url)
        for entry in feed.entries:
            result = entry_process(entry, f.id, None, None)
            self.assertEqual(result, True)

    def tearDown(self):
        pass
