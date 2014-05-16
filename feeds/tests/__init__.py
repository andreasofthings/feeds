#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
Tests for the "feeds" app.
==========================

  :date: 2014-05-03
  :version: 0.1
  :description: Test Cases for :py:mod:`feeds`

- :py:mod:`feeds.models`
- :py:mod:`feeds.views`

 - for anonymous users / not logged in
 - for logged in users

- :py:mod:`feeds.tasks`

.. moduleauthor:: Andreas Neumeier <andreas@neumeier.org>

"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

import pkgutil
import unittest

for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(module_name).load_module(module_name)
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, unittest.case.TestCase):
            exec ('%s = obj' % obj.__name__)


class ViewsAnonymousTest(TestCase):
    """
    Test whether all :py:mod:`feeds.views` are working.

    Working, in this context means the, corresponding URL returns:

    - "2xx OK" for publically visible sites/pages.
    - "3xx Redirect" for pages that require authentication.

    URLs available in :mod:`feeds` are defined in :mod:`feeds.urls`.

    .. moduleauthor:: Andreas Neumeier <andreas@neumeier.org>
    """

    fixtures = ['Feed.yaml']

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

    def test_feed_home(self):
        """
        Go to feed-home.

        Assert the returned page comes with "HTTP 200 OK".

        .. todo:: define/document expected result/return values.
        """
        result = self.client.get(reverse('planet:feed-home'))
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

    def test_sitemap(self):
        client = Client()
        result = client.get("/sitemap.xml")
        self.assertEqual(result.status_code, 200)
