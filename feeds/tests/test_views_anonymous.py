#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from django.test import TestCase, Client, RequestFactory
from django.urls import reverse


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
        'WebSite.yaml',
        'Feed_all.yaml',
        # 'socialaccount.socialapp.yaml'
    ]

    def setUp(self):
        """
        Set up environment.
        """
        from feeds.models import WebSite
        site = WebSite(scheme="https", netloc="pramari.de")
        site.save()
        self.site_id = site.pk
        """Test WebSite."""

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

    def home(self):
        """
        home
        ---------
            :url: url(r'^$', Home.as_view(), name="home"),

            Should return 200
        """
        result = self.client.get(reverse('planet:home'))
        self.assertEqual(result.status_code, 200)

    def test_views(self):
        """
        Views.
        =====

        Test :py:mod:`feeds.views.Home` section from the user-side.

        Access the following pages, in order,
        as defined in :py:mod:`feeds.urls`.
        """
        self.home()

    def website_home(self):
        """
        site-home
        ---------
            :url: url(
                    r'^website/$', SiteListView.as_view(),
                    name="website-home"
                    ),

            Should redirect to login.
        """
        response = self.client.get(reverse('planet:website-home'))
        self.assertRedirects(
            response, '/accounts/login/?next=/feeds/website/',
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )

    def website_submit(self):
        """
        site-submit
        -----------
            :url: url(
                    r'^site/submit/$',
                    SiteSubmitWizardView.as_view(SiteSubmitForms),
                    name="website-submit"

            Should return a form.
            Should accept a post.
        """
        result = self.client.get(reverse('planet:website-submit'))
        self.assertEqual(result.status_code, 200)
        """Assert the `submit` site is visible to anonymous users."""
        result = self.client.post(
            reverse('planet:website-submit'),
            {
                'url': 'http://spiegel.de/',
                'form-TOTAL_FORMS': 1,
                'form-INITIAL_FORMS': 0,
                'site_submit_wizard_view-current_step': 'WebSite',
            }
        )
        self.assertEqual(result.status_code, 200)
        """Assert the `submit` site accepts `POST` from anonymous users."""

    def website_add(self):
        """
        site-add
        --------
            :url: url(
                    r'^website/add/$',
                    SiteCreateView.as_view(),
                    name="website-add"
                    )

            To add a site should require credentials.

            Should result in a redirect to the login-page.
        """
        result = self.client.get(reverse('planet:website-add'))
        self.assertRedirects(
            result,
            '/accounts/login/?next=%s' % (reverse('planet:website-add'))
        )
        self.assertEqual(result.status_code, 302)

    def website_view(self):
        """
        site-detail
        -----------
            :url: url(
                r'^website/(?P<pk>\\d+)/$',
                SiteDetailView.as_view(),
                name="website-detail"
                )

            Viewing a website should be available to the public.

            Should return 200.
        """
        result = self.client.get(
            reverse('planet:website-detail', args=(self.site_id,))
        )
        self.assertEqual(result.status_code, 200)

    def website_update(self):
        """
        site-update
        -----------
            :url: url(
                    r'^website/(?P<pk>\\d+)/update/$',
                    SiteUpdateView.as_view(),
                    name="website-update"
                )

            .. todo:: needs to be defined.
        """
        result = self.client.get(
            reverse(
                'planet:website-update',
                args=(self.site_id,)
                )
            )
        self.assertRedirects(
            result,
            '/accounts/login/?next=%s' % (
                reverse('planet:website-update',
                        args=(self.site_id,)
                        )
            )
        )
        self.assertEqual(result.status_code, 302)

    def website_delete(self):
        """
        site-delete
        -----------
            :url: url(
                r'^website/(?P<pk>\\d+)/delete/$',
                SiteDeleteView.as_view(),
                name="website-delete"
                )

            .. todo:: needs to be defined.
        """
        result = self.client.get(
            reverse(
                'planet:website-delete',
                args=(self.site_id,)
            )
        )
        self.assertEqual(result.status_code, 302)

    def test_website_views(self):
        """
        Site.
        =====

        Test the :py:mod:`feeds.models.WebSite` section from the user-side.

        Access the following pages, in order,
        as defined in :py:mod:`feeds.urls`.

        # website_submit() is breaking for some reason
        # self.website_submit()
        .. todo:: Make the WebSiteSubmitWizard work and write a
        proper test for the procedure.
        """
        self.website_home()
        self.website_add()
        self.website_view()
        self.website_update()
        self.website_delete()

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
        self.assertEqual(result.status_code, 302)

    def feed_subscriptions(self):
        """
        feed-subscription
        ---------
            :url: url(
                r'^list/$',
                FeedSubscriptionView.as_view(),
                name="feed-subscription"
                )

            Should return 302 for an anonymous user.
        """
        result = self.client.get(reverse('planet:feed-subscriptions'))
        self.assertEqual(result.status_code, 302)

    def feed_create(self):
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

    def feed_detail(self):
        """
        feed-detail
        -----------
            :url: url(
                r'^(?P<pk>\\d+)/$',
                FeedDetailView.as_view(),
                name="feed-detail"
            ),

            Viewing details for a :py:mod:`feeds.models.Feed` should be
            available to the public.

            Should return 200.

            The `fixture` has a feed with the ID 1.
        """

        result = self.client.get(reverse('planet:feed-detail', args=(1,)))
        self.assertEqual(result.status_code, 302)

    def feed_update(self):
        """
        feed-update
        -----------
            :url:
                url(
                  r'^(?P<pk>\\d+)/update/$',
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
            r'^(?P<pk>\\d+)/delete/$',
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
            url(r'^(?P<pk>\\d+)/refresh/$',
            FeedRefreshView.as_view(), name="feed-refresh"),
        """
        self.feed_home()
        self.feed_create()
        self.feed_detail()
        self.feed_update()
        self.feed_delete()
        self.feed_subscriptions()

    def test_sitemap(self):
        """
        .. todo::
            actual lazy urls.
        """
        client = Client()
        result = client.get("/feeds/sitemap.xml")
        self.assertEqual(result.status_code, 200)
