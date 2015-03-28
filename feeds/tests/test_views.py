#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User, Permission

from feeds.models import Feed, Post, Category


class ViewsAnonymousTest(TestCase):
    """
    Test whether all :py:mod:`feeds.views` are working.

    Working, in this context means the, corresponding URL returns:

    - "2xx OK" for publically visible sites/pages.
    - "3xx Redirect" for pages that require authentication.

    URLs available in :mod:`feeds` are defined in :mod:`feeds.urls`.

    .. moduleauthor:: Andreas Neumeier <andreas@neumeier.org>
    """

    fixtures = [
        'Feed_all.yaml',
        'Categories.yaml',
    ]

    def setUp(self):
        """
        Set up environment.
        """
        from feeds.models import Site
        site = Site(url="https://angry-planet.com/")
        site.save()
        self.site_id = site.pk
        """Test Site."""

        self.client = Client()
        """Test Client."""

        self.factory = RequestFactory()
        """Test Client."""

    def test_feed_options(self):
        """
        Go to the options page.

        This is only available per user.

        Assert the returned page comes with "HTTP 302 Redirect".
        """
        result = self.client.get(reverse('planet:options'))
        self.assertEqual(result.status_code, 302)
        self.assertRedirects(
            result,
            '/accounts/login/?next=%s' % (reverse('planet:options'))
        )

    def test_opml_import(self):
        """
        Go to the options page.

        This is only available per user.

        Assert the returned page comes with "HTTP 302 Redirect".
        """
        with open('feeds/tests/data/feedly.opml') as fp:
            result = self.client.post(
                reverse('planet:opml'),
                {
                    'opml': fp.read(),
                }
            )
        self.assertEqual(result.status_code, 200)

    def site_home(self):
        """
        site-home
        ---------
            :url: url(r'^site/$', SiteListView.as_view(), name="site-home"),

            Should return 200
        """
        result = self.client.get(reverse('planet:site-home'))
        self.assertEqual(result.status_code, 200)

    def site_submit(self):
        """
        site-submit
        -----------
            :url: url(
                    r'^site/submit/$',
                    SiteSubmitWizardView.as_view(SiteSubmitForms),
                    name="site-submit"

            Should return a form.
            Should accept a post.
        """
        result = self.client.get(reverse('planet:site-submit'))
        self.assertEqual(result.status_code, 200)
        """Assert the `submit` site is visible to anonymous users."""
        result = self.client.post(
            reverse('planet:site-submit'),
            {
                'url': 'http://spiegel.de/',
                'form-TOTAL_FORMS': 1,
                'form-INITIAL_FORMS': 0,
                'site_submit_wizard_view-current_step': 'Site',
            }
        )
        self.assertEqual(result.status_code, 200)
        """Assert the `submit` site accepts `POST` from anonymous users."""

    def site_add(self):
        """
        site-add
        --------
            :url: url(
                    r'^site/add/$',
                    SiteCreateView.as_view(),
                    name="site-add"
                    )

            To add a site should require credentials.

            Should result in a redirect to the login-page.
        """
        result = self.client.get(reverse('planet:site-add'))
        self.assertRedirects(
            result,
            '/accounts/login/?next=%s' % (reverse('planet:site-add'))
        )
        self.assertEqual(result.status_code, 302)

    def site_view(self):
        """
        site-view
        ---------
            :url: url(
                r'^site/(?P<pk>\d+)/$',
                SiteDetailView.as_view(),
                name="site-view"
                )

            Viewing a site should be available to the public.

            Should return 200.
        """
        result = self.client.get(
            reverse('planet:site-view', args=(self.site_id,))
        )
        self.assertEqual(result.status_code, 200)

    def site_update(self):
        """
        site-update
        -----------
            :url: url(
                    r'^site/(?P<pk>\d+)/update/$',
                    SiteUpdateView.as_view(),
                    name="site-update"
                )

            .. todo:: needs to be defined.
        """
        result = self.client.get(
            reverse(
                'planet:site-update',
                args=(self.site_id,)
                )
            )
        self.assertRedirects(
            result,
            '/accounts/login/?next=%s' % (
                reverse('planet:site-update',
                        args=(self.site_id,)
                        )
            )
        )
        self.assertEqual(result.status_code, 302)

    def site_delete(self):
        """
        site-delete
        -----------
            :url: url(
                r'^site/(?P<pk>\d+)/delete/$',
                SiteDeleteView.as_view(),
                name="site-delete"
                )

            .. todo:: needs to be defined.
        """
        result = self.client.get(
            reverse(
                'planet:site-delete',
                args=(self.site_id,)
            )
        )
        self.assertEqual(result.status_code, 302)

    def test_site_views(self):
        """
        Site.
        =====

        Test the :py:mod:`feeds.models.Site` section from the user-side.

        Access the following pages, in order,
        as defined in :py:mod:`feeds.urls`.
        """
        self.site_home()
        self.site_submit()
        self.site_add()
        self.site_view()
        self.site_update()
        self.site_delete()

    def feed_home(self):
        """
        feed-home
        ---------
            :url: url(
                r'^list/$',
                FeedListView.as_view(),
                name="feed-home"
                )

                name="feed-home"
                )

                FeedListView.as_view(),
                name="feed-home"
                )

            Should return 200 for an anonymous user.
        """
        result = self.client.get(reverse('planet:feed-home'))
        self.assertEqual(result.status_code, 200)

    def feed_home_paginated(self):
        """
        feed-home-paginated
        -------------------
            :url: url(
                     r'^page/(?P<page>\w+)/$',
                     FeedListView.as_view(),
                     name="feed-home-paginated"
                  ),

            - Should return 200 for an anonymous user.
            - Should allow to navigate between paginated results.
        """
        result = self.client.get(
            reverse(
                'planet:feed-home-paginated',
                args=(1,)
            )
        )
        self.assertEqual(result.status_code, 200)

    def feed_add(self):
        """
        feed-add
        --------
            :url: url(r'^add/$', FeedCreateView.as_view(), name="feed-add"),

        """
        result = self.client.get(reverse('planet:feed-add'))
        self.assertRedirects(
            result,
            '/accounts/login/?next=%s' % (reverse('planet:feed-add'))
        )
        self.assertEqual(result.status_code, 302)

    def feed_view(self):
        """
        feed-view
        ---------
            :url: url(
                r'^(?P<pk>\d+)/$',
                FeedDetailView.as_view(),
                name="feed-view"
            ),

            Viewing details for a :py:mod:`feeds.models.Feed` should be
            available to the public.

            Should return 200.

            The `fixture` has a feed with the ID 1.
        """

        result = self.client.get(reverse('planet:feed-view', args=(1,)))
        self.assertEqual(result.status_code, 200)

    def feed_update(self):
        """
        feed-update
        -----------
            :url:
                url(
                  r'^(?P<pk>\d+)/update/$',
                  FeedUpdateView.as_view(),
                  name="feed-update"
                  )

            The `fixture` has a feed with the ID 1.

            .. todo:: needs to be defined.
        """
        result = self.client.get(reverse('planet:feed-update', args=(1,)))
        self.assertRedirects(
            result,
            '/accounts/login/?next=%s' % (
                reverse(
                    'planet:feed-update',
                    args=(1,)
                )
            )
        )
        self.assertEqual(result.status_code, 302)

    def feed_delete(self):
        """
        feed-delete
        -----------
            :url: url(
            r'^(?P<pk>\d+)/delete/$',
            FeedDeleteView.as_view(),
            name="feed-delete"
            ),

            The `fixture` has a feed with the ID 1.

            .. todo:: needs to be defined.
        """
        result = self.client.get(reverse('planet:feed-delete', args=(1,)))
        self.assertRedirects(
            result,
            '/accounts/login/?next=%s' % (
                reverse(
                    'planet:feed-delete',
                    args=(1,)
                )
            )
        )
        self.assertEqual(result.status_code, 302)

    def test_feed_views(self):
        """
        Feed.
        =====

        Test Feed Views:

        .. todo::
            url(r'^(?P<pk>\d+)/refresh/$',
            FeedRefreshView.as_view(), name="feed-refresh"),
        """
        self.feed_home()
        self.feed_home_paginated()
        self.feed_add()
        self.feed_view()
        self.feed_update()
        self.feed_delete()
        # self.feed_refresh()

    def category_home(self):
        """
        category-home
        -------------

            :url: url(
                r'^category/$',
                CategoryListView.as_view(),
                name="category-home"
            ),

            Viewing details for a :py:mod:`feeds.models.Category` should be
            available to the public.

            Should return 200 for an anonymous user.
        """
        result = self.client.get(reverse('planet:category-home'))
        self.assertEqual(result.status_code, 200)

    def category_home_paginated(self):
        """
        category-home
        -------------

            :url: url(
                r'^category/$',
                CategoryListView.as_view(),
                name="category-paginated"
            ),

            Viewing details for a :py:mod:`feeds.models.Category` should be
            available to the public.

            Should return 200 for an anonymous user.
        """
        result = self.client.get(
            reverse(
                'planet:category-home-paginated',
                args=(1,)
            )
        )
        self.assertEqual(result.status_code, 200)

    def category_view(self):
        """
        category-view
        -------------
            :url: url(
                r'^(?P<pk>\d+)/$',
                CategoryDetailView.as_view(),
                name="feed-view"
            ),

            Viewing details for a :py:mod:`feeds.models.Category` should be
            available to the public.

            Should return 200.

            The `fixture` has a feed with the ID 1.
        """
        category = Category.objects.all()
        result = self.client.get(
            reverse(
                'planet:category-view',
                args=(category[0].pk,)
            )
        )
        self.assertEqual(result.status_code, 200)

    def test_category_views(self):
        """
        Category.
        =========

        Test Category Views:

        """
        self.category_home()
        self.category_home_paginated()
        # self.category_add()
        self.category_view()
        # self.category_update()
        # self.category_delete()

    def test_sitemap(self):
        client = Client()
        result = client.get("/sitemap.xml")
        self.assertEqual(result.status_code, 200)


class TestAllViewsLoggedIn(TestCase):
    """
    Test Feeds views for users that are authenticated.
    """

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

    def test_feed_home(self):
        """
        go to feed-home

        .. todo:: rename and restructure as in
        :py:mod:`feeds.tests.ViewsAnonymousTest`.
        """
        result = self.client.get(reverse('planet:feed-home'))
        self.assertEqual(result.status_code, 200)

    def test_feed_home_paginated(self):
        """
        go to feed-home-paginated
        """
        result = self.client.get(
            reverse(
                'planet:feed-home-paginated',
                args=("1",)
            )
        )
        self.assertEqual(result.status_code, 200)

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
            Post.objects.create(feed=feed)


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
