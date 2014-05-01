#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Tests for the "feeds" app
"""

import feedparser

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse

from feeds.models import Feed, Post
from feeds.tasks import aggregate, entry_process, feed_refresh, dummy
from feeds.tasks import entry_update_twitter, entry_update_facebook

from feeds import ENTRY_NEW, ENTRY_UPDATED, ENTRY_SAME, ENTRY_ERR

from datetime import datetime

class ModelTest(TestCase):
    """
    Test Models and their Managers
    """
    def setUp(self):
        """
        Set up enivironment to test models
        """
        pass

    def test_tag(self):
        """
        Test a Tag
        """
        from feeds.models import Tag
        t = Tag(name="tag")
        tagid = t.save()
        self.assertNotEqual(tagid, 0)
        self.assertEqual(str(t), "tag")

    def tearDown(self):
        """
        Clean up environment after model tests
        """
        pass

class TaskTest(TestCase):
    """
    Test Tasks

    ..codeauthor: Andreas Neumeier
    """
    def setUp(self):
        """
        Set up enivironment to test models
        """
        self.feed1 = Feed(feed_url=reverse('planet:rss1'), name="rss1", shortname="rss1")
        self.feed1.save()

        self.feed2 = Feed(feed_url=reverse('planet:rss2'), name="rss2", shortname="rss2")
        self.feed2.save()

        self.post1 = Post(feed=self.feed1, link="http://localhost/post1")
        self.post1.save()
        
        self.post2 = Post(feed=self.feed2, link="http://localhost/post2")
        self.post2.save()

    def test_task_time(self):
        dummy.delay(invocation_time=datetime.now())
        dummy(10)

    def test_aggregate(self):
        result = aggregate()
        self.assertEqual(result, True)

    def test_count_tweets(self):
        result = entry_update_twitter(Post.objects.all()[0].id)
        self.assertEqual(result, 0)

    def test_count_share_like(self):
        result = entry_update_facebook(Post.objects.all()[0].id)
        self.assertEqual(result, True)


    def test_feed_refresh(self):
        feed = Feed.objects.all()[0]
        result = feed_refresh(feed.id)
        self.assertGreaterEqual(result[ENTRY_NEW], 0)
        self.assertGreaterEqual(result[ENTRY_UPDATED], 0)
        self.assertGreaterEqual(result[ENTRY_SAME], 0)
        self.assertGreaterEqual(result[ENTRY_ERR], 0)

    def test_entry_process(self):
        f = Feed.objects.all()[0]
        feed = feedparser.parse(f.feed_url)
        for entry in feed.entries:
            result = entry_process(entry, f.id, None, None)
            self.assertEqual(result, True)

    def tearDown(self):
        pass

class ViewsTest(TestCase):
    """
    test Feeds views
    """

    username = "john"
    password = "password"

    def setUp(self):
        """
        Set up enivironment to test models
        """
        self.user = User.objects.create_user(self.username, 'lennon@thebeatles.com', self.password)
        """Test user."""
        
        self.feed1 = Feed(feed_url=reverse('planet:rss1'), name="rss1", shortname="rss1")
        self.feed1.save()
        """Feed 1."""

        self.feed2 = Feed(feed_url=reverse('planet:rss2'), name="rss2", shortname="rss2")
        self.feed2.save()
        """Feed 2."""

        self.client = Client()
        """Test Client."""

    def test_feed_home(self):
        """
        go to feed-home
        """
        result = self.client.get(reverse('planet:feed-home'))
        self.assertEqual(result.status_code, 200)

    def test_feed_home_paginated(self):
        """
        go to feed-home-paginated
        """
        result = self.client.get(reverse('planet:feed-home-paginated', args=("1",)))
        self.assertEqual(result.status_code, 200)

    def test_feed_add_anonymous(self):
        """
        go to feed-add
        """
        result = self.client.get(reverse('planet:feed-add'), follow=False)
        self.assertEqual(result.status_code, 302)
        # self.assertRedirects(result, '/accounts/login')

    def test_feed_add_logged_in_no_credentials(self):
        """
        go to feed-add
        """
        self.client.login(username=self.username, password=self.password)
        result = self.client.get(reverse('planet:feed-add'), follow=False)
        self.assertEqual(result.status_code, 302)
        # self.assertRedirects(result, '/accounts/login')

    def test_feed_add_logged_in_valid_credentials(self):
        """
        go to feed-add
        """
        self.user = User.objects.get(username=self.username)
        permission = Permission.objects.get(codename="add_feed")
        self.user.user_permissions.add(permission)
        self.user.save()
        self.client.login(username=self.username, password=self.password)
        result = self.client.get(reverse('planet:feed-add'), follow=False)
        self.assertEqual(result.status_code, 200)

    def test_feed_add_post_anonymous(self):
        """
        go to feed-add, anonymous client
        """
        result = self.client.post(reverse('planet:feed-add'))
        self.assertEqual(result.status_code, 302)

    def test_feed_add_post_no_credential(self):
        """
        go to feed-add, anonymous client
        """
        result = self.client.post(reverse('planet:feed-add'))
        self.client.login(username=self.username, password=self.password)
        self.assertEqual(result.status_code, 302)

    def test_feed_add_post_valid_credential(self):
        """
        go to feed-add, anonymous client
        """
        result = self.client.post(reverse('planet:feed-add'))
        self.client.login(username=self.username, password=self.password)
        permission = Permission.objects.get(codename="add_feed")
        self.assertEqual(result.status_code, 302)

    def test_feed_view(self):
        """
        go to feed-view for feed 1
        """
        result = self.client.get(reverse('planet:feed-view', args=("rss1",)))
        self.assertEqual(result.status_code, 200)

    def test_category_home(self):
        """
        go to category home
        """
        c = Client()
        result = c.get(reverse('planet:category-home'))
        self.assertEqual(result.status_code, 200)

    def test_tags_home(self):
        """
        go to tags home
        """
        c = Client()
        result = c.get(reverse('planet:tag-home'))
        self.assertEqual(result.status_code, 200)

    def test_FeedRefreshView(self):
        """
        manually refresh a feed
        """
        c = Client()
        result = c.get(reverse('planet:feed-refresh', args=(Feed.objects.all()[0].id,)))
        self.assertEqual(result.status_code, 302)


    def createPost(self):
        """
        create a new post
        """

        with self.assertNumQueries(1):
            Post.objects.create(owner=self.user, feed=self.feed)

# vim: ts=4 et sw=4 sts=4

