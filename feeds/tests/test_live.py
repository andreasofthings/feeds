#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TestAllViewsAnonymousLive(LiveServerTestCase):
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

    def test_home(self):
        """
        Test the home page from browser.
        """
        self.browser.get(self.live_server_url + reverse('planet:home'))
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Feeds', body.text)

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
