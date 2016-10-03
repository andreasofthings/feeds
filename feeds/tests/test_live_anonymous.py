#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 et sw=4 sts=4

"""
"""

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse

from selenium import webdriver


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

    def test_anonymous(self):
        """
        Test the home page from browser.
        """
        self.browser.get(self.live_server_url + reverse('planet:home'))
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Feeds', body.text)

        self.browser.get(self.live_server_url + reverse('planet:website-home'))
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Andreas', body.text)

        self.browser.get(self.live_server_url + reverse('planet:feed-home'))
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Andreas', body.text)

        self.browser.get(self.live_server_url + reverse('planet:post-home'))
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Andreas', body.text)

    def tearDown(self):
        self.browser.quit()
