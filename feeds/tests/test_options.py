#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from django.test import TestCase, Client, RequestFactory, LiveServerTestCase
from django.core.urlresolvers import reverse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.contrib.auth.models import User

from feeds.views import OptionsView
from feeds.models import Options


class ViewsLoggedInTest(TestCase):
    """
    Test Options views for users that are authenticated.
    """

    username = "john"
    realname = "John Lennon"
    password = "password"

    def setUp(self):
        """
        Set up enivironment to test models
        """
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            self.username,
            self.realname,
            self.password
        )
        self.user.save()
        """Test user."""

    def test_options_anonymous(self):
        """
        Try to view options as anonymous.
        """
        client = Client()
        response = client.get(reverse('planet:options'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(
            response,
            '/accounts/login/?next=%s' % (reverse('planet:options'))
        )

    def test_options_user(self):
        """
        Try to view options as anonymous.
        """
        request = self.factory.get(reverse('planet:options'))
        request.user = self.user
        response = OptionsView.as_view()(request)
        self.assertEquals(response.status_code, 200)

    def test_options_post(self):
        """
        Try to view options as anonymous.
        """
        client = Client()
        client.login(username=self.username, password=self.password)
        response = client.post(
            reverse('planet:options'),
            {

                'number_initially_displayed': "11",
            },

        )
        self.assertEquals(response.status_code, 200)

        """
        .. todo:: This should actually be '11', after
        we updated the value above.
        """
        options = Options.objects.get(user=self.user)
        self.assertEqual(options.user, self.user)
        self.assertEqual(options.number_initially_displayed, 11)


class TestWithSelenium(LiveServerTestCase):
    """
    Test options with browser.
    """
    username = "john"
    realname = "John Lennon"
    password = "password"

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.user = User.objects.create_superuser(
            self.username,
            self.realname,
            self.password
        )

    def tearDown(self):
        self.browser.quit()

    def test_options(self):
        """
        Test the options page from browser.

        .. todo:: This currently only tests for a superuser.
        Also create a regular user.
        """
        self.browser.get(self.live_server_url + '/admin/')

        # She sees the familiar 'Django administration' heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        # She types in her username and passwords and
        # hits return
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(self.username)

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.RETURN)
