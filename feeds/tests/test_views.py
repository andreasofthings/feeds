#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from datetime import datetime

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User, Permission

from feeds.models import Feed, Post


class TestAllViewsLoggedIn(TestCase):
    """
    Test Feeds views for users that are authenticated.
    """

    fixtures = [
        'Feed_all.yaml',
    ]

    username = "john"
    password = "password"

    def setUp(self):
        """
        Set up enivironment to test models
        """
        self.user = User.objects.create_user(
            self.username,
            'lennon@thebeatles.com',
            self.password
        )
        """Test user."""

        self.feed1 = Feed(
            feed_url=reverse('planet:rss1'),
            name="rss1",
            short_name="rss1"
        )
        self.feed1.save()
        """Feed 1."""

        self.feed2 = Feed(
            feed_url=reverse('planet:rss2'),
            name="rss2",
            short_name="rss2"
        )
        self.feed2.save()
        """Feed 2."""

        self.client = Client()
        """Test Client."""

    def site_add(self):
        """.. todo:: todo"""
        pass

    def test_site(self):
        """
        test_site
        ---------

        Test all aspects of "Site" as a logged in user.

        - add
        - submit
        - view
        - update
        """
        self.site_add()

    def feed_home(self):
        """
        go to feed-home

        .. todo:: rename and restructure as in
        :py:mod:`feeds.tests.ViewsAnonymousTest`.
        """
        result = self.client.get(reverse('planet:feed-home'))
        self.assertEqual(result.status_code, 200)

    def feed_subscribe(self):
        """
        test feed-subscribe
        ---------
            :url: url(
                r'^list/$',
                FeedSubscribeView.as_view(),
                name="feed-subscription"
                )

            Should return 302 for an authenticated user and redirect to the
            details-page for the just subscribed feed.
        """
        self.client.login(
            username=self.username,
            password=self.password
        )
        result = self.client.get(
            reverse('planet:feed-subscribe', kwargs={'pk': 1})
        )
        self.assertEqual(result.status_code, 302)
        self.assertRedirects(
            result,
            reverse('planet:feed-view', kwargs={'pk': 1})
        )

    def feed_subscription(self):
        """
        test feed-subscription
        ---------
            :url: url(
                r'^list/$',
                FeedSubscriptionView.as_view(),
                name="feed-subscription"
                )

            Should return 200 for an authenticated user.
        """
        self.client.login(
            username=self.username,
            password=self.password
        )
        result = self.client.get(reverse('planet:feed-subscriptions'))
        self.assertEqual(result.status_code, 200)

    def feed_update(self):
        """
        test FeedUpdateView
        """
        self.client.login(
            username=self.username,
            password=self.password
        )
        result = self.client.get(
            reverse('planet:feed-update', kwargs={'pk': 1})
        )
        self.assertEqual(result.status_code, 200)

    def feed_delete(self):
        """
        Test FeedDeleteView

        Probably better through Selenium
        """
        pass

    def test_feed(self):
        """
        Run tests for all views related to feeds.
        - self.feed_home
        """
        self.feed_home()
        self.feed_subscribe()
        self.feed_subscription()
        self.feed_update()
        self.feed_delete()

    def test_feed_add(self):
        """
        Go to feed-add.
        This should require the proper credentials.
        """
        result = self.client.get(reverse('planet:feed-add'), follow=False)
        self.assertEqual(result.status_code, 302)

    def test_feed_add_no_credentials(self):
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
        self.client.login(
            username=self.username,
            password=self.password
        )
        """
        .. todo:: this currently gives
        'AttributeError: 'module' object has no
        attribute 'CRISPY_TEMPLATE_PACK'.
        """
        # result = self.client.get(reverse('planet:feed-add'), follow=False)
        # self.assertEqual(result.status_code, 200)

    def test_feed_add_post_anonymous(self):
        """
        go to feed-add, anonymous client
        """
        result = self.client.post(reverse('planet:feed-add'))
        self.client.login(username=self.username, password=self.password)
        self.assertEqual(result.status_code, 302)

    def test_feed_view(self):
        """
        go to feed-view for feed 1
        """
        feed_id = Feed.objects.all()[0].pk
        result = self.client.get(reverse('planet:feed-view', args=(feed_id,)))
        """.. todo:: figure out why this gives 404"""
        self.assertEqual(result.status_code, 200)

    def test_feed_refresh_view(self):
        """
        manually refresh a feed
        """
        c = Client()
        feeds = Feed.objects.all()
        result = c.get(reverse('planet:feed-refresh', args=(feeds[0].pk,)))
        self.assertEqual(result.status_code, 302)

    def test_create_post(self):
        """
        create a new post
        """
        feed = Feed.objects.all()[0]
        """
        Get first feed from the db.
        We use fixtures, so we can assume there are feeds.
        """
        with self.assertNumQueries(1):
            Post.objects.create(
                feed=feed,
                published=datetime.now()
            )


class TestFeedViewsWithCredentials(TestCase):
    """
    Test those aspects of :py:mod:`feeds.views` related to
    py:mod:`feeds.models.Feed`, that require proper cedentials.
    """

    fixtures = ['Feed_all.yaml', ]

    username = "john"
    password = "password"

    def setUp(self):
        """
        Set up enivironment to test models
        """
        self.user = User.objects.create_user(
            self.username,
            'lennon@thebeatles.com',
            self.password
        )
        """Test user."""

        permission = Permission.objects.get(codename="add_feed")
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename="change_feed")
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(codename="can_refresh_feed")
        self.user.user_permissions.add(permission)
        """Give the test user proper permission."""

    def test_feed_add_post(self):
        """
        go to feed-add
        add a post.
        """
        self.client.login(username=self.username, password=self.password)
        result = self.client.get(reverse('planet:feed-add'))
        self.assertEqual(result.status_code, 200)
        result = self.client.post(
            reverse('planet:feed-add'),
        )
        self.assertEqual(result.status_code, 200)

    def test_feed_update_view(self):
        """
        Test whether a user with proper credentials can update a feed.
        """
        c = Client()
        c.login(username=self.username, password=self.password)
        feeds = Feed.objects.all()
        result = c.post(reverse('planet:feed-update', args=(feeds[0].pk,)),
                        {'feed_url': "http://spiegel.de/index.rss"}
                        )
        self.assertEquals(result.status_code, 302)
        self.assertRedirects(result, reverse('planet:feed-home'))

    def test_feed_refresh_view(self):
        """
        manually refresh a feed
        """
        c = Client()
        c.login(username=self.username, password=self.password)
        feeds = Feed.objects.all()
        result = c.get(reverse('planet:feed-refresh', args=(feeds[0].pk,)))
        expected = reverse('planet:feed-view', args=(feeds[0].pk,))
        self.assertEqual(result.status_code, 302)
        self.assertRedirects(result, expected)

    def test_post_list_view(self):
        """
        Test PostListView
        """
        c = Client()
        c.login(username=self.username, password=self.password)
        result = c.get(reverse('planet:post-home'))
        self.assertEqual(result.status_code, 200)
        result = c.get(reverse('planet:post-home')+'?paginate_by=15')
        self.assertEqual(result.status_code, 200)
        result = c.get(reverse('planet:post-home')+'?page=2')
        self.assertEqual(result.status_code, 404)
        """we won't have a 2nd page for now."""
